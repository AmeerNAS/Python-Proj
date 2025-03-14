import json
import os
from datetime import datetime

#TODO: make db standalone and import it in habit rather than the other way around.
#TODO: updateHabit has O(n) try to find better algo.
class Database:

    #Class costructor
    def __init__(self, filename=None):
        self.filename = filename if filename else os.getcwd() + "\\app\\main.json"
        self.db_schema = {
            "database": self.filename,
            "tables": {
                "habit": [],
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
         
    def getNextID(self):
        """Calculates the highest habit ID and returns it"""
        #GPT first instance error solution:
        db_data = self.loadDB() 
        if not db_data["tables"]["habit"]:
            return 0
        return max(habit["id"] for habit in db_data["tables"]["habit"]) + 1
    
    def addHabit(self, name, desc, type, check_record=[], id=None):
        """ Creates a new habit entry """
        #ensures unique names, might revert it
        if self.getHabitByName(name):
            print(f"Error: Habit '{name}' already exists!")
            raise ValueError

        habit_id = id or self.getNextID()
        new_habit = {
            "id": habit_id,
            "name": name,
            "desc": desc,
            "interval": type,
            "check_record": check_record
        }
        self.db["tables"]["habit"].append(new_habit)
        self.saveDB()
        return habit_id

    #database crawllers
    def getHabitByName(self, name):
        """ Returns list of habits with the specified name (handle as list even if there is only one entry) """
        return [habit for habit in self.db["tables"]["habit"] if habit["name"] == name]
    
    def getHabitByID(self, habit_id: int):
        """Returns a habit by its ID."""
        for habit in self.db["tables"]["habit"]:
            if int(habit["id"]) == habit_id:
                return habit
        return None

    def updateHabit(self, habit_json):
        """Ensures habit is updated in-place and saves to the database."""
        for index, habit in enumerate(self.db["tables"]["habit"]):
            if habit["id"] == habit_json["id"]:
                self.db["tables"]["habit"][index]= habit_json
                print(f"Updated Habit {habit_json["id"]}: {self.db['tables']['habit'][index]}")
                self.saveDB()  # ✅ Ensure it writes to `main.json`
                return True
        return False
        # TODO: finish up the empty functions

    def deleteHabit(self, habit_id):
        """Deletes a habit by its ID."""
        habit_id = int(habit_id)
        self.db["tables"]["habit"] = [habit for habit in self.db["tables"]["habit"] if int(habit["id"]) != habit_id]
        self.saveDB()
    
    def get_seed_data(self):
        pass
