""" 
Database Model in JSON
"""

# Imports 
import json
import os
from datetime import datetime, timedelta

#used in getSeedData()    
import random


#TODO: updateHabit has O(n) try to find better algo.
    
class Database:
    """
    Initializes and manages JSON database with curated methods that allow for seamless querying and loading
    
    :param str filename: Controls the name of the database file which the databse will load/save to
    and allows for interswitches if requested.
    
    :return: Database Manager Object
    :rtype: Database
    """
    
    # Interval Validator 
    VALID_INTERVALS = {"DAILY", "WEEKLY"}
    def __init__(self, filename=None):
        """ 
        :param str filename: Controls the name of the database file which the databse will load/save to
            and allows for interswitches if requested.
            
        :return: Databse manager object
        :rtype: Database
        """
        self.filename = filename if filename else os.getcwd() + "\\app\\main.json"
        self.db_schema = {
            "database": self.filename,
            "tables": {
                "habit": [],
                "history": []
            }
        }
        self.db = self.loadDB()

    def saveDB(self):
        """Saves the current database state to a JSON file."""
        with open(self.filename, "w") as f:
            json.dump(self.db, f, indent=4)

    def loadDB(self):
        """Loads the database from the file, or initializes if missing."""
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            self.db = self.db_schema
            self.saveDB()
            return self.db


    # Adders
    # ++++++
    def addHabit(self, name, desc, interval, id=None):
        """
        Creates a new habit entry in the database.
        \
        :param str name:
            The name to be used to save the habit under
            
        :param str desc:
            A small description descripting the habit in finer definition
            
        :param str interval:
            The habit's interval of periodicity.

                - "DAILY": for daily habits 
                - "WEEKLY": for weekly habits
            
        :param int (optional) id:
            None | allows the slection of a specific id to be used for adding data, otherwise generates id based on getNextID()
            
            
        :return: habit id | For implementation if the user needs a reference after creation
        :rtype: int
        
        :raises ValueError: If the habit already exists or the iterval is not apart of the accepted enum strings
        """
        
        #name check
        if self.getHabitByName(name):
            raise ValueError(f"Error: Habit '{name}' already exists!")
        
        #interval check
        if interval not in self.VALID_INTERVALS:
            raise ValueError(f"{interval}': must be " + ", ".join(self.VALID_INTERVALS))
        
        #adder
        habit_id = id or self.getNextID()
        new_habit = {
            "id": habit_id,
            "name": name,
            "desc": desc,
            "interval": interval
        }
        self.db["tables"]["habit"].append(new_habit)
        self.saveDB()
        return habit_id
    
    
    def addHistory(self, habit_id: int, streak: int, status: str, date: str):
        """
        Adds a history entry for a habit.

        :param int habit_id:
            The unique identifier of the habit for which the history is being recorded

        :param int streak:
            The streak count at the time of the recorded history entry

        :param str status:
            The status of the habit at the recorded date.

                - "active": The habit is still being maintained
                - "broken": The habit streak was interrupted

        :param str date:
            The date of the history entry in YYYY-MM-DD format

        :return: True if the history entry was successfully added
        :rtype: bool
        """
        
        self.db["tables"]["history"].append({
            "habit_id": habit_id,
            "streak": streak,
            "status": status,
            "date": date
        })
        
        self.saveDB()
        return True
    
    
    # Getters
    # +++++++
    def getNextID(self):
        """Returns the next available habit ID. Used for attaining appropraite habit id in addHabit()"""
        db_data = self.loadDB()
        if not db_data["tables"]["habit"]:
            return 0
        return max(habit["id"] for habit in db_data["tables"]["habit"]) + 1
    
    
    def getHabitByName(self, name):
        """Returns a list of habits matching the name.
        
        :param str name: specified habit name to be used for querying
        
        :return: Habit(s) under that name
        :rtype: list[Habit]"""
        return [habit for habit in self.db["tables"]["habit"] if habit["name"] == name]


    def getHabitByID(self, habit_id) -> dict[str, any]:
        """Returns a habit by its ID.
        
        :param str name: specified habit name to be used for querying
        
        :return: Habit's JSON data
        :rtype: dict[str, any]"""
        for habit in self.db["tables"]["habit"]:
            if int(habit["id"]) == habit_id:
                return habit
        return None


    # Deleters
    # ++++++++
    def deleteHabit(self, habit_id):
        """
        Deletes a habit and its history.
        
        :param int habit_id: specified habit id to be used for querying
        
        :return: True if successful | False & Error message if unsuccessful
        :rtype: bool | tuple(bool, str)"""
        habit_id = int(habit_id)
        try:
            self.db["tables"]["habit"] = [habit for habit in self.db["tables"]["habit"] if int(habit["id"]) != habit_id]
            self.db["tables"]["history"] = [record for record in self.db["tables"]["history"] if int(record["habit_id"]) != habit_id]
            self.saveDB()
        except Exception as e:
            return False, e
        return True

    
    def deleteHistory(self, habit_id: int, date: str) -> bool:
        """Removes a specific habit record from history by habit_id and date.
        
        :param int habit_id: specified habit id to be used for querying
        :param str date: the date of the particular history entry for querying
        
        :return: True if successful | False if unsuccessful
        :rtype: bool """
        initial_length = len(self.db["tables"]["history"])

        #filter 
        self.db["tables"]["history"] = [
            record for record in self.db["tables"]["history"]
            if not (record["habit_id"] == habit_id and record["date"] == date)
        ]

        if len(self.db["tables"]["history"]) < initial_length:
            self.saveDB()
            return True 

        return False
    
    
    # Updaters
    # ++++++++
    
    def updateHabit(self, habit_id: int, name: str = None, desc: str = None, interval: str = None) -> bool:
        """Updates an existing habit's attributes while maintaining efficiency.
        
        :param int habit_id: specified habit id to be used for querying
        :param str name: the new name of the habit entry for updating
        :param str desc: the new desc of the habit entry for updating
        :param str interval: the new interval type of the habit entry for updating
        
        :return: True if successful | False if unsuccessful
        :rtype: bool """
        
        for habit in self.db["tables"]["habit"]:
            if habit["id"] == habit_id:
                if name:
                    habit["name"] = name
                if desc:
                    habit["desc"] = desc
                if interval:
                    if interval not in self.VALID_INTERVALS:
                        raise ValueError(f"Invalid interval '{interval}'. Must be one of: {', '.join(self.VALID_INTERVALS)}")
                    habit["interval"] = interval
                self.saveDB()
                print(name + " updated") # !
                return True 

        print(f"Warning: Habit with ID {habit_id} not found.") # !
        return False 

    def updateHistory(self, habit_id: int, date: str, new_streak: int, new_status: str) -> bool:
        """Updates an existing history record with new streak and status. (!DNU)
        
        :param int habit_id: specified habit id to be used for querying for the habit
        :param str date: the new name of the history entry for updating
        :param int new_streak: the new streak of the hsitory entry for updating
        :param str new_status: the new status type of the history entry for updating
        
        :return: True if successful | False if unsuccessful
        :rtype: bool """
        
        for record in self.db["tables"]["history"]:
            if record["habit_id"] == habit_id and record["date"] == date:
                record["streak"] = new_streak
                record["status"] = new_status
                self.saveDB()
                return True

        print(f"Warning: No matching history record found for habit ID {habit_id} on {date}.")
        return False


    #External (found online) 
    def get_seed_data(self):
        """
        Populates the database with 10 sample habits and 4+ weeks of history for testing.
        
        :return: Populates Database main file however does not retune any real data.
        """
        sample_habits = [
            ("Morning Run", "Go for a 30-minute run every morning", "DAILY"),
            ("Reading", "Read at least 10 pages of a book", "DAILY"),
            ("Meditation", "Meditate for 10 minutes", "DAILY"),
            ("Workout", "Complete a full-body workout", "DAILY"),
            ("Drink Water", "Drink 2L of water", "DAILY"),
            ("Journal", "Write a journal entry", "DAILY"),
            ("Guitar Practice", "Practice guitar for 30 minutes", "DAILY"),
            ("Meal Prep", "Prepare healthy meals", "WEEKLY"),
            ("Budgeting", "Track expenses for the week", "WEEKLY"),
            ("Home Cleaning", "Clean the house thoroughly", "WEEKLY")
        ]

        # Add habits
        for name, desc, interval in sample_habits:
            habit_id = self.addHabit(name, desc, interval)

            # Generate History
            start_date = datetime.today() - timedelta(weeks=4)
            streak = 0
            for i in range(20 + random.randint(0, 7)):
                date_str = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")

                # Introduce random habit breaks
                if random.random() > 0.85: 
                    continue

                if random.random() > 0.9: 
                    status = "broken"
                    streak = 0 
                else:
                    status = "active"
                    streak += random.choice([1, 1, 1, 2])

                self.addHistory(habit_id, streak, status, date_str)

        self.saveDB()
        print("Seed data added successfully.")

        # for Flask
        return {"status": "success", "redirect": "/main"}
