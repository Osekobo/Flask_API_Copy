from flask import Blueprint, request, jsonify
from models import db, User, datetime, OTP
from datetime import timezone, timedelta
from utils import format_phone, generate_otp_code
from werkzeug.security import generate_password_hash
auth = Blueprint('auth', __name__)


@auth.route("/forgot_password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Email or phone required"}), 400

    email = data.get("email")
    phone = data.get("phone")

    user = None
    contact_type = None

    if email:
        email = email.lower().strip()
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
        return jsonify({"error": "Email or phone required"}), 400
    if not user:
        return jsonify({"message": "If user exists, an OTP has been sent"}), 200
    OTP.query.filter_by(user_id=user.id).delete()
    otp_code = generate_otp_code()
    otp_entry = OTP(user_id=user.id, otp=otp_code,
                    created_on=datetime.now(timezone.utc))
    db.session.add(otp_entry)
    db.session.commit()


@auth.route("/verify_otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Email and OTP required"}), 400

    if not all(t in data for t in ("email", "otp")):
        return jsonify({"error": "Email and OTP required"}), 400

    email = data["email"].lower().strip()
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

    return jsonify({"message": "OTP verified successfully"}), 200


@auth.route("/reset_password", methods=["POST"])
def reset_password():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Email, OTP and password required"}), 400

    email = data["email"].lower().strip()
    otp = data["otp"].strip()
    new_password = data["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    otp_entry = User.query.filter_by(user_id=user.id, otp=otp).first()

    if not otp_entry:
        return jsonify({"error": "Invalid OTP"}), 400

    user.password = generate_password_hash(new_password)

    db.session.add(otp_entry)
    db.session.commit()
    
    return jsonify({"message": "Password reset successfully"}), 200
