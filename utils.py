import random


def format_phone(phone):
    phone = phone.strip()
    if phone.startswith("0"):
        return "+254" + phone[1:]
    elif phone.startswith("+"):
        return phone
    else:
        raise ValueError("Invalid phone number format")


def generate_otp_code():
    return str(random.randint(100000, 999999))
