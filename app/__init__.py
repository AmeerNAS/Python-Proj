from flask import Flask 
from app.db import Database

app = Flask(__name__)

db_manager = Database()

from app import routes