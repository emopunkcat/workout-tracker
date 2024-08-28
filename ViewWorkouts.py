from flask import Flask, render_template
import sqlite3
from datetime import datetime, date

app = Flask(__name__)

@app.route('/')
def view_workouts():
    conn = sqlite3.connect('workout_stats.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workouts')
    workouts = cursor.fetchall()
    conn.close()

    # Assuming workouts is your original data
    workout_dates = set()
    for workout in workouts:
        date_str = workout[1][:10]  # Assuming the date is the second item in each workout tuple
        workout_dates.add(date_str)

    # Convert to a list and sort
    workout_dates = sorted(list(workout_dates))

    # Calculate the first day of each month
    first_days = []
    year = int(workouts[0][1][:4])  # Get the year from the first workout
    for month in range(1, 13):
        first_day = date(year, month, 1).weekday()
        first_days.append((first_day + 1) % 7)  # Adjust to make Sunday 0 and Saturday 6

    # Pass this to your template along with other data
    return render_template('workouts.html', workouts=workouts, workout_dates=workout_dates, first_days=first_days)

if __name__ == '__main__':
    app.run(debug=True)