from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Products, Purchases
app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'hgyutd576uyfutu'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:12039@localhost:5432/learning"
db.init_app(app)


@app.route("/")
def home():
    return ("Flask version 1.0")


@app.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "GET":
        product = Products.query.all()
        product_list = []
        for x in product:
            data = {"id": x.id, "name": x.name,
                    "buying_price": x.buying_price, "selling_price": x.selling_price}
            product_list.append(data)
        return jsonify(product_list)
    elif request.method == "POST":
        data = dict(request.get_json())
        if "name"not in data.keys() or "buying_price"not in data.keys() or "selling_price"not in data.keys():
            error = {"error": "Ensure all fields are set"}
            return jsonify(error), 400
        else:
            prod = Products(
                name=data["name"], buying_price=data["buying_price"], selling_price=data["selling_price"])
            db.session.add(prod)
            db.session.commit()
            data["id"] = prod.id
            return jsonify(data), 201
    else:
        error = {"error": "Method not allowed"}
        return jsonify(error), 405


@app.route("/purchases")
def purchases():
    purchases = Purchases.query.all()
    purchases_list = []
    for x in purchases:
        data = {"id": x.id, "quantity": x.quantity, "product_id": x.product_id,
                "created_at": x.created_at.strftime("%Y-%m-%d %H:%M:%S"), "updated_at": x.updated_at.strftime("%Y-%m-%d %H:%M:%S")}
        purchases_list.append(data)
        return jsonify(purchases_list)
    # return ("Purchase page")


if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
app.run()
