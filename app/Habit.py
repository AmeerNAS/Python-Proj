from datetime import datetime, timedelta
from db import *


class Habit:   

    def __init__(self, id, name, desc, interval, check_record=[]):
        
        # Basic data initialization
        #could potentially be replaced with more efficient solution


        self.name = name
        self.desc = desc
        self.interval = interval
        self.longest_streak = 0
        self.current_streak = 0

        # check-off dates record list
        self.check_record = check_record

    #Check-off function: takes current date and appends it to check_record list then computes streak.
    def checkOff(self, date=None):
        """ Checks off the habit based on its interval type """
        if not date:
            date = datetime.today().strftime('%Y-%m-%d')

        if date not in self.check_record:  
            self.check_record.append(date)
        return True

    #Prof. compute streak method
    def getStreak(self):
        #Sort the check record and creates temp clone
        sorted_dates = sorted(self.check_record)

        #No records handling:
        if not sorted_dates:
            self.longest_streak = 0
            return

        #variable initialization
        temp_c = 1    

        for i in range(1, len(sorted_dates)):
            if sorted_dates[i] -sorted_dates[i-1]==timedelta(days=1):
                temp_c += 1
                self.longest_streak = max(self.longest_streak, temp_c)
            else:
                temp_c = 1

        self.current_streak = temp_c

    def editHabit(self, variable, newVariable):
        database = Database()
        habit_data = database.getHabitByID(self.id)
        for var in habit_data:
            if var == variable:
                var = newVariable
        database.saveDB()

    def toDict(self):
        habit_to_dict = {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "interval": self.interval,
            "check_record": self.check_record
        }
        return habit_to_dict

        

""" Test
test = Habit("update","test habit for updating","daily")
test.editHabit("name", "updated")

habit = Habit("test", "test habit", "daily")
print(habit.id) 
"""

