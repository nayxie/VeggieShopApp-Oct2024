from flask import Blueprint, flash, redirect, render_template, request, session
from app import models, models_orm, db, helper, utils

public_page = Blueprint("public", __name__, static_folder="static", template_folder="templates")



@public_page.route("/")
def home():
    return render_template("/public/home.html")

@public_page.route("/login/", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with db.get_db() as db_session:
            person = helper.get_one_user(db_session, username, 'any')
            if person is None:
                flash("User not found", 'warning')
                return redirect(request.url)
            if person is not None and not utils.verify_password(password, person.password):
                flash("Password not correct", 'warning')
                return redirect(request.url)
            
            session.clear()  # Clear any existing session data
            session['id'] = person.id
            session['username'] = person.username
            session['user_type'] = person.type
            session['loggedin'] = True
            if person.type == 'customer' or person.type == 'corporate_customer':
                return redirect('/customer/dashboard/')
            else:
                return redirect('/staff/dashboard/')
    return render_template("/public/login.html")

@public_page.route("/logout/")
def logout():
    session.clear()
    return redirect('/')

@public_page.route("/register/", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        password = utils.generate_hashed_password(password)
        address = request.form['address']
        type = request.form['customer_type']

        with db.get_db() as db_session:
            person = helper.get_one_user(db_session, username, 'any')
            if person is not None:
                flash("Username already exists", 'danger')
                return redirect(request.url)
            if not utils.validate_name(first_name):
                flash("First name is invalid", 'danger')
                return redirect(request.url)
            if not utils.validate_name(last_name):
                flash("Last name is invalid", 'danger')
                return redirect(request.url)
            if not utils.validate_address(address):
                flash("Address is invalid", 'danger')
                return redirect(request.url)
            try:
                if type == 'corporate_customer':
                    customer = models.CorporateCustomer(fname=first_name, lname=last_name, username=username, password=password, address=address, balance=0)
                    customer_orm = models_orm.CorporateCustomer(
                        first_name=customer.first_name, last_name=customer.last_name, 
                        username=customer.username, password=customer.password, 
                        address=customer.address, balance=customer.balance, 
                        credit_limit=customer.credit_limit, available_credit=customer.credit_limit, 
                        discount=customer.discount)
                else:
                    customer = models.Customer(fname=first_name, lname=last_name, username=username, password=password, address=address, balance=0)
                    customer_orm = models_orm.Customer(
                        first_name=customer.first_name, last_name=customer.last_name, 
                        username=customer.username, password=customer.password, 
                        address=customer.address, balance=customer.balance, 
                        credit_limit=customer.credit_limit, 
                        available_credit=customer.credit_limit)
                db_session.add(customer_orm)
                # db_session.commit()
                flash("Registration successful", 'success')
                return redirect('/login/')
            except Exception as e:
                print(f"An error of type {type(e).__name__} occurred: {e}")
                # db_session.rollback()
                flash("Registration failed. Please try again.", 'danger')
                return redirect(request.url)
        
    return render_template("/public/register.html")