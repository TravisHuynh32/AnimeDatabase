import json
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

def delete_all_data(cursor, db):
    confirm = input("Are you sure you want to delete all data from the 'anime' table? (yes/no): ")
    if confirm.lower() == "yes":
        cursor.execute("DELETE FROM anime")
        db.commit()
        print("All data deleted from the 'anime' table.")
        exit()
    else:
        print("Deletion canceled.")

delete_all_data(cursor, db)
