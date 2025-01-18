from datetime import datetime, timedelta 


class Habit:   

    def __init__(self, name, desc, type):
        
        # Basic data initialization
        self.name = name
        self.desc = desc
        self.type = type
        self.longest_streak = 0
        self.current_streak = 0


        # check-off dates record list
        self.check_record = []

    #Check-off function: takes current date and appends it to check_record list then computes streak.
    def checking(self, date):
        self.check_record.append(date)
        self.compute_streak()

    #Prof. compute method
    def compute_streak(self):
        #Sort the check record and creates temp clone
        sorted_dates = sorted(self.check_record)

        #No records handling:
        if not sorted_dates:
            self.longest_streak = 0
            return

        #variable initialization
        l_streak = 1
        c_streak = 1    

        for i in range(1, len(sorted_dates)):
            if sorted_dates[i] -sorted_dates[i-1]==timedelta(days=1):
                c_streak += 1
                l_streak = max(l_streak, c_streak)
            else:
                c_streak = 1
            
        self.longest_streak = l_streak
        self.current_streak = c_streak
