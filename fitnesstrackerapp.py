#user details db

import sqlite3

def create_database():
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, weight REAL, height REAL, goal TEXT)''')
    conn.commit()
    conn.close()

def add_user(name, age, weight, height, goal):
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age, weight, height, goal) VALUES (?, ?, ?, ?, ?)",
                   (name, age, weight, height, goal))
    conn.commit()
    conn.close()

# Example usage
create_database()
add_user("John", 25, 70, 175, "Lose weight")