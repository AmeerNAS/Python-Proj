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
    
    def teardown_method(self):
        del self.habit

pytest.main