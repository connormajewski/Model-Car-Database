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


def add_model(brand, year, scale, condition, quantity, description='', value=0.0):
    
    attr = ["brand", "year", "scale", "condition", "quantity"]
    attr_value = [brand, int(year), scale, condition, int(quantity)]
    placeholders = ["?", "?", "?", "?", "?"]
    
    if description != '':
        attr.append("description")
        attr_value.append(f"'description'")
        placeholders.append("?")
        
    
    attr.append("value")
    attr_value.append(0.0 if value == '' else float(value))
    placeholders.append("?")
        
    attr_string = ", ".join(attr)
    print(attr)
    placeholders_string  = ", ".join(placeholders)
    query = f"INSERT INTO models ({attr_string}) VALUES ({placeholders_string})"
    
    print(query)
    print(attr_value)
    
    try:
        execute_query(query, tuple(attr_value))
    except sqlite3.Error as error:
        print(f"Error inserting model: {error}")
        
def update_model(model_id, brand=None, year=None, scale=None, condition=None, quantity=None, description=None, value=None):
    
    attr=["brand", "year", "scale", "condition", "quantity", "description", "value"]
    attr_value=[brand, year, scale, condition, quantity, description, value]
    
    query_values = []
    query_attr = []
    
    for i in range(len(attr)):
        if(attr_value[i] != ''):
            if attr[i] == 'year' or attr_value[i] == 'quantity':
                query_attr.append(attr[i])
                query_values.append(int(attr_value[i]))
            elif attr[i] == 'value':
                query_attr.append(attr[i])
                query_values.append(float(attr_value[i]))
            else:
                query_attr.append(attr[i])
                query_values.append(f"'{attr_value[i]}'")

   
    
    q = ", ".join([f"{a} = {b}" for a, b in zip(query_attr, query_values)])
   
    query=f"UPDATE models SET {q} WHERE id is {model_id}"
 
    try:
        execute_query(query)
    except sqlite3.Error as error:
        print(f"Error deleting model: {error}") 
 
def delete_model(model_id):
    try:
        query = f"DELETE FROM models WHERE id is {model_id}"
        print(query)
        execute_query(query)
    except sqlite3.Error as error:
        print(f"Error deleting model: {error}")  
   