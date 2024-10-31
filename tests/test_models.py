from app import models, utils

def test_create_customer(customer_obj):
    assert customer_obj.first_name == 'Archie'
    assert customer_obj.balance == 0.0
    assert customer_obj.owing == 0.0
    assert customer_obj.credit_limit == 100.0
    assert customer_obj.available_credit == 100.0

def test_update_customer(customer_obj):
    customer_obj.balance = 10.0
    customer_obj.owing = 5.0
    assert customer_obj.balance == 10.0
    assert customer_obj.owing == 5.0

def test_create_corporate_customer(corporate_customer_obj):
    assert corporate_customer_obj.first_name == 'John'
    assert corporate_customer_obj.credit_limit == 200.0
    assert corporate_customer_obj.owing == 0.0
    assert corporate_customer_obj.available_credit == 200.0
    assert hasattr(corporate_customer_obj, 'discount')
    assert corporate_customer_obj.discount == 0.1

def test_create_staff():
    staff = models.Staff(
        fname='Karen', lname='Lee',
        username='karen_l', password='abcdefg',
        dept='People and Culture')
    assert staff.first_name == 'Karen'
    assert staff.date_joined == utils.get_current_date()   

def test_create_veggie(product_obj):
    assert product_obj.name == 'Apple'
    assert product_obj.price == 3.0

def test_update_veggie(product_obj):
    product_obj.price = 4.0
    assert product_obj.price == 4.0

def test_create_premadebox():
    product = models.PremadeBox(size='small')
    assert product.name == 'Premade box'
    assert hasattr(product, 'price')

def test_create_order_for_cus(order_obj_for_cus):
    assert isinstance(order_obj_for_cus, models.Order)
    assert order_obj_for_cus.customer.first_name == 'Archie'
    assert order_obj_for_cus.status == 'processing'
    assert order_obj_for_cus.delivery == True
    assert order_obj_for_cus.delivery_fee == 10

def test_create_order_for_corpcus(order_obj_for_corpcus):
    assert isinstance(order_obj_for_corpcus, models.Order)
    assert order_obj_for_corpcus.customer.first_name == 'John'
    assert order_obj_for_corpcus.status == 'processing'
    assert order_obj_for_corpcus.delivery == True
    assert order_obj_for_corpcus.delivery_fee == 10

def test_create_orderline(orderline_obj):
    assert orderline_obj.item.name == 'Apple'
    assert orderline_obj.quantity == 5
    assert hasattr(orderline_obj, 'subtotal')

def test_append_orderline_to_order_cus(order_obj_for_cus, orderline_obj):
    order_obj_for_cus.add_orderline(orderline_obj)
    assert len(order_obj_for_cus.orderline_list) == 1
    assert order_obj_for_cus.orderline_list[0].item.name == 'Apple'

def test_order_calculate_total_cus(order_obj_for_cus, orderline_obj):
    order_obj_for_cus.add_orderline(orderline_obj)
    assert hasattr(order_obj_for_cus.customer, 'discount') == False
    assert order_obj_for_cus.orderline_list[0].subtotal == 15
    assert order_obj_for_cus.delivery_fee == 10
    assert order_obj_for_cus.calculate_total() == 25

def test_append_orderline_to_order_corpcus(order_obj_for_corpcus, orderline_obj):
    order_obj_for_corpcus.add_orderline(orderline_obj)
    assert len(order_obj_for_corpcus.orderline_list) == 1
    assert order_obj_for_corpcus.orderline_list[0].item.name == 'Apple'

def test_order_calculate_total_copcus(order_obj_for_corpcus, orderline_obj):
    order_obj_for_corpcus.add_orderline(orderline_obj)
    assert order_obj_for_corpcus.customer.discount == 0.1
    assert order_obj_for_corpcus.orderline_list[0].subtotal == 15
    assert order_obj_for_corpcus.delivery_fee == 10
    assert order_obj_for_corpcus.calculate_total() == 23.5
    assert order_obj_for_corpcus.total == 23.5

def test_create_payment(payment_obj):
    assert isinstance(payment_obj, models.Payment)
    assert payment_obj.amount == 25
    assert payment_obj.customer.first_name == 'Archie'

def test_customer_make_payment(customer_obj, payment_obj):
    assert customer_obj.balance == 0.0
    assert customer_obj.owing == 0.0
    assert customer_obj.available_credit == 100.0
    customer_obj.make_payment(payment_obj)
    assert customer_obj.balance == 0.0
    assert customer_obj.owing == payment_obj.amount
    assert customer_obj.available_credit == 100.0 - payment_obj.amount
