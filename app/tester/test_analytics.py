import pytest
from datetime import datetime, timedelta
from app.habit import Habit
from app.db import Database
from app.analytics import (
    parseDates, getProgress, getFullProgress,
    filterHabits, sortHabits, plotLongestStreaks,
    plotHistory, plotStats, plotProgress
)

@pytest.fixture
def sample_habits():
    """Creates sample habits for testing."""
    habits = [
        Habit(habit_id=1, name="Exercise", desc="Execise by doing 10 pushups", interval="DAILY"),
        Habit(habit_id=2, name="Reading", desc="Read 10 pages atleast to be counted as complete", interval="DAILY"),
        Habit(habit_id=3, name="Meditation", desc="", interval="WEEKLY")
    ]
    return habits

def test_parseDates():
    """Tests conversion of date strings to datetime objects."""
    dates = ["2025-03-01", "2025-03-02"]
    parsed_dates = parseDates(dates)
    assert all(isinstance(date, datetime) for date in parsed_dates)

def test_getProgress(sample_habits):
    """Tests habit progress calculation for a given date."""
    date = datetime.today().strftime('%Y-%m-%d')
    sample_habits[0].checkOff()
    progress = getProgress(sample_habits, date)
    assert 0 <= progress <= 100

def test_getFullProgress(sample_habits):
    """Tests full progress history generation."""
    sample_habits[0].checkOff()
    progress_history = getFullProgress(sample_habits)
    assert isinstance(progress_history, dict)

def test_filterHabits(sample_habits):
    """Tests filtering habits by name, interval, and streak length."""
    filtered = filterHabits(sample_habits, interval="DAILY")
    assert all(h.interval == "DAILY" for h in filtered)

def test_sortHabits(sample_habits):
    """Tests sorting habits by name and streak values."""
    sorted_habits = sortHabits(sample_habits, by="name")
    assert sorted_habits[0].name == "Exercise"

def test_plotLongestStreaks(sample_habits):
    """Tests generation of longest streaks plot."""
    plot_html = plotLongestStreaks(sample_habits)
    assert "<div" in plot_html

def test_plotHistory(sample_habits):
    """Tests habit history visualization."""
    sample_habits[0].checkOff()
    plot_html = plotHistory(sample_habits[0])
    assert "<div" in plot_html

def test_plotStats(sample_habits):
    """Tests statistical visualization of habit check-offs."""
    sample_habits[0].checkOff()
    plot_html = plotStats(sample_habits[0])
    assert "<div" in plot_html

def test_plotProgress(sample_habits):
    """Tests progress visualization for all habits."""
    sample_habits[0].checkOff()
    plot_html = plotProgress(sample_habits)
    assert "<div" in plot_html
