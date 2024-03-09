import pandas as pd
import json
import mysql.connector
import matplotlib.pyplot as plt

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
        if self.db.is_connected():
            print("Connected to MySQL database")
        else:
            print("Failed to connect to MySQL database")
        return self.db


# Function to fetch anime data from MySQL database using pandas
def fetch_anime_data(conn):
    query = "SELECT * FROM anime"
    anime_data = pd.read_sql(query, conn)

    return anime_data

# Usage
config_file = "private/config.json"  # Replace with the path to your JSON file
connector = MySQLConnector(config_file)
db = connector.connect()

# Fetch anime data from the database using pandas
anime_data = fetch_anime_data(db)
print("Anime data:")
print(anime_data)
