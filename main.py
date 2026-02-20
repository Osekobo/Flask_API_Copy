from models import db, Product, Purchases
from flask import Flask, jsonify
app = Flask(__name__)


app.config['JWT_SECRET_KEY'] = 'hgyutd576uyfutu'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:12039@localhost:5432/leaning"
db.init_app(app)


@app.route("/")
def home():
    return ("Flask Version 1.0")


@app.route("/products")
def products():
    products = Product.query.all()
    products_list = []
    for x in products:
        data = {"id": x.id, "name": x.name,
                "buying_price": x.buying_price, "selling_price": x.selling_price}
        products_list.append(data)
    return jsonify(products_list), 200


@app.route("/purchases")
def purchases():
    purchases = Purchases.query.all()
    purchase_list = []
    for x in purchases:
        data = {"id": x.id, "quantity": x.quantity,
                "created_at": x.created_at.strftime("%Y-%m-%d %H:%M:%S"), "updated_at": x.updated_at.strftime("%Y-%m-%d %H:%M:%S")}
        purchase_list.append(data)
    return jsonify(purchase_list), 200


@app.route("/sales")
def sale():
    return ("sales page")


if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run()
