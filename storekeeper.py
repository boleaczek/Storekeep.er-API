from flask import Flask, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy


# inicjalizacja i konfiguracja aplikacji
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/baza.db'
db = SQLAlchemy(app)


# model produktu
class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(256), nullable=False)
	desc = db.Column(db.String())

	def __repr__(self):
		return '<Product %r>' % self.id

	def to_json(self):
		return {
			'id': self.id,
			'name': self.name,
			'desc': self.desc
		}


# wszystkie produkty
@app.route('/all')
def allProducts():
	return jsonify([p.to_json() for p in Product.query.all()])


# strona główna
@app.route('/')
def index():
	return "Hello World"
	

# uruchomienie aplikacji
app.run()
