from flask import Blueprint, request, jsonify
from models import Payment, db
from mpesa import stk_push

payment_bp = Blueprint("payments", __name__)


@payment_bp.route("/pay", methods=["POST"])
def pay():

    data = request.get_json()

    phone = data["phone"]
    amount = data["amount"]

    response = stk_push(phone, amount)

    checkout_id = response.get("CheckoutRequestID")

    payment = Payment(
        phone=phone,
        amount=amount,
        checkout_request_id=checkout_id
    )

    db.session.add(payment)
    db.session.commit()

    return jsonify(response)


@payment_bp.route("/api/mpesa/callback", methods=["POST"])
def mpesa_callback():

    data = request.get_json()

    callback = data["Body"]["stkCallback"]

    checkout_id = callback["CheckoutRequestID"]
    result_code = callback["ResultCode"]

    payment = Payment.query.filter_by(
        checkout_request_id=checkout_id
    ).first()

    if result_code == 0:

        items = callback["CallbackMetadata"]["Item"]

        receipt = None

        for item in items:
            if item["Name"] == "MpesaReceiptNumber":
                receipt = item["Value"]

        payment.status = "success"
        payment.mpesa_receipt = receipt

    else:
        payment.status = "failed"

    db.session.commit()

    return {"ResultCode": 0, "ResultDesc": "Accepted"}
