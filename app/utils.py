'''utility functions for the application'''

import datetime
import re
import bcrypt

def validate_name(name):
    pattern = r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$"
    return bool(re.fullmatch(pattern, name.strip()))

def validate_address(address):
    pattern = r"^[A-Za-z0-9À-ÖØ-öø-ÿ',.\-/ ]+$"
    return bool(re.fullmatch(pattern, address.strip()))

def validate_card_number(card_number):
    return bool(re.fullmatch(r"\d{13,19}", card_number))

def validate_expiry_date(expiry_date):
    try:
        date_obj = convert_str_to_date(expiry_date)
        return date_obj > datetime.date.today()
    except ValueError:
        return False
        
def generate_hashed_password(password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password

def verify_password(password, correct_password):
    return bcrypt.checkpw(password.encode('utf-8'), correct_password.encode('utf-8'))

def conver_decimal_to_percentage(decimal):
    return "{:.0f}%".format(decimal * 100)

def get_current_date():
    return datetime.date.today().strftime('%d-%m-%Y')

def convert_str_to_date(date_str):
    return datetime.datetime.strptime(date_str, '%d-%m-%Y').date()

def convert_date_to_str(date):
    return date.strftime('%d-%m-%Y')

def is_within_week(date):
    today = datetime.date.today()
    return (today - date).days <= 7

def is_within_month(date):
    today = datetime.date.today()
    return (today - date).days <= 30

def is_within_quarter(date):
    today = datetime.date.today()
    return (today - date).days <= 90

def is_within_year(date):
    today = datetime.date.today()
    return (today - date).days <= 365