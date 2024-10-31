import pytest
from app import app, models

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def customer_obj():
    data = {
        'fname': 'Archie',
        'lname': 'Grande',
        'username': 'archie_g',
        'password': '123456',
        'address': '123 Main St, Auckland',
        'balance': 0.0,
    }
    customer = models.Customer(**data)
    return customer

@pytest.fixture
def corporate_customer_obj():
    data = {
        'fname': 'John',
        'lname': 'Doe',
        'username': 'john_d',
        'password': 'abcdefg',
        'address': '456 Low St, Auckland',
        'balance': 0,
    }
    customer = models.CorporateCustomer(**data)
    return customer

@pytest.fixture
def order_obj_for_cus(customer_obj):
    data = {
        'customer': customer_obj,
        'date': '01-01-2024',
        'status': 'processing',
        'delivery': True,
    }
    order = models.Order(**data)
    return order

@pytest.fixture
def order_obj_for_corpcus(corporate_customer_obj):
    data = {
        'customer': corporate_customer_obj,
        'date': '01-01-2024',
        'status': 'processing',
        'delivery': True,
    }
    order = models.Order(**data)
    return order

@pytest.fixture
def payment_obj(customer_obj):
    data = {
        'amount': 25,
        'date': '01-01-2024',
        'customer': customer_obj,
    }
    payment = models.Payment(**data)
    return payment

@pytest.fixture
def product_obj():
    data = {
        'name': 'Apple',
        'price': 3.0,
        'url': 'static/img/apple.jpg',
    }
    product = models.WeightedVeggie(**data)
    return product

@pytest.fixture
def orderline_obj(product_obj):
    data = {
        'item': product_obj,
        'quantity': 5,
    }
    orderline = models.OrderLine(**data)
    return orderline