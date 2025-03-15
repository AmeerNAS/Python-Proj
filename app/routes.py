from flask import Flask, render_template, jsonify, request, redirect, url_for
from app.analytics import *
from app import app
from app import db_manager

@app.route('/')
@app.route('/index')
def index(): 
    """Main page that displays habits and analytics plots."""
    data = db_manager.db["tables"]["habit"]

    habits = [Habit.fromJSON(h) for h in data]  # Convert JSON data into Habit objects
    
    plot_long = plotLongestStreaks(habits)
    weekly = plotWeeklyProgress(habits)
    
    return render_template(
        "index.html",
        habits_weekly=filterHabits(habits, interval="weekly"),
        habits_daily=filterHabits(habits, interval="daily"),
        plot_weekly_prog=weekly, 
        plot_long=plot_long
    )


@app.route('/creator', methods=['GET', 'POST'])
def create_habit():
    """Handles habit creation form."""
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')
        interval = request.form.get('interval')

        if not name or not interval:
            return "Habit name and interval are required!", 400

        try:
            habit_id = db_manager.addHabit(name, desc, interval, check_record=[])
            return redirect(url_for('habit', habit_id=habit_id))  # Redirect to habit details
        except ValueError:
            return "A habit with this name already exists.", 400

    return render_template('creator.html')

@app.route('/habit/<int:habit_id>') 
def habit(habit_id): 
    """Displays habit details."""
    habit_data = db_manager.getHabitByID(habit_id)
    
    if not habit_data:
        return "Habit not found", 404

    habit = Habit.fromJSON(habit_data)
    longest_streak, current_streak = getStreak(habit, "both")

    return render_template(
        "habit.html",
        habit=habit,
        longest_streak=longest_streak,
        current_streak=current_streak
    )

@app.route("/api/habits")
def get_habits():
    """Fetch habits with optional filters (interval & min_streak)."""
    habit_dicts = db_manager.db["tables"]["habit"]  # Get raw habit data (as dicts)

    # ✅ Convert dictionaries to Habit objects
    habits = [Habit.fromJSON(h) for h in habit_dicts]  

    # Get filter parameters
    name = request.args.get("search", None)
    interval = request.args.get("interval", None)
    min_streak = request.args.get("streak", type=int, default=0)

    # ✅ Apply filtering with real Habit objects
    filtered_habits = filterHabits(habits=habits, name=name, interval=interval, min_streak=min_streak)

    # ✅ Convert Habit objects back to dictionaries for JSON response
    formatted_habits = [
        {
            "id": habit.id,
            "name": habit.name,
            "desc": habit.desc,
            "interval": habit.interval,
            "streak": getStreak(habit, "long")  # ✅ getStreak works now!
        }
        for habit in filtered_habits
    ]
    return jsonify(formatted_habits)

@app.route("/habits")
def habit_list():
    return render_template("habits.html")

@app.route("/check/<int:habit_id>", methods=["POST"])
def check(habit_id):
    """Toggle the check-off state of a habit."""
    data = request.get_json()  # Ensure JSON data is received
    is_checked = data.get("checked", False)

    print(f"🔄 Received POST for habit {habit_id} with checked: {is_checked}")  # Debugging  

    habit_data = db_manager.getHabitByID(habit_id)  
    if not habit_data:
        print(f"❌ Habit {habit_id} not found!")
        return jsonify({"error": "Habit not found"}), 404

    habit = Habit.fromJSON(habit_data)  # Convert JSON to Habit object

    if is_checked:
        habit.checkOff()  # ✅ This should add today's date to `check_record`
        print(f"✅ Habit {habit.id} checked off - New check_record: {habit.check_record}")
    else:
        habit.uncheckOff()  # ✅ This should remove today's date
        print(f"✅ Habit {habit.id} unchecked - Updated check_record: {habit.check_record}")

    # ✅ Save the updated habit to the database
    db_manager.updateHabit(habit.toJSON())  
    db_manager.saveDB()

    return jsonify({"success": True, "check_record": habit.check_record})
