import json
import os
from datetime import datetime

#TODO: make db standalone and import it in habit rather than the other way around.
#TODO: updateHabit has O(n) try to find better algo.
    
class Database:
    """Initializes and manages the database"""
    
    VALID_INTERVALS = {"DAILY", "WEEKLY"}
    def __init__(self, filename=None):
        self.filename = filename if filename else os.getcwd() + "\\app\\main.json"
        self.db_schema = {
            "database": self.filename,
            "tables": {
                "habit": [],
                "history": []  # Replaces `history`
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
        """Creates a new habit entry in the database."""
        
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
        """Returns the next available habit ID."""
        db_data = self.loadDB()
        if not db_data["tables"]["habit"]:
            return 0
        return max(habit["id"] for habit in db_data["tables"]["habit"]) + 1
    
    
    def getHabitByName(self, name):
        """Returns a list of habits matching the name."""
        return [habit for habit in self.db["tables"]["habit"] if habit["name"] == name]


    def getHabitByID(self, habit_id):
        """Returns a habit by its ID."""
        for habit in self.db["tables"]["habit"]:
            if int(habit["id"]) == habit_id:
                return habit
        return None


    # Deleters
    # ++++++++
    def deleteHabit(self, habit_id):
        """Deletes a habit and its history."""
        habit_id = int(habit_id)
        self.db["tables"]["habit"] = [habit for habit in self.db["tables"]["habit"] if int(habit["id"]) != habit_id]
        self.db["tables"]["history"] = [record for record in self.db["tables"]["history"] if int(record["habit_id"]) != habit_id]
        self.saveDB()

    
    def deleteHistory(self, habit_id: int, date: str) -> bool:
        """Removes a specific habit record from history by habit_id and date."""
        initial_length = len(self.db["tables"]["history"])

        #filter 
        self.db["tables"]["history"] = [
            record for record in self.db["tables"]["history"]
            if not (record["habit_id"] == habit_id and record["date"] == date)
        ]

        if len(self.db["tables"]["history"]) < initial_length:
            self.saveDB()
            return True  # Successfully deleted

        return False
    
    
    # Updaters
    # ++++++++
    
    def updateHabit(self, habit_id: int, name: str = None, desc: str = None, interval: str = None) -> bool:
        """Updates an existing habit's attributes while maintaining efficiency."""
        
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

        print(f"Warning: Habit with ID {habit_id} not found.")
        return False 

    def updateHistory(self, habit_id: int, date: str, new_streak: int, new_status: str) -> bool:
        """Updates an existing history record with new streak and status."""
        
        for record in self.db["tables"]["history"]:
            if record["habit_id"] == habit_id and record["date"] == date:
                record["streak"] = new_streak
                record["status"] = new_status
                self.saveDB()
                return True  # Successfully updated

        print(f"Warning: No matching history record found for habit ID {habit_id} on {date}.")
        return False
    

    
    
    
    #External
    def get_seed_data(self):
        pass
