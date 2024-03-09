import json
import requests
from bs4 import BeautifulSoup
import os
import mysql.connector

## WORK IN PROGRESS
## DOES NOT WORK

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

# Function to scrape images from MyAnimeList
def scrape_anime_images(cursor):
    # Retrieve anime URLs from your database
    cursor.execute("SELECT title, url FROM anime")
    anime_records = cursor.fetchall()

    # Folder to save downloaded images
    image_folder = "anime_images"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    for title, url in anime_records:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the cover photo image element
            image_element = soup.find("img", class_="image")

            print(f"Found image element for anime: {title} - {image_element}")

            if image_element:
                # Get the image URL
                image_url = image_element["data-src"]

                # Download the image
                image_filename = f"{title}.jpg"
                image_path = os.path.join(image_folder, image_filename)
                with open(image_path, "wb") as f:
                    image_data = requests.get(image_url).content
                    f.write(image_data)

                print(f"Downloaded image for anime: {title}")

        except Exception as e:
            print(f"Error processing anime '{title}': {e}")

    print("Image scraping completed.")

# Usage
config_file = "private/config.json"  # Replace with the path to your JSON file
connector = MySQLConnector(config_file)
db, cursor = connector.connect()

scrape_anime_images(cursor)
