from flask import Flask, request, jsonify, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, JWTManager
from models import db, User, OTP
from utils import format_phone, generate_otp_code
from datetime import datetime, timezone
app = Flask(__name__)
auth = Blueprint('auth', __name__)

app.config['JWT_SECRET_KEY'] = 'hgyutd576uyfutu'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:12039@localhost:5432/learning"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
jwt = JWTManager(app)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "phone", "email", "password")):
        return jsonify({"error": "Ensure all fields are set"}), 400
    email = data.get("email").lower().strip()
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409
    usr = User(name=data["name"], phone=data["phone"], email=email,
               password=generate_password_hash(data["password"]))
    token = create_access_token(identity=usr.id)
    db.session.add(usr)
    db.session.commit()
    return jsonify({"message": "User registered successfully", "Token": token}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"error": "Email or phone required"}), 400
    email = data.get("email").lower().strip()
    password = data.get("password").strip()
    usr = User.query.filter_by(email=email).first()
    if not usr or not check_password_hash(usr.password, password):
        return jsonify({"error": "Invalid email or password"}), 401
    token = create_access_token(identity=usr.id)
    return jsonify({"message": "Login successful", "Token": token}), 200


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
        raw_phone = phone.strip()
        try:
            phone_formatted = format_phone(raw_phone)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        user = User.query.filter_by(phone=phone_formatted).first()
        contact_type = "phone"
    else:
        return jsonify({"error": "Email or phone required"}), 400

    if not user:
        return jsonify({"message": "If user exists, an OTP has been sent"}), 200

    OTP.query.filter_by(user_id=user.id).delete()
    # db.flush()
    otp_code = generate_otp_code()
    otp_entry = OTP(user_id=user.id, otp=otp_code,
                    created_on=datetime.now(timezone.utc))
    db.session.add(otp_entry)
    db.session.commit()
    return jsonify({"message": f"OTP sent to {contact_type}"}), 200


@auth.route("/verify_otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    if not data or not all(k in data for k in ("email", "otp")):
        return jsonify({"error": "OTP and password required"}), 400
    email = data.get("email").lower().strip()
    otp = data.get("otp").strip().replace("", "")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    otp_entry = OTP.query.filter_by(user_id=user.id, otp=otp).first()
    if not otp_entry or otp_entry.otp != otp:
        return jsonify({"error": "Invalid OTP"}), 400
    # db.session.add(otp_entry)
    # db.session.commit()
    return jsonify({"message": "OTP verified successfully"}), 200


@auth.route("/reset_password", methods=["POST"])
def reset_password():
    data = request.get_json()
    if not data or not all(k in data for k in ("email", "otp", "new_password")):
        return jsonify({"error": ""}), 400
    email = data.get("email").lower().strip()
    otp = data.get("otp").strip().replace("", "")
    new_password = data.get("new_password")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    otp_entry = OTP.query.filter_by(user_id=user.id, otp=otp).first()
    if not otp_entry:
        return jsonify({"error": "Invalid OTP"}), 400
    user.password = generate_password_hash(new_password)
    db.session.delete(otp_entry)
    db.session.commit()
    return jsonify({"message": "Password reset successfully"}), 200


app.register_blueprint(auth)
if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run()
