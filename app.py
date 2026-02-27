from flask import Flask, request, jsonify
from models import db, User, Product, Purchase, Sale
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from collections import defaultdict
app = Flask(__name__)


@app.route("/")
def home():
    return ("Flask version 1.0")


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    if not all(k in data for k in ("name", "phone", "email", "password")):
        return jsonify({"error": "Ensure all fields are set!"}), 400

    email = data["email"].lower().strip()

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists!"}), 409
    usr = User(name=data["name"], phone=data["phone"],
               email=email, password=data["password"])

    db.session.add(usr)
    db.session.commit()
    token = create_access_token(identity=usr.id)
    return jsonify({"message": "User registered!", "token": token}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    if "email"not in data or "password"not in data:
        return jsonify({"error": "Ensure all fields are set!"}), 400

    email = data.get("email").lower().strip()
    password = data.get("password")

    usr = User.query.filter_by(email=email).first()

    if not usr or not check_password_hash(usr.password, password):
        return jsonify({"error": "Invalid email or password!"})

    token = create_access_token(identity=usr.id)

    return jsonify({"token": token}), 200


@app.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "GET":
        products = Product.query.all()
        product_list = []
        for x in products:
            data = {}
            product_list.append(data)
        return jsonify(product_list), 200
    elif request.method == "POST":
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON body"}), 400

        name = data.get("name")
        buying_price = data.get("buying_price")
        selling_price = data.get("selling_price")

        if not name or buying_price is None or selling_price is None:
            return jsonify({"error": "Ensure all fields are set!"}), 400

        if selling_price < 0 or buying_price < 0:
            return jsonify({"error": "Ensure prices are above 0"}), 400

        prod = Product(name=name,
                       buying_price=buying_price,
                       selling_price=selling_price)
        db.session.add(prod)
        db.session.commit()
        return jsonify({"id": prod.id}), 201

    return jsonify({"error": "Method not allowed!"}), 405


@app.route("/purchases", methods=["GET", "POST"])
def purchases():
    if request.method == "GET":
        purchases = Purchase.query.all()
        purchase_list = []
        for p in purchases:
            data = {}
            purchase_list.append(data)
        return jsonify(purchase_list), 200
    elif request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data!"}), 400
        if "quantity"not in data or "product_id"not in data:
            return jsonify({"error": "Ensure all fields are set!"}), 400
        purch = Purchase()
        db.session.add(purch)
        db.session.commit()
        response = {}
        return jsonify(response), 201
    return jsonify({"error": "Method not allowed!"}), 400


@app.route("/sales", methods=["GET", "POST"])
def sales():
    if request.method == "GET":
        data = ()
        sales_list = defaultdict(list)
        for sale, detail, product in data:
            sales_list[sale.id].append((sale, detail, product))
        result = []
        return jsonify(result), 200
    elif request.method == "POST":
        pass
    return jsonify({"error": "Method not allowed!"}), 400

@app.route("/forgot_password",methods=["POST"])
def forgot_password():
    pass