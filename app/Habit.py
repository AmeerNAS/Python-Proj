""" 
Habit Object Oriented Module
Defines Habit as object, requires direct access to db module
"""

# Imports
from datetime import datetime, date

#db access
from app.db import Database

#object creation
from dataclasses import dataclass


@dataclass
class Habit:
    """
    Represents a habit tracked in the system.
    
    :param int habit_id: The key index of the Habit object
    :param str name:    The name of the habit object (short and hints on habit's purpose)
    :param str desc:    The desc of the habit object (for expanding on or help clarifying the habit's purpose)
    :param str interval: The interval of periodicity of the habit object (only accepts 'WEEKLY', 'DAILY', validated by database)
    :param int current_streak: The current streak local save to avoid extensive recalculation (aids in performance for plotting)
    :param int longest_streak: The longest streak local save to avoid extensive recalculation
    
    :return: A new habit entry with access to defauly database queries
    :rtype: Habit
    """
    
    habit_id: int
    name: str
    desc: str
    interval: str
    current_streak: int = 0
    longest_streak: int = 0
    
    def __post_init__(self) -> None:
        """ 
        Post Initialization method.
        \
        Checks database for any history entries and get the habit's current_streak, longest_streak. 
        """
        self.refreshStreaks()
    
    
    # +++++++++
    # Utilities
    
    #Prof. compute streak method improvised
    def getStreaks(self, mode=None):
        """ 
        Calculates streaks without resetting the saved values. 
        
        :param "l" "c" | None mode: 
            - None: Return both streaks (tuple: current, longest).
            - "long": Return longest streak.
            - "c": Return current streak. 
        :return: Current streak or longest streak or both.
        :rtype: int | (int, int)
        """
        db = Database()
        history = [s for s in db.db["tables"]["history"] if s["habit_id"] == self.habit_id]

        if not history:
            return (0, 0) if mode is None else 0
        
        streaks = [record["streak"] for record in history]
        current_streak = streaks[-1] if streaks else 0
        longest_streak = max(streaks) if streaks else 0

        if mode is None:
            return current_streak, longest_streak
        elif mode == "c":
            return current_streak
        elif mode == "l":
            return longest_streak
        else:
            raise ValueError("Invalid mode. Use 'c', 'l', or None.")
        
    def refreshStreaks(self):
        """ intermediatory method for streak values recalculation and asignment"""
        self.current_streak, self.longest_streak = self.getStreaks() 
        
    
    def doesStreakContinue(self, last_date: str | date, current_date: datetime.date = None) -> bool:
        """Checks if the streak continues based on the habit's interval.
        
        :param str | date last_date: 
            The date of the habit's latest check entry
        :param date (optional) current_date:
            None | The date to be checked against, is set to current date if left None
            
        :return: Check reslts for if the habit continues (True) or has been broken (False).
        :rtype: bool
        """
        last_date = self.convertor(last_date) if isinstance(last_date, str) else last_date
        current_date = current_date or datetime.today().date()

        intervals = {"DAILY": 1, "WEEKLY": 7}
        interval_days = intervals.get(self.interval.upper(), 1)  

        return (current_date - last_date).days <= interval_days
        
    
    @staticmethod
    def convertor(date: str):
        """Converts a string date 'YYYY-MM-DD' into a datetime.date object.
        
        :param str date: 
            The date as string type which will be converted.
        
        :return: date as a datetime object.
        :rtype: date
        """
        return datetime.strptime(date, "%Y-%m-%d").date()

    def getLastStreak(self) -> dict | None:
        """Retrieves the last recorded streak for the habit."""
        db = Database()
        streaks = [s for s in db.db["tables"]["history"] if s["habit_id"] == self.habit_id]

        #Empty case
        if not streaks:
            return None 
        return max(streaks, key=lambda s: self.convertor(s["date"]))
    
    def getAllStreaks(self) -> dict | None:
        """Retrieves all recorded streaks for the habit."""
        db = Database()
        streaks = [s for s in db.db["tables"]["history"] if s["habit_id"] == self.habit_id]

        print(streaks)
        #Empty case
        if not streaks:
            return None 
        return streaks
        
    
    
    # ++++++++++++++++++++
    # Check property funcs
        
    def isChecked(self, date: str = None) -> bool:
        """Checks if a habit was completed on a specific date.
        
        :param str (optional) date: 
            The date to be checked for, current date if left None.
            
        :return: The Check for matching check record as date.
        :rtype: bool
        """
        date = date or datetime.today().strftime('%Y-%m-%d')
        db = Database()
        return any(record["habit_id"] == self.habit_id and record["date"] == date for record in db.db["tables"]["history"])
    
    
    def getCheckins(self) -> list[str]:
        """Retrieves all check-in dates sorted.
        
        :return: The list of check in dates connected to habit in the format of '%Y-%m-%d'
        :rtype: list[str]"""
        db = Database()
        dates = [record["date"] for record in db.db["tables"]["history"] if record["habit_id"] == self.habit_id]
        dates.sort()
        return dates
    
    
    def checkOff(self):
        """
        Marks habit as checked for today's date and updates streak history.
        
        :return: True if succeeded | False if failed
        :rtype: bool"""
        db = Database()
        today = datetime.today().strftime("%Y-%m-%d")
        
        if self.isChecked(today):
            print(f"Warning: Habit already checked off on {today}.")
            return False

        last_streak = self.getLastStreak()
        new_streak = 1

        if last_streak:
            if self.doesStreakContinue(last_streak["date"]):
                new_streak = last_streak["streak"] + 1
            else:
                last_streak["status"] = "broken"
                db.updateHistory(
                    habit_id=self.habit_id, 
                    date=last_streak["date"], 
                    new_streak=last_streak["streak"], 
                    new_status=last_streak["status"]
                )

        db.addHistory(
            habit_id=self.habit_id,
            streak=new_streak,
            status="active",
            date=today
        )
        db.saveDB()
        print("history: " + today + " added") # !
        
        self.refreshStreaks()
        return True
    
    def uncheckOff(self, date=None) -> bool:
        """Removes a check-in for a given date (defaults to today).
        
        :return: True if succeeded | False if failed
        :rtype: bool
        """
        if not date:
            date = datetime.today().strftime('%Y-%m-%d')

        db = Database()
        
        # Retrieve the last recorded streak
        last_streak = self.getLastStreak()
        
        # If no history exists for this habit, return False
        if not last_streak or last_streak["date"] != date:
            print(f"Warning: No check-in found for {date}.")
            return False
        
        # Remove the habit entry for the given date
        db.deleteHistory(
            habit_id=self.habit_id, 
            date=date)
        return True


    # ++++++++++
    # JSON funcs

    @staticmethod
    def fromJSON(data: dict):
        """Creates a Habit object from JSON data.
        
        :return: Habit class Object created with json data
        :rtype: Habit
        """
        return Habit(
            habit_id=int(data["id"]),
            name=data["name"],
            desc=data["desc"],
            interval=data["interval"]
        )
        

    def toJSON(self):
        """Converts the Habit object to a dictionary.
        
        :return: converted habit object
        :rtype: dict[str, any]
        """
        return {
            "habit_id": self.habit_id,
            "name": self.name,
            "desc": self.desc,
            "interval": self.interval
        }