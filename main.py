import sqlite3
from datetime import datetime, timedelta
import random

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('workout_stats.db')
cursor = conn.cursor()

# Create a table to store workout stats
cursor.execute('''
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY,
    date TEXT,
    exercise TEXT,
    sets INTEGER,
    reps INTEGER,
    weight REAL
)
''')

# Function to add a new workout
def add_workout(exercise, sets, reps, weight, date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
    INSERT INTO workouts (date, exercise, sets, reps, weight)
    VALUES (?, ?, ?, ?, ?)
    ''', (date, exercise, sets, reps, weight))
    conn.commit()

# Function to retrieve workouts
def get_workouts():
    cursor.execute('SELECT * FROM workouts')
    return cursor.fetchall()

# Function to generate random workouts
def generate_random_workouts():
    exercises = [
        "Chest Press", "Lat Raises", "Shoulder Press", "Bicep Curls",
        "Pull-Ups", "Lat Pull-Downs", "Tricep Pulldowns", "Forearm Curls"
    ]
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    for exercise in exercises:
        for _ in range(20):
            random_date = start_date + timedelta(days=random.randint(0, 365))
            sets = random.randint(3, 5)
            reps = random.randint(8, 12)
            weight = round(random.uniform(10, 100), 1)
            add_workout(exercise, sets, reps, weight, random_date.strftime("%Y-%m-%d %H:%M:%S"))

# Create a menu for workout selection
print("Select a workout:")
print("1. Chest Press")
print("2. Lat Raises")
print("3. Shoulder Press")
print("4. Bicep Curls")
print("5. Pull-Ups")
print("6. Lat Pull-Downs")
print("7. Tricep Pulldowns")
print("8. Forearm Curls")

workout_choice = input("Enter the number of your workout: ")

workout_map = {
    "1": "Chest Press",
    "2": "Lat Raises",
    "3": "Shoulder Press",
    "4": "Bicep Curls",
    "5": "Pull-Ups",
    "6": "Lat Pull-Downs",
    "7": "Tricep Pulldowns",
    "8": "Forearm Curls"
}

if workout_choice in workout_map:
    exercise = workout_map[workout_choice]
    sets = int(input("Enter the number of sets: "))
    reps = int(input("Enter the number of reps: "))
    weight = float(input("Enter the weight (in lb): "))
    add_workout(exercise, sets, reps, weight)
else:
    print("Invalid workout choice.")

# Uncomment the following line to generate random workouts
# generate_random_workouts()

# Print all workouts
#for workout in get_workouts():
    #print(workout)

# Close the connection when done
conn.close()
