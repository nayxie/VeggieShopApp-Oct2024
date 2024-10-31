'''domain model classes for the application'''

from abc import ABC
import datetime
from typing import Union
from app import utils


class Person(ABC):
    def __init__(self, fname: str, lname: str, username: str, password: str) -> None:
        self.first_name = fname
        self.last_name = lname
        self.username = username
        self.password = password

    def __str__(self) -> str:
        return f"Name: {self.first_name} {self.last_name}, Username: {self.username}"
    
    @property
    def first_name(self) -> str:
        return self.__first_name
    
    @first_name.setter
    def first_name(self, fname: str) -> None:
        self.__first_name = fname.capitalize()

    @property
    def last_name(self)-> str:
        return self.__last_name
    
    @last_name.setter
    def last_name(self, lname: str) -> None:
        self.__last_name = lname.capitalize()

    @property
    def username(self) -> str:
        return self.__username
    
    @username.setter
    def username(self, username: str) -> None:
        self.__username = username.lower()

    @property
    def password(self) -> str:
        return self.__password
    
    @password.setter
    def password(self, password: str) -> None:
        self.__password = password

class Staff(Person): 
    def __init__(self, fname: str, lname: str, username: str, password: str, dept: str) -> None:
        super().__init__(fname, lname, username, password)
        self.department = dept
        self.date_joined = utils.get_current_date()

    def __str__(self) -> str:
        return f"{super().__str__()}, Dept: {self.department}, Date Joined: {self.date_joined}"

    @property
    def department(self)-> str:
        return self.__department
    
    @department.setter
    def department(self, dept: str) -> None:
        self.__department = dept.capitalize()

    @property
    def date_joined(self) -> str:
        return self.__date_joined
    
    @date_joined.setter
    def date_joined(self, date: Union[datetime.date, str]) -> None:
        if isinstance(date, datetime.date):
            self.__date_joined = date
        elif isinstance(date, str):
            try:
                utils.convert_str_to_date(date)
            except ValueError:
                raise ValueError(f"Invalid date string format: {date}. Expected 'DD-MM-YYYY'.")
            else:
                self.__date_joined = date
        else:
            raise TypeError(f"Expected a date or string, but got {type(date).__name__}.")

class Customer(Person):
    def __init__(self, fname: str, lname: str, username: str, password: str, address: str, balance: float) -> None:
        super().__init__(fname, lname, username, password)
        self.address = address
        self.balance = balance
        self.owing = 0.00
        self.credit_limit = 100
        self.available_credit = self.credit_limit - self.owing
        self.order_list = []
        self.payment_list = []

    def __str__(self) -> str:
        return f"{super().__str__()}, Address: {self.address}, Balance: {self.balance}, Owing: {self.owing}, Credit Limit: {self.credit_limit}"
    
    @property
    def address(self) -> str:
        return self.__address
    
    @address.setter
    def address(self, address: str) -> None:
        self.__address = address

    @property
    def balance(self) -> float:
        return self.__balance
    
    @balance.setter
    def balance(self, balance: float) -> None:
        if balance < 0:
            raise ValueError("Balance cannot be negative")
        self.__balance = balance

    @property
    def owing(self) -> float:
        return self.__owing
    
    @owing.setter
    def owing(self, owing: float) -> None:
        if owing < 0:
            raise ValueError("Owing cannot be negative")
        self.__owing = owing

    @property
    def credit_limit(self) -> float:
        return self.__credit_limit
    
    @credit_limit.setter
    def credit_limit(self, credit_limit: float) -> None:
        if credit_limit < 0:
            raise ValueError("Credit limit cannot be negative")
        self.__credit_limit = credit_limit

    @property
    def available_credit(self) -> float:
        return self.__available_credit
    
    @available_credit.setter
    def available_credit(self, available_credit: float) -> None:
        if available_credit < 0:
            raise ValueError("Available credit cannot be negative")
        self.__available_credit = available_credit
    
    def place_order(self, order: 'Order') -> None:
        self.order_list.append(order)
    
    def make_payment(self, payment: 'Payment') -> None:
        if payment.amount > self.balance + self.available_credit:
            raise InsuficientCreditError("Insufficient credit")
        elif payment.amount > self.balance:
            credit_payment = payment.amount - self.balance
            self.balance = 0   # use up balance first  
            self.owing += credit_payment  # credit decreases, owing increases
            self.available_credit -= credit_payment  # deduct credit second
        else:
            self.balance -= payment.amount
        self.payment_list.append(payment)

class CorporateCustomer(Customer):
    def __init__(self, fname: str, lname: str, username: str, password: str, address: str, balance: float, credit_limit: float = 200) -> None:
        super().__init__(fname, lname, username, password, address, balance)
        self.credit_limit = credit_limit   # override default credit limit (inherited from Customer)
        self.available_credit = self.credit_limit - self.owing   # update available credit
        self.discount = 0.1

    def __str__(self) -> str:
        return f"{super().__str__()}, Discount: {self.discount}" 
    
    @property
    def discount(self) -> float:
        return self.__discount
    
    @discount.setter
    def discount(self, discount: float) -> None:
        if discount < 0:
            raise ValueError("Discount cannot be negative")
        self.__discount = discount

class Payment:
    def __init__(self, amount: float, date: Union[datetime.date, str], customer: Customer) -> None:
        self.amount = amount
        self.date = date
        self.customer = customer
    
    def __str__(self) -> str:
        return f"Amount: {self.amount}, Date: {self.date}, Customer: {self.customer.first_name} {self.customer.last_name}"
    
    @property
    def amount(self) -> float:
        return self.__amount
    
    @amount.setter
    def amount(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self.__amount = amount

    @property
    def date(self) -> datetime.date:
        return self.__date
    
    @date.setter
    def date(self, date: Union[datetime.date, str]) -> None:
        if isinstance(date, datetime.date):
            self.__date = date
        elif isinstance(date, str):
            try:
                utils.convert_str_to_date(date)
            except ValueError:
                raise ValueError(f"Invalid date string format: {date}. Expected 'DD-MM-YYYY'.")
            else:
                self.__date = date
        else:
            raise TypeError(f"Expected a date or string, but got {type(date).__name__}.")

    @property
    def customer(self) -> Customer:
        return self.__customer
    
    @customer.setter
    def customer(self, customer: Customer) -> None:
        self.__customer = customer

class CreditPayment(Payment):
    def __init__(self, amount: float, date: Union[datetime.date, str], customer: Customer, card_number: str, card_type: str, expiry_date: Union[datetime.date, str]) -> None:
        super().__init__(amount, date, customer)
        self.card_number = card_number
        self.card_type = card_type
        self.expiry_date = expiry_date
    
    def __str__(self) -> str:
        return f"{super().__str__()}, Card Number: {self.card_number}, Card Type: {self.card_type}, Expiry Date: {self.expiry_date}"
    
    @property
    def card_number(self) -> str:
        return self.__card_number
    
    @card_number.setter
    def card_number(self, card_number: str) -> None:
        if not utils.validate_card_number(card_number):
            raise ValueError("Invalid card number")
        self.__card_number = card_number

    @property
    def card_type(self) -> str:
        return self.__card_type
    
    @card_type.setter
    def card_type(self, card_type: str) -> None:
        self.__card_type = card_type

    @property
    def expiry_date(self) -> datetime.date:
        return self.__expiry_date
    
    @expiry_date.setter
    def expiry_date(self, expiry_date: Union[datetime.time, str]) -> None:
        if isinstance(expiry_date, datetime.date):
            if expiry_date < datetime.date.today():
                raise ValueError("Expiry date cannot be in the past")
            self.__expiry_date = expiry_date
        elif isinstance(expiry_date, str):
            if not utils.validate_expiry_date(expiry_date):
                raise ValueError("Invalid expiry date")
            self.__expiry_date = expiry_date
        else:
            raise TypeError(f"Expected a date or string, but got {type(expiry_date).__name__}.")

class DebitPayment(Payment):
    def __init__(self, amount: float, date: Union[datetime.date, str], customer: Customer, card_number: str, bank_name: str) -> None:
        super().__init__(amount, date, customer)
        self.card_number = card_number
        self.bank_name = bank_name
    
    def __str__(self) -> str:
        return f"{super().__str__()}, Card Number: {self.card_number}, Bank Name: {self.bank_name}"
    
    @property
    def card_number(self) -> str:
        return self.__card_number
    
    @card_number.setter
    def card_number(self, card_number: str) -> None:
        if not utils.validate_card_number(card_number):
            raise ValueError("Invalid card number")
        self.__card_number = card_number

    @property
    def bank_name(self) -> str:
        return self.__bank_name
    
    @bank_name.setter
    def bank_name(self, bank_name: str) -> None:
        self.__bank_name = bank_name

class Order:
    def __init__(self, date: datetime.date, status: str, customer: Customer, delivery: bool = False, total: float = 0, distance_limit: int = 20) -> None:
        self.date = date
        self.total = total  # default total is 0
        self.status = status # processing, fulfilled, cancelled
        self.customer = customer
        self.delivery = delivery
        self.delivery_fee = 10.00
        self.distance_limit = distance_limit
        self.orderline_list = []
    
    def __str__(self) -> str:
        return f"Date: {self.date}, Total: {self.total}, Status: {self.status}, Customer: {self.customer.first_name} {self.customer.last_name}"
    
    @property
    def date(self) -> datetime.date:
        return self.__date
    
    @date.setter
    def date(self, date: Union[datetime.date, str]) -> None:
        if isinstance(date, datetime.date):
            self.__date = date
        elif isinstance(date, str):
            try:
                utils.convert_str_to_date(date)
            except ValueError:
                raise ValueError(f"Invalid date string format: {date}. Expected 'DD-MM-YYYY'.")
            else:
                self.__date = date
        else:
            raise TypeError(f"Expected a date or string, but got {type(date).__name__}.")

    @property
    def total(self) -> float:
        return self.__total
    
    @total.setter
    def total(self, total: float) -> None:
        if total < 0:
            raise ValueError("Total cannot be negative")
        self.__total = total

    @property
    def status(self) -> str:
        return self.__status
    
    @status.setter
    def status(self, status: str) -> None:
        if status not in ['processing', 'fulfilled', 'cancelled']:
            raise InvalidOrderStatusError("Invalid order status")
        self.__status = status

    @property
    def customer(self) -> Customer:
        return self.__customer
    
    @customer.setter
    def customer(self, customer: Customer) -> None:
        self.__customer = customer

    @property
    def delivery(self) -> bool:
        return self.__delivery
    
    @delivery.setter
    def delivery(self, delivery: bool) -> None:
        self.__delivery = delivery

    @property
    def delivery_fee(self) -> float:
        return self.__delivery_fee
    
    @delivery_fee.setter
    def delivery_fee(self, delivery_fee: float) -> None:
        if delivery_fee < 0:
            raise ValueError("Delivery fee cannot be negative")
        self.__delivery_fee = delivery_fee

    @property
    def distance_limit(self) -> int:
        return self.__distance_limit
    
    @distance_limit.setter
    def distance_limit(self, distance_limit: int) -> None:
        if distance_limit < 0:
            raise ValueError("Distance limit cannot be negative")
        if distance_limit > 20:
            raise DeliveryOutOfRangeError("Delivery out of current range of 20km")
    
    def add_orderline(self, orderline: 'OrderLine') -> None:
        self.orderline_list.append(orderline)
    
    def get_orderline_list(self) -> list['OrderLine']:
        return self.orderline_list
    
    def calculate_total(self) -> float:
        total = 0
        if self.orderline_list:
            for orderline in self.orderline_list:
                total += orderline.subtotal
            if isinstance(self.customer, CorporateCustomer):
                total -= total * self.customer.discount
            if self.delivery:
                total += self.delivery_fee
        self.total = total   # update total
        return total

    def check_credit(self) -> bool:
        if self.total > self.customer.balance + self.customer.available_credit:
            return False
        return True

class OrderLine:
    def __init__(self, item: 'Item', quantity: int) -> None:
        self.item = item
        self.quantity = quantity
        self.subtotal = item.price * quantity
    
    def __str__(self) -> str:
        return f"Item: {self.item}, Quantity: {self.quantity}, Subtotal: {self.subtotal}"
    
    @property
    def item(self) -> 'Item':
        return self.__item
    
    @item.setter
    def item(self, item: 'Item') -> None:
        self.__item = item

    @property
    def quantity(self) -> int:
        return self.__quantity
    
    @quantity.setter
    def quantity(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.__quantity = quantity

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    @subtotal.setter
    def subtotal(self, subtotal: float) -> None:
        if subtotal < 0:
            raise ValueError("Subtotal cannot be negative")
        self.__subtotal = subtotal

class Item(ABC):
    pass

class Veggie(Item):
    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url

    def __str__(self) -> str:
        return f"Item name: {self.name}"
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str) -> None:
        self.__name = name.capitalize()

    @property
    def url(self) -> str:
        return self.__url
    
    @url.setter
    def url(self, url: str) -> None:
        self.__url = url

class WeightedVeggie(Veggie):
    def __init__(self, name: str, price: float, url: str) -> None:
        super().__init__(name, url)
        self.price = price
    
    def __str__(self) -> str:
        return f"{self.name}, Price per kg: {self.price}"
    
    @property
    def price(self) -> float:
        return self.__price
    
    @price.setter
    def price(self, price: float) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.__price = price

class PackVeggie(Veggie):
    def __init__(self, name: str, price: float, url: str) -> None:
        super().__init__(name, url)
        self.price = price
    
    def __str__(self) -> str:
        return f"{self.name}, Price per pack: {self.price}"
    
    @property
    def price(self) -> float:
        return self.__price
    
    @price.setter
    def price(self, price: float) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.__price = price

class UnitPriceVeggie(Veggie):
    def __init__(self, name: str, price: float, url: str) -> None:
        super().__init__(name, url)
        self.price = price
    
    def __str__(self) -> str:
        return f"{self.name}, Price per unit: {self.price}"
    
    @property
    def price(self) -> float:
        return self.__price
    
    @price.setter
    def price(self, price: float) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.__price = price

class PremadeBox(Item):
    def __init__(self, size: str) -> None:
        self.name = 'Premade box'
        self.size = size
        self.price = self.calculate_price()
        self.content_list: list[Veggie] = []
    
    def __str__(self) -> str:
        if len(self.content_list) == 0:
            return f"Size: {self.size}, Price: {self.price}, Content: Pre-selected"
        return f"Size: {self.size}, Price: {self.price}, Content: {self.content_list}"
    
    @property
    def size(self) -> str:
        return self.__size
    
    @size.setter
    def size(self, size: str) -> None:
        if size not in ['small', 'medium', 'large']:
            raise PremadeboxSizeError("Invalid size")
        self.__size = size

    @property
    def price(self) -> float:
        return self.__price
    
    @price.setter
    def price(self, price: float) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.__price = price
    
    def calculate_price(self) -> float:
        if self.size == "small":
            self.price = 10.00
        elif self.size == "medium":
            self.price = 15.00
        elif self.size == "large":
            self.price = 20.00
        return self.price
    
    def add_veggie(self, veggie):
        self.content_list.append(veggie)
    
    def get_contents(self) -> list[Veggie]:
        return self.content_list
    


class InsuficientCreditError(Exception):
    pass

class InvalidOrderStatusError(Exception):
    pass

class DeliveryOutOfRangeError(Exception):
    pass

class PremadeboxSizeError(Exception):
    pass