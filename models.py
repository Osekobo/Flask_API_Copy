from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


# class Product(db.Model):
#     __tablename__ = "products"
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     name = db.Column(db.String(256), nullable=False)
#     buying_price = db.Column(db.Float, nullable=False)
#     selling_price = db.Column(db.Float, nullable=False)


# class Purchase(db.Model):
#     __tablename__ = "purchases"
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     quantity = db.Column(db.Float, nullable=False)
#     product_id = db.Column(db.Integer, db.ForeignKey(
#         "products.id"), nullable=False)
#     created_on = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_on = db.Column(
#         db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# # class Sale(db.Model):
# #     __tablename__ = "sales"
# #     id = db.Column(db.Integer, primary_key=True, nullable=False)
# #     created_on = db.Column(db.DateTime, default=datetime.utcnow)
# #     updated_on = db.Column(
# #         db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
# class Sale(db.Model):
#     __tablename__ = "sales"
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     product_id = db.Column()
#     quantity = db.Column()
#     total = db.Column()


# class SalesDetails(db.Model):
#     __tablename__ = "sales_details"
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     sale_id = db.Column(db.Integer, db.ForeignKey("sales.id"), nullable=False)
#     product_id = db.Column(db.Integer, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     created_on = db.Column(db.DateTime, default=datetime.now)


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


# class OTP(db.Model):
#     __tablename__ = "otp"
#     id = db.Column()
#     user_id = db.Column()
#     otp = db.Column()
#     created_at = db.Column()

class OTP(db.Model):
    __tablename__ = "otps"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20))
    amount = db.Column(db.Float)
    checkout_request_id = db.Column(db.String(100))
    mpesa_receipt = db.Column(db.String(50))
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
