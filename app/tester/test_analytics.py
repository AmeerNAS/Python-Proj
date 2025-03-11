from analytics import Analytics

class testAnalytics:
    def startup_method(self):
        pass
    
    def testFunction(self):
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

    def teardown_method(self):
        pass