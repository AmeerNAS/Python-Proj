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
    
    def isBroken(self):
        """Checks if the habit is broken by detecting when the last check-in was."""
        if not self.check_record:
            return True  # No check-ins means the habit is broken
        
        last_check = datetime.strptime(self.check_record[-1], '%Y-%m-%d').date()
        today = datetime.today().date()

        # Determine allowed gap based on habit interval
        interval_days = {"daily": 1, "weekly": 7, "monthly": 30}.get(self.interval, 1)
        
        return (today - last_check) > timedelta(days=interval_days)

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

