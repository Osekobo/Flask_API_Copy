import random


# def format_phone(phone):
#     phone = phone.strip()
#     if phone.startswith("0"):
#         return "+254" + phone[1:]
#     elif phone.startswith("+"):
#         return phone
#     else:
#         raise ValueError("Invalid phone number format")
def format_phone(phone):
    phone = phone.strip()

    # +254714391137
    if phone.startswith("+254"):
        return "0" + phone[4:]

    # 254714391137
    if phone.startswith("254"):
        return "0" + phone[3:]

    # already correct
    if phone.startswith("07") or phone.startswith("01"):
        return phone

    raise ValueError("Invalid Kenyan phone number")


def generate_otp_code():
    return str(random.randint(100000, 999999))
