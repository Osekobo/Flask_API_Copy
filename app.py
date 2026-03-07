from flask import Flask, request, jsonify
from models import db, User, Product, Purchase
from flask_jwt_extended import create_access_token, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'hgyutd576uyfutu'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:12039@localhost:5432/learning"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
jwt = JWTManager(app)


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
    email = data.get("email").lower().strip()

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 409
    usr = User(name=data["name"], phone=data["phone"],
               email=email, password=generate_password_hash(data["password"]))
    db.session.add(usr)
    db.session.commit()
    token = create_access_token(identity=usr.id)
    return jsonify({"message": "User registered successfuly!", "Token": token}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400
    if "email"not in data or "password"not in data:
        return jsonify({"error": "Ensure all fields are set"}), 400
    email = data.get("email").lower().strip()
    password = data.get("password")
    usr = User.query.filter_by(email=email).first()
    if not usr or not check_password_hash(usr.password, password):
        return jsonify({"error": "Invalid email or password!"}), 409
    token = create_access_token(identity=usr.id)
    return jsonify({"message": "Login successful!", "Token": token}), 200


@app.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "GET":
        products = Product.query.all()
        products_list = []
        for p in products:
            data = {"id": p.id, "name": p.name,
                    "buying_price": p.buying_price, "selling_price": p.buying_price}
            products_list.append(data)
        return jsonify(products_list), 200
    elif request.method == "POST":
        data=request.get_json()
        if not data:
            return jsonify({"error":""}),400
        pass
    return jsonify({"error": "Method not allowed"}), 405


if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run()
