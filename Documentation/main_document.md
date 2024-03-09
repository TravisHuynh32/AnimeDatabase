# Anime Database Scraper

## Introduction
This Python script scrapes data from MyAnimeList to retrieve information about the top anime series and stores it in a MySQL database.

## Dependencies
- `json`: Used for reading the MySQL configuration from a JSON file.
- `requests`: Used for making HTTP requests to fetch web pages.
- `bs4` (BeautifulSoup): A library for pulling data out of HTML and XML files.
- `mysql.connector`: A MySQL driver for Python.

## Configuration
The script requires a MySQL database to store the scraped data. The database configuration details are stored in a JSON file (`config.json`).

## MySQLConnector Class
- **Description**: This class is responsible for establishing a connection to the MySQL database using the provided configuration file.
- **Attributes**:
  - `host`: Hostname of the MySQL server.
  - `user`: Username for database access.
  - `password`: Password for database access.
  - `database`: Name of the database.
- **Methods**:
  - `__init__(config_file)`: Initializes the MySQL connection parameters from the provided JSON configuration file.
  - `connect()`: Establishes a connection to the MySQL database and returns the database connection and cursor.

## Functions
1. **`scrape_top_100_anime(cursor, db)`**:
   - Description: Scrapes the top anime data from MyAnimeList and stores it in the MySQL database.
   - Parameters:
     - `cursor`: MySQL cursor object for executing SQL queries.
     - `db`: MySQL database connection object.
   - Steps:
     1. Fetches the top anime page from MyAnimeList.
     2. Parses the HTML content to extract anime titles, ratings, genres, and synopses.
     3. Stores the extracted data in the MySQL database.

2. **`scrape_anime_page(url)`**:
   - Description: Scrapes additional information from an individual anime page.
   - Parameters:
     - `url`: URL of the individual anime page on MyAnimeList.
   - Returns: A dictionary containing the genres and synopsis of the anime.
   - Steps:
     1. Fetches the HTML content of the provided URL.
     2. Parses the HTML content to extract genre and synopsis information.
     3. Returns the extracted data as a dictionary.

## Usage
- The script initializes a `MySQLConnector` object with the MySQL configuration file.
- It then connects to the MySQL database using the `connect()` method.
- The `scrape_top_100_anime()` function is called to scrape and store the top anime data in the database.

## Execution
- To execute the script, simply run the file.
- Ensure that the MySQL server is running and accessible.
- The script will print status messages indicating the progress of the scraping process.
