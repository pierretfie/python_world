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

#log workouts 
def log_workout(user_id, exercise, sets, reps, duration, calories):
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS workouts 
                      (id INTEGER PRIMARY KEY, user_id INTEGER, exercise TEXT, sets INTEGER, reps INTEGER, 
                       duration REAL, calories REAL, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    cursor.execute("INSERT INTO workouts (user_id, exercise, sets, reps, duration, calories) VALUES (?, ?, ?, ?, ?, ?)",
                   (user_id, exercise, sets, reps, duration, calories))
    conn.commit()
    conn.close()

# Example usage
log_workout(1, "Push-ups", 3, 10, 5, 50)