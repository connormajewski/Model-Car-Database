import sqlite3
from datetime import datetime

creation_query = '''
    CREATE TABLE IF NOT EXISTS models(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand VARCHAR(64) NOT NULL,
        year INTEGER NOT NULL,
        description VARCHAR(256),
        scale VARCHAR(8) NOT NULL,
        condition VARCHAR(16) NOT NULL,
        quantity INTEGER NOT NULL,
        value DECIMAL(5,2)
    )
'''

# Initial database creation/connection.

def create_database_connection():
    try:
        connection = sqlite3.connect('catalogue.db')
        return connection
    except sqlite3.Error as error:
        print(f"Error connecting to database: {error}")
        return None

           
def create_table(creation_query):
    try:
        connection = create_database_connection()
        cursor = connection.cursor()
        cursor.execute(creation_query)
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        printf(f"Error creating models table: {error}")

        
def execute_query(query, params=None):
    try:
        connection = create_database_connection()
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        results = cursor.fetchall()
        cursor.close()
        return results
    except sqlite3.Error as error:
        print(f"Error executing query: {error}")
        return []


def add_model(brand, year, description, scale, condition, quantity, value):
    insertion_query = f"INSERT INTO models (brand, year, description, scale, condition, quantity, value) VALUES('{brand}', {year}, '{description.replace("'", "''")}', '{scale}', '{condition}', {quantity}, {value})"
    try:
        execute_query(insertion_query)
    except sqlite3.Error as error:
        print(f"Error inserting model: {error}")
    
"""    
def query_all_models():
    selection_query = "SELECT * FROM models ORDER BY id"
    results = execute_query(selection_query)
    return results
    
def query_total_value():
    selection_query = "SELECT SUM(value) FROM models"
    result = execute_query(selection_query)
    return result
"""