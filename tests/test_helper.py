import pytest
from app import db, helper, models_orm

@pytest.mark.parametrize(
    'username, user_type, expected',
    [
        ('moe_m', 'customer', models_orm.Customer),
        ('doe_m', 'corporate_customer', models_orm.CorporateCustomer),
        ('steve_j', 'staff', models_orm.Staff),
    ]
)
def test_get_one_user(username, user_type, expected):
    with db.get_db() as db_session:
        user = helper.get_one_user(db_session, username, user_type)
        assert isinstance(user, expected)

def test_get_all_users():
    with db.get_db() as db_session:
        users = helper.get_all_users(db_session)
        assert all(isinstance(user, models_orm.Person) for user in users)

def test_get_all_products():
    with db.get_db() as db_session:
        veggie_list, premade_box_list = helper.get_all_products(db_session)
        assert all(isinstance(veggie, models_orm.Veggie) for veggie in veggie_list)
        assert all(isinstance(premade_box, models_orm.PremadeBox) for premade_box in premade_box_list)

@pytest.mark.parametrize(
    'product_id, expected',
    [
        (1, models_orm.Veggie),
        (15, models_orm.PremadeBox),
    ]
)
def test_get_one_product(product_id, expected):
    with db.get_db() as db_session:
        veggie = helper.get_one_product(db_session, product_id)
        assert isinstance(veggie, expected)

def test_get_all_orders():
    with db.get_db() as db_session:
        orders = helper.get_all_orders(db_session)
        assert all(isinstance(order, models_orm.Order) for order in orders)

def test_get_one_order():
    with db.get_db() as db_session:
        order = helper.get_one_order(db_session, 1)
        assert isinstance(order, models_orm.Order)

def test_get_all_payments():
    with db.get_db() as db_session:
        payments = helper.get_all_payments(db_session)
        assert all(isinstance(payment, models_orm.Payment) for payment in payments)

def test_create_order(order_obj_for_cus):
    with db.get_db() as db_session:
        order = helper.create_order(db_session, order_obj_for_cus, 20)
        assert isinstance(order, models_orm.Order)

@pytest.mark.parametrize(
    "order_id, item_id, quantity, expected",
    [
        (1, 1, 8, models_orm.OrderLine),
        (1, 2, 7, models_orm.OrderLine),
        (1, 3, 6, models_orm.OrderLine),
    ]
)
def test_create_orderline(order_id, item_id, quantity, expected):
    with db.get_db() as db_session:
        orderline = helper.create_orderline(db_session, order_id, item_id, quantity)
        assert isinstance(orderline, expected)

def test_create_payment(payment_obj):
    with db.get_db() as db_session:
        payment = helper.create_payment(db_session, payment_obj, 20)
        assert isinstance(payment, models_orm.Payment)
