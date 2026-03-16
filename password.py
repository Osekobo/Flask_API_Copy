from flask import Flask, request, jsonify, Blueprint
from models import User, db, OTP
from flask_jwt_extended import create_access_token, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from utils import generate_otp_code, format_phone
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
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    if not all(t in data for t in ("name", "phone", "email", "password")):
        return jsonify({"error": "Ensure all fields are set!"}), 400
    email = data.get("email", "").lower().strip()
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400
    usr = User(name=data["name"], phone=data["phone"],
               email=email, password=generate_password_hash(data["password"]))
    db.session.add(usr)
    db.session.commit()
    token = create_access_token(identity=usr.id)
    return jsonify({"Message": "User registered successfully", "token": token}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    if not "email" in data or not "password" in data:
        return jsonify({"error": "Ensure all fields are set"}), 400

    email = data.get("email").lower().strip()
    password = data.get("password")
    usr = User.query.filter_by(email=email).first()
    if not usr or not check_password_hash(usr.password, password):
        return jsonify({"error": "Invalid email or password"}), 409
    # user=User(email=email,pa)
    token = create_access_token(identity=usr.id)
    return jsonify({"Message": "Login successful", "Token": token}), 200


@auth.route("/forgot_password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    # print("REQUEST DATA:", data)
    if not data:
        return jsonify({"error": "Email or phone is required"}), 400
    email = data.get("email", "")
    phone = data.get("phone")
    contact_type = None
    user = None
    if email:
        email = email.lower().strip()
        user = User.query.filter_by(email=email).first()
        contact_type = "email"
    elif phone:
        phone_raw = phone.strip() if phone else None
        try:
            phone_formatted = format_phone(phone_raw)
            # print("FORMATTED PHONE:", phone_formatted)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        user = User.query.filter_by(phone=phone_formatted).first()
        contact_type = "phone"
    else:
        return jsonify({"error": "Phone or Email is required"}), 400
    if not user:
        return jsonify({"error": "If user exists, an OTP has been sent"}), 200
    OTP.query.filter_by(user_id=user.id).delete()
    otp_code = generate_otp_code()
    otp_entry = OTP(user_id=user.id, otp=otp_code,
                    created_on=datetime.now(timezone.utc))
    db.session.add(otp_entry)
    db.session.commit()
    return jsonify({"Message": f"OTP sent through {contact_type}"}), 200


@auth.route("/verify_otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    if not data:
        return jsonify({"": ""}), 400


@auth.route("/reset_password", methods=["POST"])
def reset_password():
    data = request.get_json()
    if not data:
        return jsonify({"": ""}), 400


app.register_blueprint(auth)
if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run()
