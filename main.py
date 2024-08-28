import sqlite3
from datetime import datetime

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
def add_workout(exercise, sets, reps, weight):
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

# Create a menu for workout selection
print("Select a workout:")
print("1. Bench Press")
print("2. Squat")
print("3. Deadlift")
print("4. Overhead Press")
print("5. Barbell Row")

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

# Print all workouts
#for workout in get_workouts():
    #print(workout)

# Close the connection when done
conn.close()
