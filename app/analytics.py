from datetime import timedelta, datetime
from app.habit import Habit
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
            max_streak = max(max_streak, current_streak)  #update if we find a longer streak
        else:
            current_streak = 1 

    habit.current_streak = current_streak
    habit.longest_streak = max_streak

    #Debug print
    #print(f"📊 DEBUG: Habit {habit.id} -> Current Streak: {habit.current_streak}, Longest Streak: {habit.longest_streak}")
    
    if streak == "long":
        return habit.longest_streak
    elif streak == "both":
        return habit.current_streak, habit.longest_streak
    elif streak is not None:
        raise ValueError(f"Invalid streak option: {streak}")

    return habit.current_streak

def filterHabits(habits: list[Habit], name: str =None, interval=None, min_streak=None):
    """Filter habits by interval or minimum streak length."""
    filtered = habits.copy()
    if name:
        name_lower = name.lower()
        filtered = [h for h in filtered if name_lower in h.name.lower()]

    if interval:
        filtered = [h for h in filtered if h.interval.lower() == interval.lower()]

    if min_streak:
        filtered = [h for h in filtered if h.current_streak >= min_streak]
    return filtered

# +++++++++++++++++++
# Filters and Sorters
# +++++++++++++++++++
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
    # Compute streaks once and sort habits accordingly
    habit_n_streaks = [(h.name, getStreak(h, "long")) for h in habits]
    habit_n_streaks.sort(key=lambda x: x[1], reverse=True)  # Sort by streak (descending)

    # Unpack sorted habit names and streak values
    habit_names, streaks = zip(*habit_n_streaks) if habit_n_streaks else ([], [])
    

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

    #for layout
    fig.update_layout(
        title="Longest Streak of Habits",
        xaxis_title="Habits",
        yaxis_title="Longest Streak",
        xaxis=dict(),
        yaxis=dict(
            tickmode="linear",
            dtick=1,  
            tickformat="d"  #integer
        ),
        template="plotly_white",
        height=500,  #adjusts html element hight
        #width=1200 
    )

    # Convert Plotly figure to HTML
    fig_in_html = pio.to_html(fig, full_html=False)
    
    return fig_in_html

# +++++++++++++++++++
# Progress Calculator
# +++++++++++++++++++
def getProgress(habits: list[Habit], date):
    """Calculate the percentage of habits completed on a given date."""
    total_habits = len(habits)
    completed_habits = sum(1 for habit in habits if date in habit.check_record)
    
    return (completed_habits / total_habits) * 100 if total_habits > 0 else 0

def getWeeklyProgress(habits):
    """Generate progress history for the past 7 days."""
    today = datetime.today()
    progress_history = {}

    for i in range(7):
        day = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        progress_history[day] = getProgress(habits, day)

    return dict(sorted(progress_history.items()))  # Sort by date

def plotWeeklyProgress(habits: list[Habit]):
    """Generate a Plotly area plot for weekly progress."""
    weekly_progress = getWeeklyProgress(habits)

    #gets pairwise values
    dates = list(weekly_progress.keys())
    progress_values = list(weekly_progress.values())

    #area plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=progress_values, mode='lines+text',
        fill='tozeroy',
        line=dict(color='black', width=2),  
        fillcolor='rgba(135, 206, 250, 0.5)',  
        text=[f"{val:.0f}%" for val in progress_values],  
        textposition="top center",  
        name="Weekly Progress"
    ))

    fig.update_layout(
        title="Weekly Habit Completion Progress",
        xaxis_title="Date",
        yaxis_title="Progress (%)",
        yaxis=dict(range=[0, 120], tickmode='linear', dtick=20),  # Adjusted range for visual effect
        xaxis=dict(
            #range=[dates[0] - timedelta(hours=12), dates[-1] + timedelta(hours=12)],
            showgrid=False),
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )

    return fig.to_html()