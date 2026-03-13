from flask import Flask, request, jsonify, Blueprint
from models import db, User, OTP, datetime
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
from datetime import timezone, timedelta
from utils import format_phone, generate_otp
app = Flask(__name__)
auth = Blueprint('auth', __name__)


@app.route("/")
def home():
    return ("Flask version 1.0")


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    if not all(k in data for k in ("name", "phone", "email", "password")):
        return jsonify({"error": "Ensure all fields are set!"}), 400
    email = data["email"].lower().strip()
    if User.query.filter_by(email=email).first():

        return jsonify({"error": "User already exists"}), 409
    usr = User()
    db.session.add(usr)
    db.session.commit()
    token = create_access_token(identity=usr.id)
    return jsonify({"message": "User registered", "Token": token}), 209


@app.route("/sales")
def sales():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    if not all(s in data for s in ("product_id", "quantity", "total")):
        return jsonify({"error": "Ensure all fields are set"}), 400


# Forgot Password Route
# (@auth.route)Tells Flask this function handles a URL endpoint.
@auth.route("/forgot_password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Email or phone is required"}), 400

    email = data.get("email")
    phone = data.get("phone")

    user = None
    contact_type = None

    if email:
        email = email.strip().lower()
        user = User.query.filter_by(email=email).first()
        contact_type = "email"

    elif phone:
        phone_raw = phone.strip()

        try:
            phone_formatted = format_phone(phone_raw)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        user = User.query.filter_by(phone=phone_formatted).first()
        contact_type = "phone"

    else:
        return jsonify({"error": "Email or phone is required"}), 400

    if not user:
        return jsonify({"message": "If user exists, an OTP has been sent"}), 200

    OTP.query.filter_by(user_id=user.id).delete()
    otp_code = generate_otp()
    otp_entry = OTP(
        user_id=user.id,
        otp=otp_code,
        created_at=datetime.now(timezone.utc)
    )
    db.session.add(otp_entry)
    db.session.commit()


# Verify OTP Route
@auth.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()

    if not data or not all(k in data for k in ("email", "otp")):
        return jsonify({"error": "Email and OTP required"}), 400

    email = data["email"].strip().lower()
    otp = data["otp"].strip()

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    otp_entry = OTP.query.filter_by(user_id=user.id, otp=otp).first()

    if not otp_entry:
        return jsonify({"error": "Invalid OTP"}), 400
    
    if datetime.now(timezone.utc) - otp_entry.created_on > timedelta(minutes=5):
        return jsonify({"error": "OTP expired"}), 400
    
    db.session.delete(otp_entry)
    db.session.commit()
    
    return jsonify({
        "message": "OTP verified successfully"
    }), 200


# Reset Password Route
@auth.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()

    if not data or not all(k in data for k in ("email", "otp", "new_password")):
        return jsonify({"error": "Email, OTP and new password required"}), 400

    email = data["email"].strip().lower()
    otp = data["otp"]
    new_password = data["new_password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    otp_entry = OTP.query.filter_by(user_id=user.id, otp=otp).first()

    if not otp_entry:
        return jsonify({"error": "Invalid OTP"}), 400

    user.password = generate_password_hash(new_password)

    db.session.delete(otp_entry)
    db.session.commit()

    return jsonify({
        "message": "Password reset successfully"
    }), 200



if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run()


# 200 → Success
# 201 → Created
# 400 → Bad request
# 401 → Unauthorized
# 404 → Not found
# 500 → Server error
