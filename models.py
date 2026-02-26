from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    buying_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)


class Purchase(db.Model):
    __tablename__ = "purchases"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "products.id"), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Sale(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SalesDetails(db.Model):
    __tablename__ = "sales_details"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sale_id = db.Column(db.Integer, db.ForeignKey("sales.id"), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# @app.route("/sales", methods=["GET", "POST"])
# def sales():
#     if request.method == "GET":
#         results = (
#             db.session.query(Sale, SalesDetails, Product)
#             .join(SalesDetails, SalesDetails.sale_id == Sale.id)
#             .join(Product, Product.id == SalesDetails.product_id)
#             .order_by(Sale.created_at.desc())
#             .all()
#         )

#         sales_group = defaultdict(list)
#         for sale, detail, product in results:
#             sales_group[sale.id].append((sale, detail, product))

#         result = [
#             {
#                 "sale_id": sale.id,
#                 "created_at": sale.created_at.strftime("%Y-%m-%d %H:%M:%S"),
#                 "items": [
#                     {
#                         "product_id": product.id,
#                         "product_name": product.name,
#                         "quantity": detail.quantity,
#                     }
#                     for _, detail, product in grouped
#                 ],
#             }
#             for sale_id, grouped in sales_group.items()
#             for sale, _, _ in [grouped[0]]
#         ]

#         return jsonify(result), 200

#     elif request.method == "POST":
#         try:
#             data = request.get_json()
#             if not data:
#                 return jsonify({"error": "Invalid JSON body"}), 400

#             sales_data = data.get("sales", [])
#             if not sales_data or not isinstance(sales_data, list):
#                 return jsonify({"error": "Request must include a 'sales' list"}), 400

            
#             for item in sales_data:
#                 product_id = item.get("product_id")
#                 quantity = item.get("quantity")

#                 if product_id is None or quantity is None or quantity <= 0:
#                     return jsonify({"error": "Each sale must include valid product_id and quantity"}), 400

            
#             sale = Sale()
#             db.session.add(sale)
#             db.session.flush()

#             created_details = []

#             for item in sales_data:
#                 detail = SalesDetails(
#                     sale_id=sale.id,
#                     product_id=item["product_id"],
#                     quantity=item["quantity"],
#                 )
#                 db.session.add(detail)

#                 created_details.append({
#                     "product_id": detail.product_id,
#                     "quantity": detail.quantity,
#                 })

#             db.session.commit()

#             return jsonify({
#                 "message": "Sales added successfully",
#                 "sale_id": sale.id,
#                 "details": created_details
#             }), 201

#         except Exception as e:
#             db.session.rollback()
#             return jsonify({"error": str(e)}), 500

#     return jsonify({"error": "Method not allowed"}), 405