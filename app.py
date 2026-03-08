from flask import Flask, request, jsonify
from models import db, User, Product, Purchase, datetime
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
        data = request.get_json()
        if not data:
            return jsonify({"error": ""}), 400
        name = data.get("name")
        buying_price = data.get("buying_price")
        selling_price = data.get("selling_price")
        if not name or buying_price is None or selling_price is None:
            return jsonify({"error": "Ensure all fields are set!"}), 400
        if Product.query.filter_by(name=name).first():
            return jsonify({"": ""}), 400
        if buying_price <= 0 or selling_price <= 0:
            return jsonify({"error": "Ensure prices are positive"}), 400
        prod = Product(name=name, buying_price=buying_price,
                       selling_price=selling_price)
        db.session.add(prod)
        db.session.commit()
        return jsonify({"id": prod.id})
    return jsonify({"error": "Method not allowed"}), 405


@app.route("/purchases", methods=["GET", "POST"])
def purchases():
    if request.method == "GET":
        purchases = Purchase.query.all()
        purchases_list = []
        for p in purchases:
            data = {"product_id": p.product_id, "quantity": p.quantity,
                    "created_on": p.created_on.strftime("%Y-%m-%d %H:%M:%S")if p.created_on else None, "updated_on": p.updated_on.strftime("%Y-%m-%d %H:%M:%S")if p.updated_on else None}
            purchases_list.append(data)
        return jsonify(purchases_list), 200
    elif request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format!"}), 400
        if "quantity"not in data or "product_id" not in data:
            return jsonify({"error": "Ensure all fields are set!"}), 400
        purch = Purchase(
            product_id=data["product_id"], quantity=data["quantity"], created_on=data.get("created_on", datetime.utcnow()))
        db.session.add(purch)
        db.session.commit()
        result = {"id": purch.id, "product_id": purch.product_id, "quantity": purch.quantity,
                  "created_on": purch.created_on.strftime("%Y-%m-%d %H:%M:%S") if purch.created_on else None, "updated_on": purch.updated_on.strftime("%Y-%m-%d %H:%M:%S") if purch.updated_on else None}
        return jsonify(result), 201
    return jsonify({"error": "Method not allowed!"}), 405


if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run()
