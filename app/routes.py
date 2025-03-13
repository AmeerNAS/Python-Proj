from flask import Flask, render_template, jsonify, request, redirect, url_for
from app.analytics import *
from app import app
from app import db_manager

@app.route('/')
@app.route('/index')
def index(): 
    data = db_manager.db["tables"]["habit"]
    
    new_list=[]
    for h in data:
        new_habit = Habit.fromJSON(h)
        new_list.append(new_habit)
    plot_long = plotLongestStreaks(new_list)
    weekly=plotWeeklyProgress(new_list)
    return render_template(
        "index.html",
        plot_weekly_prog=weekly, 
        plot_long=plot_long)

@app.route("/check-off/<int:habit_id>", methods=["POST"])
def check_off(habit_id):
    """Marks a habit as completed for today."""
    data = db_manager.db["tables"]["habit"]
    for habit in data:
        if habit["id"] == habit_id:
            habit["checked"] = True  # Simulate marking it done
            break
    return jsonify({"success": True, "habit_id": habit_id})

