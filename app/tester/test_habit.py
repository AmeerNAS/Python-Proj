import pytest
from datetime import datetime, timedelta
from app.habit import Habit
from app.db import Database

@pytest.fixture
def setup_habit():
    """Fixture to create a sample habit for testing."""
    db = Database()
    
    # Clear existing data for isolated tests
    db.db["tables"]["history"] = []
    db.saveDB()
    
    habit = Habit(habit_id=1, name="Test Habit", desc="Testing Habit", interval="DAILY")
    return habit, db

def test_habit_initialization(setup_habit):
    """Test if the habit initializes correctly."""
    habit, _ = setup_habit
    assert habit.habit_id == 1
    assert habit.name == "Test Habit"
    assert habit.interval == "DAILY"
    assert habit.current_streak == 0
    assert habit.longest_streak == 0

def test_check_off_habit(setup_habit):
    """Test checking off a habit updates the streak."""
    habit, db = setup_habit
    assert habit.checkOff() is True  # Should succeed
    assert habit.current_streak == 1
    assert habit.isChecked() is True

def test_streak_continuation(setup_habit):
    """Test if streak continues correctly based on interval."""
    habit, db = setup_habit
    today = datetime.today().strftime("%Y-%m-%d")
    
    habit.checkOff()  # Check off today
    assert habit.current_streak == 1
    
    # Simulate next day check-in
    next_day = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    db.addHistory(habit.habit_id, 2, "active", next_day)
    db.saveDB()
    
    habit.refreshStreaks()
    assert habit.current_streak == 2

def test_uncheck_habit(setup_habit):
    """Test unchecking a habit removes it from history."""
    habit, _ = setup_habit
    habit.checkOff()
    assert habit.uncheckOff() is True  # Should remove today's check-in
    assert habit.isChecked() is False