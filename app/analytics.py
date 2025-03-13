from datetime import timedelta, datetime
from app.Habit import Habit
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio

# TODO: longest streak only gets updated on the first current streak, must rechange the calculation system to account for a longes streak the happened to old save data independantly
# TODO: add pyplot of history of streak
# TODO: add pyplot of multiple streaks stats
# TODO: add filter options
    
def parseDates(check_record):
    """Convert string dates to datetime objects."""
    return [datetime.strptime(date, '%Y-%m-%d') for date in check_record]

#Prof. compute streak method imporvised
def getStreak(habit: Habit, streak=None):
    """ 
    Calculates streaks without resetting the saved values. 
    \
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

    records = parseDates(habit.check_record)
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
    
""" def computeStreak(habit):
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

def filterHabits(habits: list[Habit], interval=None, min_streak=None):
    """Filter habits by interval or minimum streak length."""
    filtered = habits
    if interval:
        filtered = [h for h in filtered if h.interval == interval]
    if min_streak:
        filtered = [h for h in filtered if getStreak(h, "long") >= min_streak]
    return filtered

def sortHabits(habits: list[Habit], by="name", reverse=False):
    """Sort habits by name, interval, or streak length."""
    key_func = {
        "name": lambda h: h.name.lower(),
        "interval": lambda h: h.interval,
        "streak": lambda h: getStreak(h, "long"),
    }.get(by, lambda h: h.name.lower())

    return sorted(habits, key=key_func, reverse=reverse)

def plotLongestStreaks(habits: list[Habit]):
    """Generate an HTML representation of the streaks plot using Plotly."""
    
    habit_names = [h.name for h in habits]
    streaks = [getStreak(h, "long") for h in habits]

    #create Plotly instance
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=habit_names, 
        y=streaks, 
        marker=dict(
            color="skyblue",
            line=dict(color="black", width=1)
        ),
        width=0.6
    ))

    # Customize layout
    fig.update_layout(
        title="Longest Streak of Habits",
        xaxis_title="Habits",
        yaxis_title="Longest Streak",
        xaxis=dict(),
        yaxis=dict(
            tickmode="linear",
            dtick=1,  # Force ticks to be whole numbers
            tickformat="d"  # Format as integers
        ),
        template="plotly_white",
        height=500,  #adjusts html element hight
        width=1200 
    )

    # Convert Plotly figure to HTML
    fig_in_html = pio.to_html(fig, full_html=False)
    
    return fig_in_html
