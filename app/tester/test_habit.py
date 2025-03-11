from app.Habit import Habit
from datetime import datetime
import pytest


class TestHabit:

    def setup_method(self):
        #Habit setup for testing
        self.habit = Habit("Excercise", "do excercises for 30 minutes", "University")

    def test_single_date(self):
        self.habit.checking(datetime(2025, 1, 3))
        assert self.habit.longest_streak == 1

    def test_multi_date(self):
        self.habit.checking(datetime(2025,1,3))
        self.habit.checking(datetime(2025,1,4))
        self.habit.checking(datetime(2025,1,5))
        assert self.habit.longest_streak == 3

        self.habit.checking(datetime(2025,1,10))
        assert self.habit.longest_streak == 3 
    
    def test_personal(self):
        # Test
        test = Habit(1, "update","test habit for updating","daily")
        #test.editHabit("name", "updated")

        habit = Habit(2, "test", "test habit", "monthly", ["2025-02-19", "2025-02-11", "2025-02-13", "2025-02-14", "2025-02-15", "2025-02-16", "2025-02-17", "2025-02-23"])
        print(test.id) 
        print(habit.toString()) 
        print(habit.isbroken())   
    
    def teardown_method(self):
        del self.habit

pytest.main