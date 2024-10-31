from flask import Blueprint, flash, jsonify, redirect, render_template, request, session
from app import db, models, helper, utils

customer_page = Blueprint("customer", __name__, static_folder="static", template_folder="templates")


@customer_page.route("/dashboard/")
def dashboard():
    with db.get_db() as db_session:
        veggie_list, premade_box_list = helper.get_all_products(db_session)
        
        user = helper.get_one_user(db_session, session['username'], session['user_type'])
        user_profile = helper.format_user_profile(user)
        cart_details = session.get('cart', {})
        cart_summary = helper.summarise_cart(cart_details, user)
        
        veggies = []
        for veggie in veggie_list:
            veggie_dict = {
                'id': veggie.id,
                'name': veggie.name,
                'price': veggie.price,
                'url': veggie.url         
            }
            if veggie.type == 'weighted_veggie':
                veggie_dict['unit_type'] = 'kg'
            elif veggie.type == 'pack_veggie':
                veggie_dict['unit_type'] = 'pack'
            elif veggie.type == 'unitprice_veggie':
                veggie_dict['unit_type'] = 'unit'
            veggies.append(veggie_dict)

        premade_boxes = []
        for premade_box in premade_box_list:
            premade_box_dict = {
                'id': premade_box.id,
                'size': premade_box.size,
                'price': premade_box.price
            }
            premade_boxes.append(premade_box_dict)

        return render_template("customer/dashboard.html",
            veggie_list=veggies,
            premade_box_list=premade_boxes,
            user_profile=user_profile,
            cart_details=cart_details,
            cart_summary=cart_summary)

@customer_page.route('/add_to_cart/', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('productId')
    quantity = data.get('quantity')
    name = data.get('name')
    price = data.get('price')
    unit = data.get('unit')

    cart = session.get('cart', {})
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
        cart[product_id]['subtotal'] = float(f"{cart[product_id]['quantity'] * price:.2f}")
    else:
        cart[product_id] = {
            'name': name.capitalize(),
            'price': price,
            'quantity': quantity,
            'unit': unit,
            'subtotal': float(f'{quantity * price:.2f}')
        }

    print(f'Added item: \n{product_id}: {cart[product_id]}')
    print(f'Full cart: \n{cart}\n')
    session['cart'] = cart  # update session with new cart

    return jsonify({'status': 'success', 'cart': cart})

@customer_page.route('/place_order/', methods=['GET','POST'])
def place_order():
    with db.get_db() as db_session:
        user_orm = helper.get_one_user(db_session, session['username'], session['user_type'])
        user_obj = helper.map_customer_orm_to_domain(user_orm)
        user_profile = helper.format_user_profile(user_orm)
        cart_details = session.get('cart', {})
        if not cart_details:
            flash('Please add items to cart', 'warning')
            return redirect(request.referrer)

        cart_summary = helper.summarise_cart(cart_details, user_orm)
        
        if request.method == 'GET':
            return render_template("customer/place_order.html", 
                user_profile=user_profile,
                cart_details=cart_details,
                cart_summary=cart_summary)
        
        if request.method == 'POST':
            delivery_option = request.form.get('deliveryOption')
            payment_method = request.form.get('paymentMethod')
            if delivery_option == 'delivery':
                delivery = True
            elif delivery_option == 'pickup':
                delivery = False
            
            try:
                order = models.Order(
                    date=utils.get_current_date(), status='processing', 
                    customer=user_obj, delivery=delivery)
            except Exception as e:
                print(f"An error of type {type(e).__name__} occurred: {e}")
                flash('Order creation failed', 'danger')
                return redirect(request.url)

            for id, item in cart_details.items():
                # print(f'{id}: {item}')
                item_orm = helper.get_one_product(db_session, id)
                try:
                    item_obj = helper.map_item_orm_to_domain(item_orm)
                    orderline = models.OrderLine(item_obj, item['quantity'])
                    order.add_orderline(orderline)
                except Exception as e:
                    print(f"An error of type {type(e).__name__} occurred: {e}")
                    flash('Order creation failed', 'danger')
                    return redirect(request.url)

            order.calculate_total()  # update order total
            order_orm = helper.create_order(order, user_orm.id)

            db_session.add(order_orm)
            # db flush rather than commit to get order id
            db_session.flush()     
            order_id = order_orm.id

            for orderline in order.orderline_list:
                for id, item in cart_details.items():
                    if orderline.item.name.lower() == item['name'].lower(): 
                        orderline_orm = helper.create_orderline(order_id, id, item['quantity'])
                        db_session.add(orderline_orm)

            if payment_method == 'credit':
                cc_number = request.form.get('cc-number')
                cc_type = request.form.get('cc-type')
                cc_expiration = request.form.get('cc-expiration')

                if not utils.validate_card_number(cc_number):
                    db_session.rollback()
                    flash('Invalid credit card number', 'danger')
                    return redirect(request.url)
                if not utils.validate_expiry_date(cc_expiration):
                    db_session.rollback()
                    flash("Invalid credit card expiry date. Expected a future date: 'DD-MM-YYYY'", 'danger')
                    return redirect(request.url)
                try:
                    payment = models.CreditPayment(
                        amount=order.total, date=order.date, 
                        customer=user_orm, card_number=cc_number, 
                        card_type=cc_type, expiry_date=cc_expiration) 
                except Exception as e:
                    print(f"An error of type {type(e).__name__} occurred: {e}")
                    flash('Payment creation failed', 'danger')
                    return redirect(request.url)

            elif payment_method == 'debit':
                debit_card_number = request.form.get('debit-card-number')
                bank_option = request.form.get('bank-option')
                other_bank_name = request.form.get('other-bank-name')
                
                if other_bank_name:
                    bank_option = other_bank_name
                
                if not utils.validate_card_number(debit_card_number):
                    db_session.rollback()
                    flash('Invalid debit card number', 'danger')
                    return redirect(request.url)
                try:
                    payment = models.DebitPayment(
                        amount=order.total, date=order.date, 
                        customer=user_orm, card_number=debit_card_number, 
                        bank_name=bank_option) 
                except Exception as e:
                    print(f"An error of type {type(e).__name__} occurred: {e}")
                    flash('Payment creation failed', 'danger')
                    return redirect(request.url)
                
            elif payment_method == 'account':

                if not order.check_credit():
                    db_session.rollback()
                    flash('Insufficient funds', 'danger')
                    return redirect(request.url)
                try:
                    payment = models.Payment(amount=order.total, date=order.date, customer=user_orm) 
                except Exception as e:
                    print(f"An error of type {type(e).__name__} occurred: {e}")
                    flash('Payment creation failed', 'danger')
                    return redirect(request.url)
                
                user_obj.make_payment(payment)
                user_orm.balance = user_obj.balance
                user_orm.owing = user_obj.owing
                user_orm.available_credit = user_obj.available_credit

            payment_orm = helper.create_payment(payment, user_orm.id)  
            db_session.add(payment_orm)
            # db_session.commit() # handled by context manager
            session.pop('cart', None)
            flash('Order placed successfully', 'success')
            return redirect('/customer/dashboard/')

@customer_page.route('/start_new_order/')
def start_new_order():
    session.pop('cart', None)
    flash('Your cart is cleared', 'success')
    return redirect('/customer/dashboard/')

@customer_page.route('/view_orders/')
def view_orders():
    with db.get_db() as db_session:
        user = helper.get_one_user(db_session, session['username'], session['user_type'])
        user_profile = helper.format_user_profile(user)
        cart_details = session.get('cart', {})
        cart_summary = helper.summarise_cart(cart_details, user)
        order_list = helper.get_user_orders(db_session, user.id)

        orders = []
        for order in order_list:
            order_dict = {
                'id': order.id,
                'date': order.date,
                'total': order.total,
                'status': order.status,
                'delivery': 'pick up' if order.delivery==0 else 'delivery',
                'delivery_fee': order.delivery_fee
            }
            orders.append(order_dict)

        return render_template("customer/view_orders.html", 
            user_profile=user_profile,
            order_list=orders,
            cart_details=cart_details,
            cart_summary=cart_summary)

@customer_page.route('/cancel_order/<int:order_id>/')
def cancel_order(order_id):
    with db.get_db() as db_session:
        order = helper.get_one_order(db_session, order_id)
        order.status = 'cancelled'
        # db_session.commit()
        flash('Order cancelled successfully', 'success')
        return redirect('/customer/view_orders/')