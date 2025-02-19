from datetime import datetime, timedelta


class Habit:   

    def __init__(self, id, name, desc, interval, check_record=[]):
        
        # Basic data initialization
        #could potentially be replaced with more efficient solution

        self.id = id
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
        return self.current_streak

    """     
    def editHabit(self, variable, newVariable):
        database = Database()
        habit_data = database.getHabitByID(self.id)
        if habit_data:
            print("Edit failed, Hbit object was not found")
        else:
            for var in habit_data:
                if var == variable:
                    var = newVariable
            database.saveDB() 
    """

    @staticmethod
    def fromJSON(data):
        """ Creates a Habit object from JSON data """
        return Habit(
            id = data["id"],
            name = data["name"],
            desc = data["desc"],
            interval = data["interval"],
            #check_record=database["check_record"]
            check_record=data.get["check_record", []]
        )

    def toJSON(self):
        """ Translates the Habit object into JSON """
        habit_to_dict = {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "interval": self.interval,
            "check_record": self.check_record
        }
        return habit_to_dict

    def toString(self, withDesc=False):
        """ Habit object to string converter """
        if (withDesc):
            return f"Habit ({self.id}, {self.name}, desc: {self.desc},\n {self.interval}, streak= {self.getStreak()}, longest Streak= {self.longest_streak} )"
        return f"Habit id={self.id}, name={self.name}, interval={self.interval}, streak= {self.getStreak()}, longest Streak= {self.longest_streak} )"


""" 
# Test
test = Habit(1, "update","test habit for updating","daily")
#test.editHabit("name", "updated")

habit = Habit(2, "test", "test habit", "daily")
print(test.id) 
print(habit.toString()) 
"""