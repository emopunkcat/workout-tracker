from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, date as date_class

app = Flask(__name__)

@app.route('/')
def view_workouts():
    conn = sqlite3.connect('workout_stats.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workouts ORDER BY date')
    workouts = cursor.fetchall()
    conn.close()

    # Prepare data for charts
    chart_data = {}
    for workout in workouts:
        date, exercise, sets, reps, weight = workout[1][:10], workout[2], workout[3], workout[4], workout[5]
        if exercise not in chart_data:
            chart_data[exercise] = {'dates': [], 'weights': []}
        chart_data[exercise]['dates'].append(date)
        chart_data[exercise]['weights'].append(weight)

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
        first_day = date_class(year, month, 1).weekday()
        first_days.append((first_day + 1) % 7)  # Adjust to make Sunday 0 and Saturday 6

    # Pass this to your template along with other data
    return render_template('workouts.html', workouts=workouts, workout_dates=workout_dates, 
                           first_days=first_days, chart_data=chart_data)

def custom_strftime(value, format='%Y-%m-%d'):
    return datetime.strptime(value, '%Y-%j').strftime(format)

app.jinja_env.filters['custom_strftime'] = custom_strftime

@app.route('/add_workout', methods=['POST'])
def add_workout():
    exercise = request.form['exercise']
    sets = int(request.form['sets'])
    reps = int(request.form['reps'])
    weight = float(request.form['weight'])
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('workout_stats.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO workouts (date, exercise, sets, reps, weight)
    VALUES (?, ?, ?, ?, ?)
    ''', (date, exercise, sets, reps, weight))
    conn.commit()
    conn.close()

    return redirect(url_for('view_workouts'))

if __name__ == '__main__':
    app.run(debug=True)