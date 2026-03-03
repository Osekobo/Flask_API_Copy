from flask import Flask, request, jsonify
from models import db, Product, User, Purchase
from flask_jwt_extended import create_access_token, JWTManager
from werkzeug.security import check_password_hash, generate_password_hash
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'hgyutd576uyfutu'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:12039@localhost:5432/learning"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
jwt = JWTManager(app)


@app.route("/")
def home():
    return ("Flask Version 1.0")


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data!"}), 400

    # name = data["name"]
    # phone = data["phone"]

    # password = data["password"]
    # usr = User.query.filter_by(email=email).first()

    if not all(k in data for k in ("name", "phone", "email", "password")):
        return jsonify({"error": "Ensure all fields are set!"}), 400

    email = data["email"].lower().strip()

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409

    usr = User(name=data["name"], phone=data["phone"], email=email,
               password=generate_password_hash(data["password"]))

    db.session.add(usr)
    db.session.commit()
    token = create_access_token(identity=usr.id)

    return jsonify({"message": "User registered!", "Token": token}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data!"}), 400
    if "email" not in data or "password" not in data:
        return jsonify({"error": "Ensure all fields are set!"}), 400

    email = data.get("email").lower().strip()
    password = data.get("password")
    usr = User.query.filter_by(email=email).first()

    if not usr or not check_password_hash(usr.password, password):
        return jsonify({"error": "Invalid email or password!"}), 401

    token = create_access_token(identity=usr.id)

    return jsonify({"message": "Login successful!", "Token": token})


@app.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "GET":
        products = Product.query.all()
        products_list = []
        for x in products:
            data = {"id": x.id, "name": x.name,
                    "buying_price": x.buying_price, "selling_price": x.selling_price}
            products_list.append(data)
        return jsonify(products_list), 200
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON  body!"}), 400

        name = data.get("name")
        buying_price = data.get("buying_price")
        selling_price = data.get("selling_price")

        if not name or buying_price is None or selling_price is None:
            return jsonify({"error": "Ensure all fields are set!"}), 400

        if Product.query.filter_by(name=name).first():
            return jsonify({"error": "Product already exists"}), 409

        if buying_price <= 0 or selling_price <= 0:
            return jsonify({"error": "Ensure price is positive"}), 400

        prod = Product(name=name, buying_price=buying_price,
                       selling_price=selling_price)
        db.session.add(prod)
        db.session.commit()
        return jsonify({"Id": prod.id})
    else:
        return jsonify("Method not allowed!"), 409


@app.route("/purchases", methods=["GET", "POST"])
def purchases():
    if request.method == "GET":
        purchases = Purchase.query.all()
        purchase_list = []
        for p in purchases:
            data = {}
            purchase_list.append(data)
        return jsonify(purchase_list), 200
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON method!"}), 400
        if "product_id" not in data or "quantity":
            return jsonify({"error": "Ensure all fields are set!"}), 400
        purch = Purchase()
        db.session.add(purch)
        db.session.commit()
        result = {}
        return jsonify(result), 200
    return jsonify({"": "Method not allowed!"}), 409


@app.route("/sales", methods=["GET", "POST"])
def sales():
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass
    else:
        return jsonify({"error": "Method not allowed!"}), 409


if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run()
