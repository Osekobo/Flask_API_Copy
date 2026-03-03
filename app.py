from flask import Flask, request, jsonify
from models import Product, User
app = Flask(__name__)


@app.route("/")
def home():
    return ("Flask Version 1.0")


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data!"}), 409

    email = User.query.filter_by(email=email).first()
    pass


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data!"}), 400

    email = data.get("email")
    password = data.get("password")
    pass


@app.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "GET":
        products = Product.query.all()
        products_list = []
        for p in products:
            data = {}
            products_list.append(data)
        return jsonify(products_list), 200
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON  body!"}), 400

        name = name
        buying_price = buying_price
        selling_price = selling_price

        if buying_price < 0 or selling_price < 0:
            return jsonify({"error": "Ensure price is positive"})
        pass
    else:
        return jsonify("Method not allowed!"), 409


@app.route("/purchases", methods=["GET", "POST"])
def purchases():
    if request.method=="GET":
        pass
    if request.method=="POST":
        pass
    return jsonify({"":"Method not allowed!"}),400


@app.route("/sales")
def sales():
    pass


if __name__ == "__main__":
    app.run()
