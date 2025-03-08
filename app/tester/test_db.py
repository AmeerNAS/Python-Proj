from db import Database

class testDB:
    def startup_method(self):
        pass
    
    def testCode(self):
        db = Database()
        #habit creation
        
        db.addHabit("example_habit", "This is a test habit", "daily")
        print(db.getHabitByName("example_habit"))
        
        print("++++++++++++++++") 

        #for updating
        db.addHabit("update_habit", "This habit is unupdated", "daily", id=2)
        data_to_update = db.getHabitByID(2)
        data_to_update["desc"] = "this habit has been updated"
        db.updateHabit(data_to_update)
        return 0

    def teardown_method(self):
        self.testCode()