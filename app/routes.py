from flask import Flask, render_template, jsonify, request, redirect, url_for
from app.analytics import *
from app import app
from app import db_manager

@app.route('/')
@app.route('/index')
def index(): 
    data = db_manager.db["tables"]["habit"]
    
    habits=[]
    for h in data:
        new_habit = Habit.fromJSON(h)
        habits.append(new_habit)
    plot_long = plotLongestStreaks(habits)
    weekly=plotWeeklyProgress(habits)
    return render_template(
        "index.html",
        habits_weekly=filterHabits(habits, "weekly"),
        habits_daily=filterHabits(habits, "daily"),
        plot_weekly_prog=weekly, 
        plot_long=plot_long)

""" @app.route("/check-off/<int:habit_id>", methods=["POST"])
def check_off(habit_id):
    ""Marks a habit as completed for today.""
    data = db_manager.db["tables"]["habit"]
    for habit in data:
        if habit["id"] == habit_id:
            habit["checked"] = True  # Simulate marking it done
            break
    return jsonify({"success": True, "habit_id": habit_id}) """

@app.route('/habit/<habit_id>') 
def habit(habit_id): 
    # If sport is cricket call the view function for  
    # same and pass team name 
    if db_manager.getHabitByID(id): 
        return redirect(url_for(habit_id=habit_id)) 
    else:
        return "Record not found", 400

@app.route('/habits', methods=["GET"])
def habits():
    data = db_manager.db["tables"]["habit"]
    habits_list= [Habit.fromJSON(d) for d in data]
        
    return render_template("all_habits.html", habits_list=habits_list)


@app.route('/add', methods=['POST']) 
def add():

    if request.is_json:
        data = request.form
        print(data)
        habit_dict = data
        db_manager.addHabit(habit_dict)
        return redirect(url_for('index'))
    else:
        pass
@app.route('/check/<habit_id>')
def check(habit_id):
    habit_id = request.form.values
    habit_dict = db_manager.getHabitByID(habit_id)
    habit = Habit.fromJSON(habit_dict)
    habit.checkOff()
    return redirect(url_for("index"))
    