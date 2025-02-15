import sqlite3
from datetime import date, time

def get_db(name = "main.db"):
    db = sqlite3.connect(name)
    create_tables(db)
    return db

def create_tables(db):
    cr = db.cursor()
    cr.execute("""CREATE TABLE IF NOT EXISTS counter (
            name TEXT PRIMARY KEY,
            description TEXT)""")
    
    cr.execute("""CREATE TABLE IF NOT EXISTS log (
            date TEXT,
            time TEXT,
            counterName TEXT,
            FOREIGN KEY (counterName) REFERENCES counter(name) 
            )""")
    
    db.commit()

def add_counter(db, name, desc):
    cr = db.cursor()

    cr.execute("INSERT INTO counter VALUES (?, ?)", (name, desc))
    db.commit

def increment_counter(db, name, eventDate=None, eventTime=None):
    cr = db.cursor()
    if not eventDate:
        eventDate = str(date.today)

    if not eventTime:
        eventTime = time.isoformat

    cr.execute("INSERT INTO log VALUES (?, ?, ?)", (name, eventDate, eventTime))
    db.commit

def get_counterByName(db, name):
    cr = db.cursor()
    cr.execute("SELECT * FROM tracker WHERE name=?", (name))
    return cr.fetchall()


db= get_db()
create_tables(db)

