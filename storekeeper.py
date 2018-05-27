from flask import Flask, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import json

# inicjalizacja i konfiguracja aplikacji
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/baza.db'
app.config['SQLALCHEMY_BINDS'] = { 'users': 'sqlite:///data/auth.db' }
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


# użytkownicy (to tymczasowe, później będziemy ich ściągać z bazy)
users = {
	"kamil": "limak",
	"bartosz": "denys",
	"test": "test"
}


# zwraca hasło dla danego loginu
@auth.get_password
def get_pwd(user):
	if user in users:
		return users.get(user)
	return None


# model użytkownika
class User(db.Model):
	__bind_key__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(256), nullable=False)
	password = db.Column(db.String(256), nullable=False)

	def __init__(self, username, password):
		self.username = username
		self.password = generate_password_hash(password)

	def to_json(self):
		return {
			'id': self.id,
			'username': self.username,
			'password hash': self.password
		}

	def checkPassword(self, password):
		return check_password_hash(self.password, password)


# model produktu
class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(256), nullable=False)
	desc = db.Column(db.String())
	picture_ulr = db.Column(db.String(256), nullable=True) 

	def __repr__(self):
		return '<Product %r>' % self.id

	def to_json(self):
		return {
			'id': self.id,
			'name': self.name,
			'desc': self.desc
		}

	category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
		nullable=False)

	category = db.relationship('Category',
		backref=db.backref('products', lazy=True))

	def __init__(self, name, desc, category_id):
		self.name = name
		self.desc = desc
		self.category_id = category_id

#model kategorii
class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	
	def __repr__(self):
		return '<Category %r>' % self.name

	def __init__(self, name):
		self.name = name

# dodanie kategorii
@auth.login_required
@app.route('/category', methods=['POST'])
def addCategory():
	json = request.get_json()
	category = Category(json.get('name'))
	db.session.add(category)
	db.session.commit()
	
	return jsonify({
		'msg': 'Category added.'	
	}), 200

# wyswietlenie wszystkich kategorii
@app.route('/category', methods=['POST'])
def showCategories():
	return jsonify([c.to_json() for c in Category.query.all()]), 200

# wyswietlenie produktow w danej kategorii
@app.route('/category/products/<id>', methods=['GET'])
def showProductsInCategory(id):

	return jsonify([p.to_json() for p in Product.query.filter_by(category_id=id).all()]), 200

# wszystkie produkty
@app.route('/all', methods=['GET'])
def showProducts():
	return jsonify([p.to_json() for p in Product.query.all()]), 200

# jeden produkt
@app.route('/product/<id>', methods=['GET'])
def showProduct(id):
	product = Product.query.filter_by(id=id).first()

	if product is not None:
		return jsonify(product.to_json()), 200
	else:
		return jsonify({
			'msg': 'Product not found.'
		}), 404

# dodanie nowego produktu
@auth.login_required
@app.route('/product', methods=['POST'])
def addProduct():
	json = request.get_json()
	product = Product(json.get('name'), json.get('desc'), json.get('category_id'))
	db.session.add(product)
	db.session.commit()

	return jsonify({
		'msg': 'Product added.'	
	}), 200

#modyfikacja istniejącego produktu
@auth.login_required
@app.route('/product/update/<id>', methods=['POST'])
def updateProduct(id):
	product = Product.query.filter_by(id=id).first()
	json = request.get_json()
	name = json.get('name')
	desc = json.get('desc')
	if name is not None:
		product.name = name
	if desc is not None:
		product.desc = desc

	db.session.commit()
	return jsonify({
		'msg': 'Product updated.'
	}), 200

# usunięcie istniejącego produktu
@auth.login_required
@app.route('/product/<id>', methods=['DELETE'])
def deleteProduct(id):
	product = Product.query.filter_by(id=id).first()

	if product is not None:
		db.session.delete(product)
		db.session.commit()

		return jsonify({
			'msg': 'Product deleted.'
		}), 200
	else:
		return jsonify({
			'msg': 'Product not found.'
		}), 404

# strona główna
@app.route('/')
def index():
	msg = "Allowed requests: GET /all, GET /product/<id>, POST /product, DELETE /product/<id>"
	return msg, 200

# uruchomienie aplikacji
app.run()
