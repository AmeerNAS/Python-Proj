from flask import Flask, render_template, jsonify, request, redirect, url_for
from app.analytics import *
from app import app
from app import Database

@app.route('/')
@app.route('/index')
def index(): 
    """Main page that displays habits and analytics plots."""
    db_manager = Database()
    data = db_manager.db["tables"]["habit"]

    habits = [Habit.fromJSON(h) for h in data]  # Convert JSON data into Habit objects
    
    plot_long = plotLongestStreaks(habits)
    weekly = plotProgress(habits)
    
    return render_template(
        "index.html",
        habits_weekly=filterHabits(habits, interval="WEEKLY"),
        habits_daily=filterHabits(habits, interval="DAILY"),
        plot_weekly_prog=weekly, 
        plot_long=plot_long
    )


@app.route('/creator', methods=['GET', 'POST'])
def create_habit():
    """Handles habit creation form and API requests."""
    db_manager = Database()
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            name = data.get('name')
            desc = data.get('desc', '')  # Default to empty if not provided
            interval = data.get('interval').upper()
        else:
            name = request.form.get('name')
            desc = request.form.get('desc', '')
            interval = request.form.get('interval').upper()

        # Validate required fields
        if not name or not interval:
            return jsonify({"error": "Habit name and interval are required!"}), 400

        try:
            habit_id = db_manager.addHabit(name=name, desc=desc, interval=interval)
            
            #f it's a JSON request
            if request.is_json:
                return jsonify({"message": "Habit created successfully!", "habit_id": habit_id}), 201
            
            #redirect to new habit page
            return redirect(url_for('habit', habit_id=habit_id))
        
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    # Handle GET request: Show the form for creating a habit
    return render_template('creator.html')


@app.route('/habit/<int:habit_id>') 
def habit(habit_id): 
    """Displays habit details."""
    db_manager = Database()
    habit_data = db_manager.getHabitByID(habit_id)
    
    if not habit_data:
        return "Habit not found", 404

    habit = Habit.fromJSON(habit_data)
    current_streak, longest_streak = habit.getStreaks()

    return render_template(
        "habit.html",
        habit=habit,
        longest_streak=longest_streak,
        current_streak=current_streak
    )

@app.route("/api/habits")
def get_habits():
    """Fetch habits with optional filters (interval & min_streak)."""
    db_manager = Database()
    habit_dicts = db_manager.db["tables"]["habit"]  # Get raw habit data (as dicts)

    habits = [Habit.fromJSON(h) for h in habit_dicts]  

    # Get filter params
    name = request.args.get("search", None)
    interval = request.args.get("interval", None)
    min_streak = request.args.get("streak", type=int, default=0)

    #apply filtering
    filtered_habits = filterHabits(habits=habits, name=name, interval=interval, min_streak=min_streak)

    formatted_habits = [
        {
            "id": habit.habit_id,
            "name": habit.name,
            "desc": habit.desc,
            "interval": habit.interval,
            "streak": habit.getStreaks("l") #inshallah it works 
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
    db_manager = Database()
    data = request.get_json()  # Ensure JSON data is received
    is_checked = data.get("checked", False)

    print(f"🔄 Received POST for habit {habit_id} with checked: {is_checked}")  # Debugging  

    habit_data = db_manager.getHabitByID(habit_id)  
    if not habit_data:
        print(f"❌ Habit {habit_id} not found!")
        return jsonify({"error": "Habit not found"}), 404

    habit = Habit.fromJSON(habit_data)  # Convert JSON to Habit object

    if is_checked:
        habit.checkOff()  #This should add today's date to history
        print(f"✅ Habit {habit.habit_id} checked off - New check_record: {habit.getLastStreak()}")
    else:
        habit.uncheckOff()  #This should remove today's date
        print(f"✅ Habit {habit.habit_id} unchecked - Updated check_record: {habit.getLastStreak()}")

    # ✅ Save the updated habit to the database

    #db_manager.updateHabit(habit_id=habit.habit_id, name=habit.name, desc= habit.desc, interval=habit.interval)  
    #db_manager.saveDB()
    print(db_manager.getNextID())
    return jsonify({"success": True, "check_record": habit.getLastStreak()})
