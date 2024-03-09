import json
import requests
from bs4 import BeautifulSoup
import mysql.connector

class MySQLConnector:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        self.host = config["mysql"]["host"]
        self.user = config["mysql"]["user"]
        self.password = config["mysql"]["password"]
        self.database = config["mysql"]["database"]
    
    def connect(self):
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.db.cursor()
        return self.db, self.cursor

# Usage
config_file = "private/config.json"  # Replace with the path to your JSON file
connector = MySQLConnector(config_file)
db, cursor = connector.connect()

# Function to scrape and store anime data from MyAnimeList
def scrape_top_100_anime(cursor, db):
    url = "https://myanimelist.net/topanime.php"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        print(f"Failed to fetch the top anime page: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    anime_list = soup.find_all("tr", class_="ranking-list")
    
    if not anime_list:
        print("No anime found in the top anime page.")
        return

    for anime in anime_list[:30]:  # Limiting to 30 for demonstration
        # Extract title and URL of each anime
        title_element = anime.find("div", class_="detail")
        if title_element:
            title = title_element.find("div", class_="di-ib clearfix").text.strip()
            anime_url = title_element.find("a")["href"]
        else:
            title = "Title Not Found"  # Placeholder value if title is not found
            anime_url = None

        rating_element = anime.find("td", class_="score")
        if rating_element:
            rating = rating_element.text.strip()
        else:
            rating = None  # If rating is not found, set to None 

        # Extract additional information from the anime page
        if anime_url:
            anime_info = scrape_anime_page(anime_url)
            if anime_info:
                genres = anime_info.get("genres")
                synopsis = anime_info.get("synopsis")

                # Store data in MySQL database
                try:
                    cursor.execute("INSERT INTO anime (title, genres, rating, synopsis, url) VALUES (%s, %s, %s, %s, %s)",
                                   (title, genres, rating, synopsis, anime_url))
                    db.commit()
                    print(f"Inserted anime: {title}")
                except mysql.connector.Error as err:
                    print(f"Error inserting anime '{title}': {err}")

    print("Scraping and storing completed.")

# Function to scrape additional information from the individual anime page
def scrape_anime_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        print(f"Failed to fetch anime page: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract genres
    genre_elements = soup.find_all("span", itemprop="genre")
    genres = [genre.text.strip() for genre in genre_elements]

    # Extract synopsis
    synopsis_element = soup.find("p", itemprop="description")
    synopsis = synopsis_element.text.strip() if synopsis_element else None


    anime_info = {
        "genres": ", ".join(genres),
        "synopsis": synopsis,
    }

    return anime_info

# Usage
scrape_top_100_anime(cursor, db)
