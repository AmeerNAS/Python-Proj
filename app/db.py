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
    
    """ 
    ! OLD CODE
    def __init__(self, filename="main.json"):
        self.filename = filename
        self.db_schema = {
            "database": self.filename,
            "tables": {
                "habit": [],
            }
        }
        self.id_counter=0
        self.db = self.load_db()

    def saveDB(self):
        with open(self.filename, "w") as f:
            json.dump(self.db, f, indent=4)

    def load_db(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            self.saveDB()
            return self.db_schema
    """
    
    def addHabit(self, name, desc, type, check_record=[], id=None):
        """ Creates a new habit entry """
        #ensures unique names, might revert it
        if self.getHabitByName(name):
            print(f"Error: Habit '{name}' already exists!")
            return False

        habit_id = self.getNextID()
        new_habit = {
            "id": id,
            "name": name,
            "description": desc,
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
    
    def getHabitByID(self, id):
        """Returns a habit by its ID."""
        return self.db["tables"]["habit"].get(str(id), None)

    """ 
    def update_counter_status(db, name, status):
        for counter in db["tables"]["counter"]:
            if counter["name"] == name:
                counter["status"] = status
                saveDB(db)
                return True
        return False 
    """

    def updateHabit(self, habit_id, updated_data):
        """Updates specific fields of a habit instead of replacing the whole object. Only fields provided in `updated_data` will be updated. """
        for habit in self.db["tables"]["habit"]:
            if habit["id"] == habit_id:
                habit.update(updated_data)  # Only update given fields
                self.saveDB()
                return True
        return False  # Habit not found
        # TODO: finish up the empty functions

    def deleteHabit(self, habit_id):
        """Deletes a habit by its ID."""
        habit_id = str(habit_id)
        if habit_id in self.db["tables"]["habit"]:
            del self.db["tables"]["habit"][habit_id]
            self.saveDB()
            return True
        return False
    
    def get_seed_data(self):
        pass
