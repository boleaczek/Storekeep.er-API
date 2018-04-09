from flask import Flask, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json


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

	def __init__(self, name, desc):
		self.name = name
		self.desc = desc

# wszystkie produkty
@app.route('/all')
def showProducts():
	return jsonify([p.to_json() for p in Product.query.all()]), 200


# jeden produkt
@app.route('/product/<id>')
def showProduct(id):
	product = Product.query.filter_by(id=id).first()

	if product is not None:
		return jsonify(product.to_json()), 200
	else:
		return jsonify({
			'msg': 'nie ma takiego produktu'
		}), 404

@app.route('/product', methods=['POST', 'GET'])
def addProduct():
	if request.method == 'POST':
		product = Product(request.json["name"], request.json["desc"])
		db.session.add(product)
		db.session.commit()
		return "Product added", 200


# strona główna
@app.route('/')
def index():
	return "Hello World", 200
	

# uruchomienie aplikacji
app.run()
