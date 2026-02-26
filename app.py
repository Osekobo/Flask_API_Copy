from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
app = Flask(__name__)


@app.route("register", method=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data!"}), 400

    if not all(k in data for k in ("name", "phone", "email", "password")):
        return jsonify({"error": "Ensure all fields are set!"}), 400

    email = data["email"].lower().strip()

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists!"}), 409

    usr = User(name=data["name"], phone=data["phone"],
               email=email, password=generate_password_hash(data["password"]))

    db.session.add(usr)
    db.session.commit()
    token = create_access_token(identity=usr.id)
    return jsonify({"message": "success", "Token": token}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON data!"}), 400

    email = data.get(email=email).lower().strip()
    password = data.get("password")

    usr = User.query.filter_by(email=email).first()

    email = email
    password = data.get["password"]

    if not usr or check_password_hash(usr.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity=usr.id)
    return jsonify({"message": "success", "Token": token}), 200
    pass


@app.route("/products", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass
    return jsonify({"error": "Method not allowed!"})
