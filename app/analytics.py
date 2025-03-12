from datetime import timedelta, datetime
from Habit import Habit
import pandas as pd
import matplotlib.pyplot as plt

# TODO: longest streak only gets updated on the first current streak, must rechange the calculation system to account for a longes streak the happened to old save data independantly
# TODO: add pyplot of history of streak
# TODO: add pyplot of multiple streaks stats
# TODO: add filter options
    
def parse_dates(check_record):
    """Convert string dates to datetime objects."""
    return [datetime.strptime(date, '%Y-%m-%d') for date in check_record]

#Prof. compute streak method imporvised
def getStreak(habit: Habit, streak=None):
    """ 
    Calculates streaks without resetting the saved values. 
    
    :param Habit habit: The Habit object to analyze.
    :param str | None streak: 
        - None: Return only current streak.
        - "long": Return longest streak.
        - "both": Return both streaks (tuple: current, longest).
    :return: Current streak or longest streak or both.
    :rtype: int | (int, int)
    """
    if not habit.check_record:
        return 0 if streak is None else (0, habit.longest_streak) if streak == "both" else habit.longest_streak # instant returns for empty param case 

    records = parse_dates(habit.check_record)
    sorted_dates = sorted(records)

    # Start from stored values
    current_streak = habit.current_streak or 1
    max_streak = habit.longest_streak or 1

    for i in range(1, len(sorted_dates)):
        if sorted_dates[i] - sorted_dates[i - 1] == timedelta(days=1):
            current_streak += 1
            max_streak = max(max_streak, current_streak)  # Only update if we find a longer streak
        else:
            current_streak = 1  # Reset only current streak (longest remains)

    habit.current_streak = current_streak
    habit.longest_streak = max_streak  # Preserve longest streak

    if streak == "long":
        return habit.longest_streak
    elif streak == "both":
        return habit.current_streak, habit.longest_streak
    elif streak is not None:
        raise ValueError(f"Invalid streak option: {streak}")

    return habit.current_streak
    


""" def compute_streak(habit):
    ""Calculate current and longest streaks without modifying habit.""
    records = parse_dates(habit)
    if not records:
        return 0, 0  # No streaks if no records

    sorted_dates = sorted(records)
    current_streak = 1
    longest_streak = 1
    temp_streak = 1

    for i in range(1, len(sorted_dates)):
        if sorted_dates[i] - sorted_dates[i-1] == timedelta(days=1):
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 1

    current_streak = temp_streak
    return current_streak, longest_streak """

def filter_habits(habits: list[Habit], interval=None, min_streak=None):
    """Filter habits by interval or minimum streak length."""
    filtered = habits
    if interval:
        filtered = [h for h in filtered if h.interval == interval]
    if min_streak:
        filtered = [h for h in filtered if getStreak(h, "long") >= min_streak]
    return filtered

def sort_habits(habits: list[Habit], by="name", reverse=False):
    """Sort habits by name, interval, or streak length."""
    key_func = {
        "name": lambda h: h.name.lower(),
        "interval": lambda h: h.interval,
        "streak": lambda h: getStreak(h, "long"),
    }.get(by, lambda h: h.name.lower())

    return sorted(habits, key=key_func, reverse=reverse)

def plot_streaks(habits: list[Habit]):
    """Plot longest streaks for habits."""
    habit_names = [h.name for h in habits]
    streaks = [getStreak(h, "long") for h in habits]

    plt.figure(figsize=(10, 5))
    plt.bar(habit_names, streaks, color='skyblue')
    plt.xlabel("Habits")
    plt.ylabel("Longest Streak")
    plt.title("Longest Streaks per Habit")
    plt.xticks(rotation=45)
    plt.show()