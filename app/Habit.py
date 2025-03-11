from datetime import datetime, timedelta
from db import Database
from analytics import Analytics


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
        """ Marks the habit as completed for the given date."""
        date = date if date else datetime.today().strftime('%Y-%m-%d')

        if date in self.check_record:
            print(f"Warning: Habit already checked off on {date}.")
            return False  # Avoid duplicates

        self.check_record.append(date)
        return True
    
    def isbroken(self):
        """ Checks if the habit has been 'broken' by detecting when was the last check in comparison to the current date.
        :return: False | True
        :rtype: Boolean
        """
        lastcheck = datetime.date(datetime.strptime(self.check_record[-1], '%Y-%m-%d'))
        today = datetime.date(datetime.today())
        if (self.interval) == "daily":
            x = 1
        elif (self.interval) == "weekly":
            x = 7
        else: 
            x = 30

        print(today - lastcheck)
        if today - lastcheck <= timedelta(days=x):
            return False
        return True

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
            return f"Habit ({self.id}, {self.name}, desc: {self.desc},\n {self.interval}," # streak= {self.getStreak()}, longest Streak= {self.longest_streak} )"
        return f"Habit id={self.id}, name={self.name}, interval={self.interval}," # streak= {self.getStreak()}, longest Streak= {self.longest_streak} )"

