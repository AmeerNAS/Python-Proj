from datetime import datetime, timedelta
from app.db import Database

class Habit:
    """ Habits class """   

    def __init__(self, id: int, name: str, desc: str, interval: str, check_record=None, current_streak=0, longest_streak=0):
        
        # Basic data initialization
        #could potentially be replaced with more efficient solution

        self.id = id
        self.name = name
        self.desc = desc
        self.interval = interval
        self.current_streak = current_streak
        self.longest_streak = longest_streak

        # check-off dates record list
        self.check_record = check_record if isinstance(check_record, list) else []

    #Check-off function: takes current date and appends it to check_record list then computes streak.
    def checkOff(self, date=None):
        """ Marks the habit as completed for the given date."""
        date = date if date else datetime.today().strftime('%Y-%m-%d')

        # recurring execute check
        if date in self.check_record:
            print(f"Warning: Habit already checked off on {date}.")
            return False  # Avoid duplicates

        self.check_record.append(date)
        db = Database()
        db.updateHabit(self.toJSON())
        return True
    
    def uncheckOff(self, date=None):
        """checkOff reverser"""
        date = date if date else datetime.today().strftime('%Y-%m-%d')
         
        if date in self.check_record:
            self.check_record.remove(date)
            return True
        return False
    
    def isChecked(self):
        """Checks if the habit is broken by detecting when the last check-in was."""
        if not self.check_record:
            return True  # No check-ins means the habit is broken
        
        last_check = datetime.strptime(self.check_record[-1], '%Y-%m-%d').date()
        today = datetime.today().date()

        # Determine allowed gap based on habit interval
        interval_days = {"daily": 1, "weekly": 7, "monthly": 30}.get(self.interval, 1)
        
        return (today - last_check) > timedelta(days=interval_days)

    @staticmethod
    def fromJSON(data: dict[str, any]):
        """ Creates a Habit object from JSON data """
        return Habit(
            id = int(data["id"]),
            name = data["name"],
            desc = data["desc"],
            interval = data["interval"],
            #check_record=database["check_record"]
            check_record=data.get("check_record", [])
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

