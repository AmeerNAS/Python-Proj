import json
from datetime import datetime

class Database:

    #Class costructor
    def __init__(self, filename="main.json"):
        self.filename = filename
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
    
    def addHabit(self, id, name, desc, type, completions=[]):
        """ Creates a new habit entry """
        if self.getHabitByName(name):
            print(f"Error: Habit '{name}' already exists!")
            return False

        # !!CHANGE TO DICT FUNCTION TO CREATE OBJECT 
        habit_id = self.getNextID()
        new_habit = {
            "id": id,
            "name": name,
            "description": desc,
            "interval": type,
            "completion_dates": completions
        }
        self.db["tables"]["habit"].append(new_habit)
        self.saveDB()
        return habit_id

    #database crawllers
    def getHabitByName(self, name):
        return [habit for habit in self.db["tables"]["habit"] if habit["name"] == name]
    def getHabitByID(self, id):
        for habit in self.db["tables"]["habit"]:
            if habit["id"] == id:
                return habit
        return False
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
                habit["completion dates"].append(markDate)
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

def testCode(self):

    #habit creation
    """ self.add_habit(8, "example_habit", "This is a test habit", "daily")
    print(self.getHabitByName("example_habit"))
    print("++++++++++++++++") """

    #after marking
    self.mark_complete(0)
    print(self.getHabitByID(0))
    print("++++++++++++++++")

#db = Database()
# testCode(db)
