from flask import Flask, request, jsonify
from models import db, User, Product, Purchase
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
app = Flask(__name__)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    if not all(k in data for k in ("name", "phone", "email", "password")):
        return jsonify({"error": "Ensure all fields are set"}), 400
    email = data["email"].lower().strip()
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409
    usr = User(name=data["name"], phone=data["phone"],
               email=email, password=data["password"])
    db.session.add(usr)
    db.session.commit()
    token = create_access_token(identity=usr.id)
    return jsonify({"message": "User created", "Token": token}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Ensure all fields are set!"}), 400
    email = data.get("email").lower().strip()
    password = data.get("password")
    usr = User.query.filter_by(email=email).first()
    if not email or not generate_password_hash(usr.password, password):
        return jsonify({"error": "Invalid email or password"}), 401
    token = create_access_token(identity=usr.id)
    return jsonify({"message": "Login successful", "Token": token})


@app.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "GET":
        products = Product.query.all()
        product_list = []
        for p in products:
            data = {}
            product_list.append(data)
        return jsonify(product_list)
    elif request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data!"}), 400
        name = data.get("name")
        buying_price = data.get("buying_price")
        selling_price = data.get("selling_price")
        if not name or buying_price is None or selling_price is None:
            return jsonify({"error": "Ensure all fields are set!"}), 400
        if buying_price < 0 or selling_price < 0:
            return jsonify({"error": "Ensure prices are above 0"}), 400
        prod = Product()
        db.session.add(prod)
        db.session.commit()
        return jsonify({"id": prod.id}), 201
    return jsonify({"error": "Method not allowed!"}), 405


@app.route("/purchases", methods=["GET", "POST"])
def purchases():
    if request.method == "GET":
        purchases = Purchase.query.all()
        purchases_list = []
        for p in purchases:
            data = {}
            purchases_list.append(data)
        return jsonify(purchases_list), 200
    elif request.method == "POST":
        pass
    return jsonify({"error": "Method not allowed!"}), 405
