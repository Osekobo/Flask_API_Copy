from flask import Flask, jsonify
from models import db, Products, Purchases
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'hgyutd576uyfutu'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:12039@localhost:5432/learning"
db.init_app(app)


@app.route("/")
def home():
    return ("Flask version 1.0")


@app.route("/products")
def products():
    product = Products.query.all()
    product_list = []
    for x in product:
        data = {"id": x.id, "name": x.name,
                "buying_price": x.buying_price, "selling_price": x.selling_price}
        product_list.append(data)
    return jsonify(product_list)


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
