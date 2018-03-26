from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def index():
	return "Hello World"
