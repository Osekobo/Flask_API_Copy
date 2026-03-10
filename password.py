from flask import Blueprint, request, jsonify
from models import db, User, datetime, OTP
from datetime import timezone
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
