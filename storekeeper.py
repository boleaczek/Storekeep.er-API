from flask import Flask, url_for
import sqlite3
app = Flask(__name__)
db = sqlite3.connect('data/baza.db')

@app.route('/')
def index():
	return "Hello World"
