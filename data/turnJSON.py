import json
import mysql.connector
from decimal import Decimal

# Connect to MySQL database
db = mysql.connector.connect(
    host="TravisPC",
    user="DuhBoss32",
    password="9379544trav",
    database="testing"
)

# Function to fetch anime data from MySQL database
def fetch_anime_data():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM anime")
    anime_data = cursor.fetchall()
    cursor.close()
    return anime_data

# Function to convert Decimal objects to a JSON serializable format
def convert_decimal(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

# Export anime data to a JSON file
def export_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, default=convert_decimal, indent=4)

# Fetch anime data from the database
anime_data = fetch_anime_data()

# Export anime data to a JSON file
export_to_json(anime_data, 'anime_data.json')

