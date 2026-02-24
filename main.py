from flask import Flask, request, jsonify
from models import db, Product, Purchase, datetime, User
from flask_cors import CORS
from collections import defaultdict
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager,create_access_token
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'hgyutd576uyfutu'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:12039@localhost:5432/learning"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
CORS(app)

jwt = JWTManager(app)

@app.route("/")
def home():
    return ("Flask version: 1.0"), 200


@app.route("/register", methods=["POST"])
def register():
    data = dict(request.get_json())
    if "name"not in data.keys() or "phone"not in data.keys() or "email"not in data.keys() or "password"not in data.keys():
        error = {"error": "Ensure all fields are set!"}
        return jsonify(error), 400
    elif User.query.filter_by(email=data["email"]).first() is not None:
        error = {"error": "User with email already exists!"}
        return jsonify(error), 409
    else:
        usr = User(name=data["name"], phone=data["phone"],
                   email=data["email"], password=generate_password_hash(data["password"]))
        db.session.add(usr)
        db.session.commit()
        data["id"] = usr.id
        token = create_access_token(data["email"])
        message = {"message": "User registered successfully!"}
        return jsonify(message, {"token": token}), 201


@app.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "GET":
        product = Product.query.all()
        product_list = []
        for x in product:
            data = {"id": x.id, "name": x.name,
                    "buying_price": x.buying_price, "selling_price": x.selling_price}
            product_list.append(data)
            return jsonify(product_list), 200
    elif request.method == "POST":
        data = dict(request.get_json())
        if "name" not in data.keys() or "buying_price"not in data.keys() or "selling_price"not in data.keys():
            error = {"error": "Ensure all fields are set!"}
            return jsonify(error), 400
        else:
            prod = Product(
                name=data["name"], selling_price=data["selling_price"], buying_price=data["buying_price"])
            db.session.add(prod)
            db.session.commit()
            data["id"] = prod.id
            return jsonify(data), 201
    else:
        error = {"error": "Method not allowed!"}
        return jsonify(error), 405


@app.route("/purchases", methods=["GET", "POST"])
def purchases():
    if request.method == "GET":
        purchase = Purchase.query.all()
        purchase_list = []
        for p in purchase:
            data = {"quantity": p.quantity, "product_id": p.product_id,
                    "created_on": p.created_on, "updated_on": p.updated_on}
            purchase_list.append(data)
            return jsonify(purchase_list), 200
    elif request.method == "POST":
        data = dict(request.get_json())
        if "created_on"not in data.keys():
            data["created_on"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pass
        if "quantity" not in data.keys() or "product_id"not in data.keys():
            error = {"error": "Ensure all fields are set!"}
            return jsonify(error), 400
        else:
            data = Purchase(
                product_id=data["product_id"], quantity=data["quantity"])
            db.session.add(data)
            db.session.commit()
            data["id"] = data.id
            data["updated_on"] = data.updated_on.strftime("%Y-%m-%d %H:%M:%S")
            return jsonify(data), 201
    else:
        error = {"error": "Method not allowed!"}
        return jsonify(error), 405
    return ("")


@app.route("/sales", methods=["GET", "POST"])
def sales():
    if request.method == "GET":
        results = ()
        sales_list = defaultdict(list)
        pass
    elif request.method == "POST":
        pass
    else:
        error = {"error": "Method not allowed!"}
        return jsonify(error), 405


if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run()
