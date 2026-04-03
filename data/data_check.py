from sqlite3 import *
import os
# function to initialize the database
def init_db():
    # check if the data folder exists
    if not os.path.exists('data'):
        os.makedirs('data')
    conn = connect('data/data.db')
    cursor = conn.cursor()
    # to check it the table name user exists or not 
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

