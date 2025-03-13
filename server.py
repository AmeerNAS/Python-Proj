from flask import Flask, render_template
from app.analytics import *

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index(): 
    habits = [
        {"id": "0", "name": "Workout", "desc": "", "interval": "daily", "check_record": ["2025-03-01", "2025-03-02", "2025-03-03"]},
        {"id": "1", "name": "Read", "desc": "", "interval": "daily", "check_record": ["2025-02-25", "2025-02-26", "2025-02-28"]},
        {"id": "2", "name": "Coding", "desc": "", "interval": "weekly", "check_record": ["2025-02-18", "2025-02-25", "2025-03-04"]},
    ]
    new_list=[]
    for h in habits:
        new_habit = Habit.fromJSON(h)
        new_list.append(new_habit)
    plot_long = plotLongestStreaks(new_list)
    return render_template("index.html", plot_long=plot_long)

app.run(host="0.0.0.0", port=8000)

