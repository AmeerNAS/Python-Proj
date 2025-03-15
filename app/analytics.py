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

# Utilities
# +++++++++
def parseDates(check_record):
    """Convert string dates to datetime objects."""
    return [datetime.strptime(date, '%Y-%m-%d') for date in check_record]

def getProgress(habits: list[Habit], date):
    """Calculate the percentage of habits completed on a given date."""
    total_habits = len(habits)
    completed_habits = sum(1 for habit in habits if habit.isChecked(date))
    
    return (completed_habits / total_habits) * 100 if total_habits > 0 else 0

def getFullProgress(habits):
    """Generate progress history using Habit class data."""
    all_dates = set()
    
    for habit in habits:
        all_dates.update(habit.getCheckins())

    if not all_dates:
        return {}

    progress_history = {}
    min_date = min(all_dates)  # Earliest habit check-in
    today = datetime.today().strftime('%Y-%m-%d')

    # Generate progress from first check-in to today
    current_date = min_date
    while current_date <= today:
        progress_history[current_date] = getProgress(habits, current_date)
        current_date = (datetime.strptime(current_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

    return progress_history

# +++++++++++++++++++
# Filters and Sorters
# +++++++++++++++++++
def filterHabits(habits: list[Habit], name: str = None, interval=None, min_streak=None):
    """Filter habits by name, interval, or minimum streak length."""
    filtered = habits.copy()
    if name:
        name_lower = name.lower()
        filtered = [h for h in filtered if name_lower in h.name.lower()]

    if interval:
        filtered = [h for h in filtered if h.interval.lower() == interval.lower()]

    if min_streak:
        filtered = [h for h in filtered if h.getStreaks("c") >= min_streak]
    
    return filtered


def sortHabits(habits: list[Habit], by="name", reverse=False):
    """Sort habits by name, interval, or streak length."""
    key_func = {
        "name": lambda h: h.name.lower(),
        "interval": lambda h: h.interval,
        "streak": lambda h: h.getStreaks("l"),
    }.get(by, lambda h: h.name.lower())

    return sorted(habits, key=key_func, reverse=reverse)


def sortHabits(habits: list[Habit], by="name", reverse=False):
    """Sort habits by name, interval, or streak length."""
    key_func = {
        "name": lambda h: h.name.lower(),
        "interval": lambda h: h.interval,
        "streak": lambda h: getStreak(h, "long"),
    }.get(by, lambda h: h.name.lower())

    return sorted(habits, key=key_func, reverse=reverse)

# ++++++++
# Plotters
# ++++++++
def plotLongestStreaks(habits: list[Habit]):
    """Generate an HTML representation of the streaks plot using Plotly."""
    habit_n_streaks = [(h.name, h.getStreaks("l")) for h in habits]
    habit_n_streaks.sort(key=lambda x: x[1], reverse=True)
    
    habit_names, streaks = zip(*habit_n_streaks) if habit_n_streaks else ([], [])
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=habit_names, 
        y=streaks, 
        marker=dict(color="skyblue", line=dict(color="black", width=1)),
        width=0.6
    ))
    
    fig.update_layout(
        title="Longest Streaks per Habit",
        xaxis_title="Habits",
        yaxis_title="Longest Streak",
        template="plotly_white",
        
        #html elements
        margin=dict(l=40, r=40, t=40, b=40),
        height=500
    )
    
    return pio.to_html(fig, full_html=False)


def plotProgress(habits: list[Habit]):
    """Generate a Plotly area plot for full progress, with last 7 days as the default view."""
    progress_history = getFullProgress(habits)

    if not progress_history:
        return "<p>No progress data available.</p>"

    # Extract dates and progress values
    dates = list(progress_history.keys())
    progress_values = list(progress_history.values())

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, 
        y=progress_values, 
        mode='lines+text',
        fill='tozeroy',
        line=dict(color='black', width=2),  
        fillcolor='rgba(135, 206, 250, 0.5)',  
        text=[f"{val:.0f}%" for val in progress_values],  
        textposition="top center",  
        name="Progress Over Time"
    ))

    # Default range (last 7 days)
    default_start = (datetime.strptime(dates[-1], '%Y-%m-%d') - timedelta(days=6)).strftime('%Y-%m-%d')

    fig.update_layout(
        title="",
        xaxis_title="Date",
        yaxis_title="Progress (%)",
        yaxis=dict(range=[0, 120], tickmode='linear', dtick=20),
        xaxis=dict(
            showgrid=False,
            rangeslider=dict(visible=True),  # Enables scrolling for full data
            rangeselector=dict(  # Default to last 7 days
                buttons=list([
                    dict(count=7, label="7d", step="day", stepmode="backward"),
                    dict(count=30, label="30d", step="day", stepmode="backward"),
                    dict(step="all", label="All")
                ])
            ),
            range=[default_start, dates[-1]]  # Initial view: Last 7 days
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        
        #html elements
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig.to_html()