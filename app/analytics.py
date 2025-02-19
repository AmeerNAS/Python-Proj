from datetime import timedelta, datetime
from Habit import Habit

class Analytics:
    def __init__(self):
        pass

    #Prof. compute streak method
    # TODO: longest streak only gets updated on the first current streak, must rechange the calculation system to account for a longes streak the happened to old save data independantly
    def getStreak(habit: Habit, streak=None):
        """ 
        Sorts the check record list and creates temp clone for streak calculation, returns by default current streak only \n
        :param: Habit habit: the Habit object to be used in the calculations. 
        :param: None | str streak: None for current streak, "long" for long streak, "both" for both streaks (expect 2 output). Format string used for controling the output.
        :return: habit's: current_streak or longest_streak | current_streak & longest streak.
        :rtype: int | int, int
        """
        records = [datetime.strptime(record, '%Y-%m-%d') for record in habit.check_record]
        sorted_dates = sorted(records)

        #No records handling:
        if not sorted_dates:
            habit.longest_streak = 0
            return

        #variable initialization
        temp_c = 1    
        

        for i in range(1, len(sorted_dates)):
            if sorted_dates[i] -sorted_dates[i-1]==timedelta(days=1):
                temp_c += 1
                habit.longest_streak = max(habit.longest_streak, temp_c)
            else:
                temp_c = 1

        habit.current_streak = temp_c
        if streak:
            if streak == "long":
                return habit.longest_streak
            elif streak == "both":
                return habit.current_streak, habit.longest_streak
            else:
                ValueError(streak)
        return habit.current_streak
        
    
habit = Habit(1, "Test", "test habit for analytics", "daily", ["2025-02-19",
                    "2025-02-11",
                    "2025-02-13",
                    "2025-02-14",
                    "2025-02-15",
                    "2025-02-16",
                    "2025-02-17",
                    "2025-02-19",
                    "2025-02-20",
                    "2025-02-22",
                    "2025-02-22",
                    "2025-02-23",
                    "2025-02-19"] )
    

# test:
streak = Analytics.getStreak(habit)
longest_streak = Analytics.getStreak(habit, "long")
st1, st2 = Analytics.getStreak(habit, "both")

print(f"Current Streak: {streak}")
print(f"Longest Streak: {longest_streak}") 
print(st1, st2)
