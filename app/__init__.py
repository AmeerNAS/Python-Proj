""" App Initializer and index file for server run """

from flask import Flask 
from app.db import Database

# creates Flask App
app = Flask(__name__)

# initializes DB 
db_manager = Database()

# points to Routes
from app import routes