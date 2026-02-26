from flask import Flask, request, jsonify
from models import db, Product, Purchase, datetime, User, Sale, SalesDetails
from flask_cors import CORS
from collections import defaultdict
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token
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
    data = request.get_json()

    if not data:
        return jsonify({"error": "Send JSON body"}), 400

    if not all(k in data for k in ("name", "phone", "email", "password")):
        return jsonify({"error": "Ensure all fields are set!"}), 400

    email = data["email"].lower().strip()

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User with email already exists!"}), 409

    usr = User(
        name=data["name"],
        phone=data["phone"],
        email=email,
        password=generate_password_hash(data["password"])
    )

    db.session.add(usr)
    db.session.commit()

    token = create_access_token(identity=usr.id)

    return jsonify({
        "message": "User registered successfully!",
        "token": token
    }), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Ensure all fields are set!"}), 400

    email = data.get("email").lower().strip()
    password = data.get("password")

    usr = User.query.filter_by(email=email).first()

    if not usr or not check_password_hash(usr.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity=usr.id)

    return jsonify({"token": token}), 200


@app.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "GET":
        products = Product.query.all()
        product_list = []

        for x in products:
            data = {
                "id": x.id,
                "name": x.name,
                "buying_price": x.buying_price,
                "selling_price": x.selling_price,
            }
            product_list.append(data)

        return jsonify(product_list), 200

    elif request.method == "POST":
        data = request.get_json()

        if not data:
            return jsonify({"error": "Send JSON body"}), 400

        name = data.get("name")
        buying_price = data.get("buying_price")
        selling_price = data.get("selling_price")

        if not name or buying_price is None or selling_price is None:
            return jsonify({"error": "Ensure all fields are set!"}), 400

        if buying_price < 0 or selling_price < 0:
            return jsonify({"error": "Prices must be positive"}), 400

        prod = Product(
            name=name,
            selling_price=selling_price,
            buying_price=buying_price,
        )

        db.session.add(prod)
        db.session.commit()

        return jsonify({"id": prod.id}), 201

    return jsonify({"error": "Method not allowed"}), 405


@app.route("/purchases", methods=["GET", "POST"])
def purchases():
    if request.method == "GET":
        purchases = Purchase.query.all()
        purchase_list = []

        for p in purchases:
            data = {
                "id": p.id,
                "quantity": p.quantity,
                "product_id": p.product_id,
                "created_on": p.created_on.strftime("%Y-%m-%d %H:%M:%S") if p.created_on else None,
                "updated_on": p.updated_on.strftime("%Y-%m-%d %H:%M:%S") if p.updated_on else None,
            }
            purchase_list.append(data)

        return jsonify(purchase_list), 200

    elif request.method == "POST":
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON body"}), 400

        if "quantity" not in data or "product_id" not in data:
            return jsonify({"error": "Ensure all fields are set!"}), 400

        new_purchase = Purchase(
            product_id=data["product_id"],
            quantity=data["quantity"],
            created_on=data.get("created_on", datetime.utcnow())
        )

        db.session.add(new_purchase)
        db.session.commit()

        response = {
            "id": new_purchase.id,
            "product_id": new_purchase.product_id,
            "quantity": new_purchase.quantity,
            "created_on": new_purchase.created_on.strftime("%Y-%m-%d %H:%M:%S") if new_purchase.created_on else None,
            "updated_on": new_purchase.updated_on.strftime("%Y-%m-%d %H:%M:%S") if new_purchase.updated_on else None,   
        }
        return jsonify(response), 201

    return jsonify({"error": "Method not allowed!"}), 405


@app.route("/sales", methods=["GET", "POST"])
def sales():
    if request.method == "GET":
        results = (
            db.session.query(Sale, SalesDetails, Product)
            .join(SalesDetails, SalesDetails.sale_id == Sale.id)
            .join(Product, Product.id == SalesDetails.product_id)
            .order_by(Sale.created_at.desc())
            .all()
        )

        sales_group = defaultdict(list)
        for sale, detail, product in results:
            sales_group[sale.id].append((sale, detail, product))

        result = [
            {
                "sale_id": sale.id,
                "created_at": sale.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "items": [
                    {
                        "product_id": product.id,
                        "product_name": product.name,
                        "quantity": detail.quantity,
                    }
                    for _, detail, product in grouped
                ],
            }
            for sale_id, grouped in sales_group.items()
            for sale, _, _ in [grouped[0]]
        ]

        return jsonify(result), 200

    elif request.method == "POST":
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON body"}), 400

            sales_data = data.get("sales", [])
            if not sales_data or not isinstance(sales_data, list):
                return jsonify({"error": "Request must include a 'sales' list"}), 400

            # ✅ validate first
            for item in sales_data:
                product_id = item.get("product_id")
                quantity = item.get("quantity")

                if product_id is None or quantity is None or quantity <= 0:
                    return jsonify({"error": "Each sale must include valid product_id and quantity"}), 400

            # ✅ create sale after validation
            sale = Sale()
            db.session.add(sale)
            db.session.flush()

            created_details = []

            for item in sales_data:
                detail = SalesDetails(
                    sale_id=sale.id,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                )
                db.session.add(detail)

                created_details.append({
                    "product_id": detail.product_id,
                    "quantity": detail.quantity,
                })

            db.session.commit()

            return jsonify({
                "message": "Sales added successfully",
                "sale_id": sale.id,
                "details": created_details
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Method not allowed"}), 405


@app.route("/sales", methods=["GET", "POST"])
def sales():
    if request.method == "GET":
        results = (db.session.query(Sale, SalesDetails,
                   Product).join(SalesDetails, SalesDetails.sale_id == Sale.id).join(Product, Product.id == SalesDetails.product_id).order_by(Sale.created_on.desc()).all())
        sales_group = defaultdict(list)
        for sale, detail, product in results:
            sales_group[sale.id].append((Sale, detail, product))
        result = [{"sale_id": sale.id, "created_on": sale.created_on.strftime(), "items": [
            {"product_id": product.id, "product_name": product.name, "quantity": detail.quantity, }for _, detail, product in grouped], }for sale_id, grouped in sales_group.items()
            for sale, _, _ in [grouped[0]]]
        return jsonify(result), 200
    elif request.method == "POST":
        try:
            data = request.get_json()
            if not data:
                return ({"error": "Invalid JSON body"}), 400
            sales_data = data.get("sales", [])
            if not sales_data or not isinstance(sales_data, list):
                return jsonify({"error": "Request must include a 'sales'list"}), 400
            for item in sales_data:
                product_id = item.get("product_id")
                quantity = item.get("quantity")
                if product_id is None or quantity is None or quantity <= 0:
                    return jsonify({"error": "Each sale must include valid product_id and quantity"}), 400
            sale = Sale()
            db.session.add(Sale)
            db.session.flush()
            created_details = []
            for item in sales_data:
                detail = SalesDetails(
                    sale_id=sale.id,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                )
                db.session.add(detail)
                created_details.append({
                    "product_id": detail.product_id,
                    "quantity": detail.quantity,
                })
                db.session.commit()
                return jsonify({
                    "message": "Sales added su",
                    "sale_id": sale.id,
                    "details": created_details
                }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Method not allowed!"}), 405


if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run()
