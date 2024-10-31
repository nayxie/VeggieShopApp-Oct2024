'''orm model classes for the application'''

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db import Base


class Person(Base):
    __tablename__ = 'person'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(60))
    type: Mapped[str] = mapped_column(String(50))  # Discriminator column

    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': type
    }

class Staff(Person):
    __tablename__ = 'staff'
    
    id: Mapped[int] = mapped_column(Integer, ForeignKey('person.id'), primary_key=True)
    department: Mapped[str] = mapped_column(String(50))
    date_joined: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }

class Customer(Person):
    __tablename__ = 'customer'
    
    id: Mapped[int] = mapped_column(Integer, ForeignKey('person.id'), primary_key=True)
    address: Mapped[str] = mapped_column(String(150))
    balance: Mapped[float] = mapped_column(Float)
    owing: Mapped[float] = mapped_column(Float, default=0)
    credit_limit: Mapped[float] = mapped_column(Float, default=100)
    available_credit: Mapped[float] = mapped_column(Float)

    payments: Mapped[list['Payment']] = relationship(back_populates='customer')
    orders: Mapped[list['Order']] = relationship(back_populates='customer')

    __mapper_args__ = {
        'polymorphic_identity': 'customer'
    }

class CorporateCustomer(Customer):
    __tablename__ = 'corporate_customer'
    
    id: Mapped[int] = mapped_column(Integer, ForeignKey('customer.id'), primary_key=True)
    discount: Mapped[float] = mapped_column(Float, default=0.1)

    __mapper_args__ = {
        'polymorphic_identity': 'corporate_customer'
    }

class Payment(Base):
    __tablename__ = 'payment'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    amount: Mapped[float] = mapped_column(Float)
    date: Mapped[str] = mapped_column(String(50))
    person_id: Mapped[int] = mapped_column(Integer, ForeignKey('person.id'))
    type: Mapped[str] = mapped_column(String(50))

    customer: Mapped['Customer'] = relationship(back_populates='payments')

    __mapper_args__ = {
        'polymorphic_identity': 'payment',
        'polymorphic_on': type
    }

class CreditPayment(Payment):
    __tablename__ = 'credit_payment'
    
    id: Mapped[int] = mapped_column(Integer, ForeignKey('payment.id'), primary_key=True)
    card_number: Mapped[str] = mapped_column(String(50))
    card_type: Mapped[str] = mapped_column(String(50))
    expiry_date: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'credit_payment'
    }

class DebitPayment(Payment):
    __tablename__ = 'debit_payment'
    
    id: Mapped[int] = mapped_column(Integer, ForeignKey('payment.id'), primary_key=True)
    card_number: Mapped[str] = mapped_column(String(50))
    bank_name: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'debit_payment'
    }

class Order(Base):
    __tablename__ = 'order'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[str] = mapped_column(String(50))
    person_id: Mapped[int] = mapped_column(Integer, ForeignKey('person.id'))
    total: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(50))  # processing, fulfilled, cancelled
    delivery: Mapped[bool] = mapped_column(Boolean, default=False)
    delivery_fee: Mapped[float] = mapped_column(Float, default=10.00)
    distance_limit: Mapped[float] = mapped_column(Integer, default=20)

    customer: Mapped['Customer'] = relationship(back_populates='orders')
    orderlines: Mapped[list['OrderLine']] = relationship(back_populates='order', cascade='all, delete-orphan')

class OrderLine(Base):
    __tablename__ = 'orderline'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('order.id'))
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey('item.id'))
    quantity: Mapped[float] = mapped_column(Integer)

    order: Mapped['Order'] = relationship(back_populates='orderlines')

class Item(Base):
    __tablename__ = 'item'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': type
    }

class Veggie(Item):
    __tablename__ = 'veggie'
    
    id: Mapped[int] = mapped_column(Integer, ForeignKey('item.id'), primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    url: Mapped[str] = mapped_column(String(150))

    __mapper_args__ = {
        'polymorphic_identity': 'veggie'
    }

class WeightedVeggie(Veggie):
    __tablename__ = 'weightedveggie'
    
    id: Mapped[int] = mapped_column(Integer, ForeignKey('veggie.id'), primary_key=True)
    price: Mapped[float] = mapped_column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'weighted_veggie'
    }

class PackVeggie(Veggie):
    __tablename__ = 'packveggie'
    
    id: Mapped[int] = mapped_column(Integer, ForeignKey('veggie.id'), primary_key=True)
    price: Mapped[float] = mapped_column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'pack_veggie'
    }

class UnitPriceVeggie(Veggie):
    __tablename__ = 'unitpriceveggie'
    
    id: Mapped[int] = mapped_column(Integer, ForeignKey('veggie.id'), primary_key=True)
    price: Mapped[float] = mapped_column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'unitprice_veggie'
    }

class PremadeBox(Item):
    __tablename__ = 'premadebox'
    
    id: Mapped[int] = mapped_column(Integer, ForeignKey('item.id'), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), default='Premade box')
    size: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(Float)
    content_list: Mapped[list['Veggie']] = relationship()

    __mapper_args__ = {
        'polymorphic_identity': 'premade_box'
    }