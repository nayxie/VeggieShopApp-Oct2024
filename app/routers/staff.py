from flask import Blueprint, flash, redirect, render_template, session
from app import db, helper


staff_page = Blueprint("staff", __name__, static_folder="static", template_folder="templates")


@staff_page.route("/dashboard/")
def dashboard():

    with db.get_db() as db_session:
        veggie_list, premade_box_list = helper.get_all_products(db_session)
        user = helper.get_one_user(db_session, session['username'], session['user_type'])
        
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

        user_profile = helper.format_user_profile(user)

        return render_template("staff/dashboard.html",
            veggie_list=veggies,
            premade_box_list=premade_boxes,
            user_profile=user_profile)

@staff_page.route("/view_customers/")
def view_customers():
    with db.get_db() as db_session:
        staff = helper.get_one_user(db_session, session['username'], session['user_type'])
        staff_profile = helper.format_user_profile(staff)

        customer_list = helper.get_all_customers(db_session)

        regular_customers = []
        corporate_customers = []
        for customer in customer_list:
            customer_dict = helper.format_user_profile(customer)
            if customer.type == 'corporate_customer':
                corporate_customers.append(customer_dict)
            else:
                regular_customers.append(customer_dict)

        
        return render_template("staff/view_customers.html",
            regular_customer_list=regular_customers,
            corporate_customer_list=corporate_customers,
            user_profile=staff_profile)

@staff_page.route("/view_orders/")
def view_orders():
    with db.get_db() as db_session:
        user = helper.get_one_user(db_session, session['username'], session['user_type'])
        user_profile = helper.format_user_profile(user)
        order_list = helper.get_all_orders_with_user_details(db_session)

        orders = []
        for order, user in order_list:
            order_dict = {
                'id': order.id,
                'date': order.date,
                'total': order.total,
                'status': order.status,
                'delivery': 'pick up' if order.delivery == 0 else 'delivery',
                'delivery_fee': order.delivery_fee,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
            orders.append(order_dict)

        return render_template("staff/view_orders.html", 
            user_profile=user_profile,
            order_list=orders)

@staff_page.route("/process_order/<int:order_id>/")
def process_order(order_id):
    with db.get_db() as db_session:
        order = helper.get_one_order(db_session, order_id)
        order.status = 'fulfilled'
        # db_session.commit()
        flash('Order processed successfully', 'success')
        return redirect('/staff/view_orders/')

@staff_page.route("/view_analytics/", methods=['GET'])
def view_analytics():
    with db.get_db() as db_session:
        payment_list = helper.get_all_payments(db_session)
        user = helper.get_one_user(db_session, session['username'], session['user_type'])
        user_profile = helper.format_user_profile(user)

        revenue_by_week = helper.calculate_revenue_by_period(payment_list, 'week')
        revenue_by_month = helper.calculate_revenue_by_period(payment_list, 'month')
        revenue_by_quarter = helper.calculate_revenue_by_period(payment_list, 'quarter')
        revenue_by_year = helper.calculate_revenue_by_period(payment_list, 'year')

        product_popularity = helper.calculate_product_popularity(db_session)

        return render_template("staff/view_analytics.html",
                            revenue_by_week=revenue_by_week,
                            revenue_by_month=revenue_by_month,
                            revenue_by_quarter=revenue_by_quarter,
                            revenue_by_year=revenue_by_year,
                            product_popularity=product_popularity,
                            user_profile=user_profile)