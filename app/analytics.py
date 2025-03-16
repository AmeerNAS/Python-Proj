""" 
Advanced Analytics module.
Allows for analysis of data and plotting for visualization.
External to habit or db modules, however requires Habit for functionlity.
"""
# Import
#data parcing
from datetime import timedelta, datetime
from app.habit import Habit

#data porcessing 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#data reprsentations
import plotly.graph_objects as go
import plotly.io as pio


# +++++++++
# Utilities

def parseDates(record):
    """
    Convert string dates to datetime objects.
    \
        :param "%Y-%m-%d" record:
            - %Y: the year, format of '20XX',
            - %m: the month, formtat of '1X'.
            - $d: the date format of '1X'.
            :return: The inputted record
            :rtype: datetime.date
    """
    return [datetime.strptime(date, '%Y-%m-%d') for date in record]

def getProgress(habits: list[Habit], date):
    """
    Calculate the percentage of habits completed on a given date.
    \
        :param list[Habit] habits:
            A list of Habit object habits to be used.
        :param Date date:
            the date to be used for calculation.
            
        :return: 0 | The Calculated Percentage out of 100
        :rtype: int
    """
    total_habits = len(habits)
    completed_habits = sum(1 for habit in habits if habit.isChecked(date))
    
    return (completed_habits / total_habits) * 100 if total_habits > 0 else 0

def getFullProgress(habits):
    """Generate progress history using Habit class data.
    \
    :param list[Habit] habits:
        A list of Habit object habits to be used.
        
    :return: {} | The calculated progress for the entire list of habits
    :rtype: list
    """
    all_dates = set()
    
    for habit in habits:
        all_dates.update(habit.getCheckins())

    if not all_dates:
        return {}

    progress_history = {}
    min_date = min(all_dates)
    today = datetime.today().strftime('%Y-%m-%d')

    #(algo 2) generates from first check-in to today 
    current_date = min_date
    while current_date <= today:
        progress_history[current_date] = getProgress(habits, current_date)
        current_date = (datetime.strptime(current_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

    return progress_history

# +++++++++++++++++++
# Filters and Sorters

def filterHabits(habits: list[Habit], name: str = None, interval=None, min_streak: int = None):
    """
    Filter habits by name, interval, or minimum streak length.
    \
    :param str habits:
        A list of Habit object habits to be used by the filter.
        
    :param str name:
        A name keyword that will be used to filter the habits.
        
    :param str interval:
        The type of interval to filter by.
        
    :param int min_streak:
        Refers to the a specified integer that will be used to filter any habit with  streak below its value.
        
        
    :return: {} | The Filtered list of the entire list of habits
    :rtype: list[Habit]
    """
    filtered = habits.copy()
    if name:
        name_lower = name.lower()
        filtered = [h for h in filtered if name_lower in h.name.lower()]

    if interval:
        filtered = [h for h in filtered if h.interval.lower() == interval.lower()]

    if min_streak:
        filtered = [h for h in filtered if h.current_streak >= min_streak]
    
    return filtered


def sortHabits(habits: list[Habit], by="name", reverse=False):
    """
    Sort habits by name, interval, or streak value.
    \
    :param str habits: A list of Habit object habits to be used by the sorter.
    
           
    :param str by: "name" | specified what sorting method to use.
            
            - by "interval": sorts by inerval difference
            - by "name": sorts by name of habits
            - by "l": sorts by longest streak value
            - by "c": sorts by current streak value
        
    
    :param bool reverser:
        False | Toggles reverse indexing of sorter result
        
 
    :return: {} | The Sorted list of the entire list of habits
    :rtype: list[Habit]
    """
    if by is None and reverse:
        return reversed(habits)
    
    key_func = {
        "name": lambda h: h.name.lower(),
        "interval": lambda h: h.interval,
        "c": lambda h: h.current_streak,
        "l": lambda h: h.longest_streak
    }.get(by, lambda h: h.name.lower())

    return sorted(habits, key=key_func, reverse=reverse)

# ++++++++
# Plotters

#Used once for peristant bar coloring
import plotly.colors as pc

def plotLongestStreaks(habits: list[Habit]):
    """Plots a bar Graph of the streaks plot and returns a HTML representation using Plotly.
    \
    :param list[Habit] habits:
        A list of Habit object habits to be used in the algo.
        
    :return: "" | A converted SVG element plot of the list of habits
    :rtype: str
    """
    habit_n_streaks = [(h.name, h.getStreaks("l")) for h in habits]
    habit_n_streaks.sort(key=lambda x: x[1], reverse=True)
    
    habit_names, streaks = zip(*habit_n_streaks) if habit_n_streaks else ([], [])

    #uses color palette
    colors = pc.qualitative.Plotly * (len(habit_names) // len(pc.qualitative.Plotly) + 1)
    colors = colors[:len(habit_names)]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=habit_names, 
        y=streaks, 
        marker=dict(color=colors, line=dict(color="black", width=1)),
        width=0.6
    ))
    
    fig.update_layout(
        title="Longest Streaks per Habit",
        xaxis_title="Habits",
        yaxis_title="Longest Streak",
        template="plotly_white",
        
        # HTML elements
        margin=dict(l=40, r=40, t=40, b=40),
        height=500
    )
    
    return pio.to_html(fig, full_html=False)

def plotHistory(habit: Habit):
    """
    Plots a scatter of the complete history of a habit over time and 
    returns a HTML representation using Plotly.
    
    \
    :param list[Habit] habits:
        A list of Habit object habits to be used in the algo.
        
    :return: "" | A converted SVG element plot of the list of habits
    :rtype: str
    """
    history = habit.getAllStreaks()
    
    if not history:
        return "<p>No history available for this habit.</p>"

    # Convert to DataFrame
    df = pd.DataFrame(history)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")  # Ensure chronological order

    # Create plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], 
        y=df["streak"], 
        mode="lines+markers", 
        line=dict(color="blue"),
        marker=dict(size=6, color="blue"),
        name="Streak"
    ))

    fig.update_layout(
        title="",
        xaxis_title="Date",
        yaxis_title="Streak",
        template="plotly_white",
        
        # html elements
        margin=dict(l=40, r=40, t=10, b=40),
        height=400
    )

    return pio.to_html(fig, full_html=False)


def plotStats(habit: Habit):
    """
    Plots the average check-off distribution for a single habit and 
    returns a HTML representation using Plotly.
    
    \
    :param list[Habit] habits:
        A list of Habit object habits to be used in the algo.
        
    :return: "" | A converted SVG element plot of the habit object's check dates:
    
        - over the week if interval is daily
        - over the momth's weeks if the interval is weekly
    :rtype: str
    """
    
    check_dates =[s["date"] for s in habit.getAllStreaks()] 
    if not check_dates:
        return "<p>No check-off data available.</p>"  #incase no data

    # Convert dates to pandas datetime format
    df = pd.DataFrame(check_dates, columns=["date"])
    df["date"] = pd.to_datetime(df["date"])

    if habit.interval == "DAILY":
        # Group by day of the week (0=Monday, 6=Sunday)
        df["day_of_week"] = df["date"].dt.dayofweek
        day_counts = df["day_of_week"].value_counts().sort_index()
        x_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    elif habit.interval == "WEEKLY":
        # Group by week of the month (1st → 4th week)
        df["week_of_month"] = (df["date"].dt.day - 1) // 7 + 1
        week_counts = df["week_of_month"].value_counts().sort_index()
        x_labels = ["1st Week", "2nd Week", "3rd Week", "4th Week"]

    # Create bar plot
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x_labels, 
        y=day_counts if habit.interval == "DAILY" else week_counts,
        marker=dict(color="orange"),  
        width=0.6
    ))

    # Update layout
    fig.update_layout(
        title="",
        xaxis_title="Day of Week" if habit.interval == "DAILY" else "Week of Month",
        yaxis_title="Check-off Frequency",
        template="plotly_white",
        margin=dict(l=40, r=40, t=40, b=40),
        height=400
    )

    return pio.to_html(fig, full_html=False)

def plotProgress(habits: list[Habit]):
    """Generate area plot for full progress, with last 7 days as the default view and 
    returns a HTML representation using Plotly.
    
    \
    :param list[Habit] habits:
        A list of Habit object habits to be used in the algo.
        
    :return: "" | A converted SVG element plot of the habit objects list (with a default view of the last 7 days)
    :rtype: str
    """
    progress_history = getFullProgress(habits)

    if not progress_history:
        return "<p>No progress data available.</p>"

    #extracting dates
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

    #last 7 days
    default_start = (datetime.strptime(dates[-1], '%Y-%m-%d') - timedelta(days=6)).strftime('%Y-%m-%d')

    fig.update_layout(
        title="",
        xaxis_title="Date",
        yaxis_title="Progress (%)",
        yaxis=dict(range=[0, 120], tickmode='linear', dtick=20),
        xaxis=dict(
            showgrid=False,
            rangeslider=dict(visible=True),  #for full data
            rangeselector=dict( 
                buttons=list([
                    dict(count=7, label="7d", step="day", stepmode="backward"),
                    dict(count=30, label="30d", step="day", stepmode="backward"),
                    dict(step="all", label="All")
                ])
            ),
            range=[default_start, dates[-1]]
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        
        #html elements
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig.to_html()