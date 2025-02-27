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
        for habit in self.db["tables"]["habit"]:
            if habit["id"] == id:
                return habit
        #return [habit for habit in self.db["tables"]["habit"] if habit["id"] == id]

    def markComplete(self, iD, markDate=None):
        """ Handles appending a new completion date to a speciiified habit using its id """
        
        if not markDate:
            markDate = datetime.today().strftime('%Y-%m-%d')
        """ 
        if not eventTime:
            eventTime = datetime.now().strftime('%H:%M:%S') 
        
        self.getHabitByID(id)["completion dates"].append(eventDate)
        """
        for habit in self.db["tables"]["habit"]:
            if habit["id"] == iD:
                habit["check_record"].append(markDate)
                self.saveDB()
                return True
        return False

    """ 
    def update_counter_status(db, name, status):
        for counter in db["tables"]["counter"]:
            if counter["name"] == name:
                counter["status"] = status
                saveDB(db)
                return True
        return False 
    """
    def updateHabit(self, changed_habit_data):
        counter = 0
        for habit in self.db["tables"]["habit"]:
            
            if habit["id"] == changed_habit_data["id"]:
                self.db["tables"]["habit"][counter]["name"] = changed_habit_data["name"]
                self.db["tables"]["habit"][counter]["desc"] = changed_habit_data["desc"]
                self.db["tables"]["habit"][counter]["interval"] = changed_habit_data["interval"]
                self.db["tables"]["habit"][counter]["check_record"] = changed_habit_data["check_record"]

                self.saveDB()
                # print("habit updated")
                return 0
            counter+= 1
        return print("habit not found")
        
    """ 
    update_habit test code:
    existing_habit = self.db["tables"]["habit"]
        for i, h in enumerate(existing_habits):
            if h["id"] == habit_data["id"]:
                existing_habits[i] = habit_data 
                self.saveDB()
                return 1
        
        return 0
    #same speed :/
    """

def testCode():
    db = Database()
    #habit creation
    
    db.addHabit("example_habit", "This is a test habit", "daily")
    print(db.getHabitByName("example_habit"))
    print("++++++++++++++++") 
    

    #after marking
    db.markComplete(0)
    print(db.getHabitByID(0))
    print("++++++++++++++++")

    #for updating
    db.addHabit("update_habit", "This habit is unupdated", "daily", id=2)
    data_to_update = db.getHabitByID(2)
    data_to_update["desc"] = "this habit has been updated"
    db.updateHabit(data_to_update)
    return 0


testCode()
