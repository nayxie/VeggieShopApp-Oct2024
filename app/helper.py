'''service functions for the application'''

from sqlalchemy import func
from app import models, models_orm, utils


def get_one_user(db_session, username, user_type):
    if user_type == "staff":
        staff = db_session.query(models_orm.Staff).filter(models_orm.Staff.username == username).first()
        return staff
    if user_type == "customer":
        customer = db_session.query(models_orm.Customer).filter(models_orm.Customer.username == username).first()
        return customer
    if user_type == "corporate_customer":
        corporate_customer = db_session.query(models_orm.CorporateCustomer).filter(models_orm.CorporateCustomer.username == username).first()
        return corporate_customer
    if user_type == "any":
        person = db_session.query(models_orm.Person).filter(models_orm.Person.username == username).first()
        return person

def get_all_users(db_session):
    user_list = db_session.query(models_orm.Person).all()
    return user_list

def get_all_customers(db_session):
    customer_list = db_session.query(models_orm.Customer).all()
    return customer_list

def format_user_profile(user):
    if user.type == 'customer':
        user_profile = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'address': user.address,
            'balance': user.balance,
            'credit_limit': user.credit_limit,
            'available_credit': user.available_credit,
            'owing': user.owing,
            'user_type': user.type
        }
    elif user.type == 'corporate_customer':
        converted_discount = utils.conver_decimal_to_percentage(user.discount)
        user_profile = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'address': user.address,
            'balance': user.balance,
            'credit_limit': user.credit_limit,
            'available_credit': user.available_credit,
            'owing': user.owing,
            'discount': converted_discount,
            'user_type': user.type
        }
    elif user.type == 'staff':
        user_profile = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'department': user.department.capitalize(),
            'date_joined': user.date_joined,
            'user_type': user.type
        }
    return user_profile

def get_all_products(db_session):
    weighted_veggie_list = db_session.query(models_orm.WeightedVeggie).all()
    pack_veggie_list = db_session.query(models_orm.PackVeggie).all()
    unit_veggie_list = db_session.query(models_orm.UnitPriceVeggie).all()
    veggie_list = weighted_veggie_list + pack_veggie_list + unit_veggie_list

    premade_box_list = db_session.query(models_orm.PremadeBox).all()

    return veggie_list, premade_box_list

def get_one_product(db_session, item_id):
    item = db_session.query(models_orm.Item).filter(models_orm.Item.id == item_id).first()    
    return item

def get_all_orders(db_session):
    order_list = db_session.query(models_orm.Order).order_by(func.str_to_date(models_orm.Order.date, '%d-%m-%Y').desc()).all()
    return order_list

def get_one_order(db_session, order_id):
    order = db_session.query(models_orm.Order).filter(models_orm.Order.id == order_id).first()
    return order

def get_all_orders_with_user_details(db_session):
    order_list = (
        db_session.query(models_orm.Order, models_orm.Person)
        .join(models_orm.Person, models_orm.Order.person_id == models_orm.Person.id)
        .order_by(func.str_to_date(models_orm.Order.date, '%d-%m-%Y').desc())
        .all()
    )
    return order_list

def get_user_orders(db_session, user_id):
    order_list = db_session.query(models_orm.Order).filter(models_orm.Order.person_id == user_id).order_by(func.str_to_date(models_orm.Order.date, '%d-%m-%Y').desc()).all()
    return order_list

def get_all_payments(db_session):
    payment_list = db_session.query(models_orm.Payment).all()
    return payment_list

def create_order(order, user_id):
    order_orm = models_orm.Order(person_id=user_id, total=order.total, date=order.date, status=order.status, delivery=order.delivery, delivery_fee=order.delivery_fee)
    return order_orm 

def create_orderline(order_id, item_id, quantity):
    orderline_orm = models_orm.OrderLine(order_id=order_id, item_id=item_id, quantity=quantity)    
    return orderline_orm

def create_payment(payment, user_id):
    if isinstance(payment, models.CreditPayment):
        payment_orm = models_orm.CreditPayment(
            person_id=user_id, amount=payment.amount, 
            date=payment.date, card_number=payment.card_number, 
            card_type=payment.card_type, expiry_date=payment.expiry_date)
    elif isinstance(payment, models.DebitPayment):
        payment_orm = models_orm.DebitPayment(
            person_id=user_id, amount=payment.amount, 
            date=payment.date, card_number=payment.card_number, 
            bank_name=payment.bank_name)
    else:
        payment_orm = models_orm.Payment(
            person_id=user_id, amount=payment.amount, 
            date=payment.date)
 
    return payment_orm

def map_item_orm_to_domain(item_orm):
    try:
        if item_orm.type == 'weighted_veggie':
            item_obj = models.WeightedVeggie(item_orm.name, item_orm.price, item_orm.url)
        elif item_orm.type == 'pack_veggie':
            item_obj = models.PackVeggie(item_orm.name, item_orm.price, item_orm.url)
        elif item_orm.type == 'unitprice_veggie':
            item_obj = models.UnitPriceVeggie(item_orm.name, item_orm.price, item_orm.url)
        else:
            item_obj = models.PremadeBox(item_orm.size)
    except ValueError as e:
        print(e)
    return item_obj

def map_customer_orm_to_domain(customer_orm):
    try:
        if customer_orm.type == 'customer':
            user_obj = models.Customer(
                customer_orm.first_name, customer_orm.last_name, customer_orm.username, customer_orm.password, customer_orm.address, customer_orm.balance)
        else:
            user_obj = models.CorporateCustomer(
                customer_orm.first_name, customer_orm.last_name, customer_orm.username, customer_orm.password, customer_orm.address, customer_orm.balance)         
        user_obj.available_credit = customer_orm.available_credit
        user_obj.owing = customer_orm.owing
    except ValueError as e:
        print(e)
    return user_obj

def summarise_cart(cart_details, user_orm):
    total_amount = 0
    total_quantity = 0
    cart_summary = {}

    for item in cart_details.values():
        total_amount += item['subtotal']
        total_quantity += item['quantity']
    if user_orm.type == 'customer':
        cart_summary = {
            'total': float(f'{total_amount:.2f}'),
            'quantity': total_quantity
        }
    else:
        cart_summary = {
            'discounted_amount': float(f"{total_amount * user_orm.discount:.2f}"),
            'total_before_discount': float(f'{total_amount:.2f}'),
            'total': float(f"{total_amount * (1 - user_orm.discount):.2f}"),
            'quantity': total_quantity
        }
    return cart_summary

def calculate_revenue_by_period(payment_list, time_period):
    revenue = 0
    for payment in payment_list:
        payment_date = utils.convert_str_to_date(payment.date)
        if time_period == 'week':
            if utils.is_within_week(payment_date):
                revenue += payment.amount
        elif time_period == 'month':
            if utils.is_within_month(payment_date):
                revenue += payment.amount
        elif time_period == 'quarter':
            if utils.is_within_quarter(payment_date):
                revenue += payment.amount
        elif time_period == 'year':
            if utils.is_within_year(payment_date):
                revenue += payment.amount
    return float(f'{revenue:.2f}')

def calculate_product_popularity(db_session):
    orderline_list = db_session.query(models_orm.OrderLine).all()
    product_popularity = {}
    for orderline in orderline_list:
        item = db_session.query(models_orm.Item).filter(models_orm.Item.id == orderline.item_id).first()
        item_name = item.name
        if item.type == "premade_box":
            item_name = f"{item.name} ({item.size})"
        if item_name not in product_popularity:
            product_popularity[item_name] = orderline.quantity
        else:
            product_popularity[item_name] += orderline.quantity
    product_popularity = sorted(product_popularity.items(), key=lambda x: x[1], reverse=True)
    product_popularity = list(product_popularity)

    return product_popularity

def initialise_db(db_session):
    initialise_people(db_session)
    initialise_products(db_session)
    initialise_orders(db_session)
    initialise_payments(db_session)

def create_people_obj_from_file():
    staff_list = []
    with open("static/db_files/staff.txt", "r") as file:
        for line in file:
            try:
                staff_info = [item.strip() for item in line.split(",")]
                fname, lname, username, password, dept = staff_info
                password = utils.generate_hashed_password(password)
                staff = models.Staff(fname, lname, username, password, dept)
                staff_list.append(staff)
            except Exception as e:
                print(f"An error of type {type(e).__name__} occurred: {e}")
    
    customer_list = []
    with open("static/db_files/customer.txt", "r") as file:
        for line in file:
            try:
                customer_info = [item.strip() for item in line.split(",")]
                fname, lname, username, password, address, balance = customer_info
                password = utils.generate_hashed_password(password)
                customer = models.Customer(fname, lname, username, password, address, float(balance))
                customer_list.append(customer)
            except Exception as e:
                print(f"An error of type {type(e).__name__} occurred: {e}")
    
    corporate_customer_list = []
    with open("static/db_files/corporate_cus.txt", "r") as file:
        for line in file:
            try:
                corporate_customer_info = [item.strip() for item in line.split(",")]
                fname, lname, username, password, address, balance, credit_limit = corporate_customer_info
                password = utils.generate_hashed_password(password)
                corporate_customer = models.CorporateCustomer(fname, lname, username, password, address, float(balance), float(credit_limit))
                corporate_customer_list.append(corporate_customer)
            except Exception as e:
                print(f"An error of type {type(e).__name__} occurred: {e}")

    return staff_list, customer_list, corporate_customer_list

def initialise_people(db_session):
    user_list = get_all_users(db_session)

    if not user_list: 
        staff_list, customer_list, corporate_customer_list = create_people_obj_from_file()
        for staff in staff_list:
            staff_orm = models_orm.Staff(first_name=staff.first_name, last_name=staff.last_name, username=staff.username, password=staff.password, department=staff.department, date_joined=staff.date_joined)
            db_session.add(staff_orm)
        
        for customer in customer_list:
            customer_orm = models_orm.Customer(first_name=customer.first_name, last_name=customer.last_name, username=customer.username, password=customer.password, address=customer.address, balance=customer.balance, owing=customer.owing, credit_limit=customer.credit_limit, available_credit=customer.available_credit)
            db_session.add(customer_orm)
        
        for corporate_customer in corporate_customer_list:
            corporate_customer_orm = models_orm.CorporateCustomer(first_name=corporate_customer.first_name, last_name=corporate_customer.last_name, username=corporate_customer.username, password=corporate_customer.password, address=corporate_customer.address, balance=corporate_customer.balance, credit_limit=corporate_customer.credit_limit, owing=corporate_customer.owing, discount=corporate_customer.discount, available_credit=corporate_customer.available_credit)
            db_session.add(corporate_customer_orm)
        
        db_session.commit()
    
def create_product_obj_from_file():
    pack_veggie_list = []
    with open("static/db_files/pack_veggie.txt", "r") as file:
        for line in file:
            try:
                veggie_info = [item.strip() for item in line.split(",")]
                name, price, url = veggie_info
                veggie = models.PackVeggie(name, float(price), url)
                pack_veggie_list.append(veggie)
            except Exception as e:
                print(f"An error of type {type(e).__name__} occurred: {e}")

    weighted_veggie_list = []
    with open("static/db_files/weighted_veggie.txt", "r") as file:
        for line in file:
            try:
                veggie_info = [item.strip() for item in line.split(",")]
                name, price, url = veggie_info
                veggie = models.WeightedVeggie(name, float(price), url)
                weighted_veggie_list.append(veggie)
            except Exception as e:
                print(f"An error of type {type(e).__name__} occurred: {e}")
    
    unit_veggie_list = []
    with open("static/db_files/unit_veggie.txt", "r") as file:
        for line in file:
            try:
                veggie_info = [item.strip() for item in line.split(",")]
                name, price, url = veggie_info
                veggie = models.UnitPriceVeggie(name, float(price), url)
                unit_veggie_list.append(veggie)
            except Exception as e:
                print(f"An error of type {type(e).__name__} occurred: {e}")
    
    premade_box_list = []
    size = ["small", "medium", "large"]
    for s in size:
        premade_box = models.PremadeBox(s)
        premade_box_list.append(premade_box)
    
    return pack_veggie_list, weighted_veggie_list, unit_veggie_list, premade_box_list

def initialise_products(db_session):
    veggies, premade_boxes = get_all_products(db_session)

    if not veggies and not premade_boxes:
        pack_veggie_list, weighted_veggie_list, unit_veggie_list, premade_box_list = create_product_obj_from_file()

        for veggie in pack_veggie_list:
            veggie_orm = models_orm.PackVeggie(name=veggie.name, price=veggie.price, url=veggie.url)
            db_session.add(veggie_orm)
        
        for veggie in weighted_veggie_list:
            veggie_orm = models_orm.WeightedVeggie(name=veggie.name, price=veggie.price, url=veggie.url)
            db_session.add(veggie_orm)
        
        for veggie in unit_veggie_list:
            veggie_orm = models_orm.UnitPriceVeggie(name=veggie.name, price=veggie.price, url=veggie.url)
            db_session.add(veggie_orm)
        
        for premade_box in premade_box_list:
            premade_box_orm = models_orm.PremadeBox(size=premade_box.size, price=premade_box.price)
            db_session.add(premade_box_orm)
        
        db_session.commit()

def initialise_orders(db_session):
    order_list = get_all_orders(db_session)
    if not order_list:
        user_list = get_all_users(db_session)
        veggie_list, premade_box_list = get_all_products(db_session)
        product_list = veggie_list + premade_box_list

        order_info_list = []
        with open("static/db_files/order.txt", "r") as file:
            for line in file:
                try:
                    order_info = [item.strip() for item in line.split(",")]
                    order_id, username, date, total, status = order_info
                    for user in user_list:
                        if user.username == username:
                            order_orm = models_orm.Order(
                                person_id=user.id, total=float(total), 
                                date=date, status=status)
                            db_session.add(order_orm)
                            db_session.flush()                          
                            # db_session.commit()
                            # db_session.refresh(order_orm)
                            order_info.append(order_orm.id)
                            order_info_list.append(order_info)
                except Exception as e:
                    print(f"An error of type {type(e).__name__} occurred: {e}")
            
        orderline_orms = []
        for order_info in order_info_list:
            order_info_id = order_info[0]
            order_orm_id = order_info[-1]
            with open("static/db_files/orderline.txt", "r") as file:
                for line in file:
                    try:
                        orderline_info = [item.strip() for item in line.split(",")]
                        order_id, product_name, quantity = orderline_info
                        if order_id == order_info_id:
                            for product in product_list:
                                if product.type == "premade_box":
                                    if product.size.lower() == product_name.lower():
                                        orderline_orm = models_orm.OrderLine(
                                            order_id=order_orm_id, item_id=product.id, quantity=float(quantity))
                                        orderline_orms.append(orderline_orm)
                                else:
                                    if product.name.lower() == product_name.lower():
                                        orderline_orm = models_orm.OrderLine(
                                            order_id=order_orm_id, item_id=product.id, quantity=float(quantity))
                                        orderline_orms.append(orderline_orm)
                    except Exception as e:
                        print(f"An error of type {type(e).__name__} occurred: {e}")
    
            
        for orderline in orderline_orms:
            db_session.add(orderline)
        
        db_session.commit()
           
def initialise_payments(db_session):
    payment_list = get_all_payments(db_session)
    if not payment_list:
        user_list = get_all_users(db_session)

        payment_orms = []
        with open("static/db_files/payment.txt", "r") as file:
            for line in file:
                try:
                    payment_info = [item.strip() for item in line.split(",")]
                    payment_id, username, date, amount = payment_info
                    for user in user_list:
                        if user.username == username:
                            payment_orm = models_orm.Payment(
                                person_id=user.id, amount=float(amount), 
                                date=date)
                            payment_orms.append(payment_orm)
                except Exception as e:
                    print(f"An error of type {type(e).__name__} occurred: {e}")
        
        for payment in payment_orms:
            db_session.add(payment)
        
        db_session.commit()