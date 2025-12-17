from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
from sqlalchemy import ForeignKey
from datetime import date
from typing import List

class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)

ticket_mechanic =db.Table(
    'ticket_mechanic',
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True),
)

ticket_items = db.Table(
    'ticket_items',
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('inventory_id', db.Integer, db.ForeignKey('inventory.id'), primary_key=True),
)

class Customer(Base):
    __tablename__ = 'customers'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(db.String(255), nullable=False)
    email:Mapped[str] =mapped_column(db.String(255), nullable=False, unique=True)
    phone:Mapped[str] = mapped_column(db.String(10), nullable=True)
    password:Mapped[str] = mapped_column(db.String(255),nullable=False)

    service_tickets: Mapped[List["ServiceTickets"]] = db.relationship(
        "ServiceTickets", back_populates="customer", cascade="all, delete-orphan")

class Mechanic(Base):
    __tablename__ = 'mechanics'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    salary: Mapped[int] = mapped_column(db.Integer, nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    service_tickets: Mapped[List["ServiceTickets"]] = db.relationship(
        "ServiceTickets",
        secondary=ticket_mechanic,
        back_populates="mechanics",
    )

class ServiceTickets(Base):
    __tablename__ = "service_tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(db.Date,)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    service_descr: Mapped[str] = mapped_column(db.String(255), nullable=False)

    customer: Mapped["Customer"] = db.relationship(
        "Customer", back_populates="service_tickets"
    )
    
    mechanics: Mapped[List["Mechanic"]] = db.relationship(
        "Mechanic",
        secondary=ticket_mechanic,
        back_populates="service_tickets",
    )

    inventory: Mapped[List["Inventory"]] = db.relationship(
        "Inventory",
        secondary=ticket_items,
        back_populates="service_tickets",
    )



class Inventory(Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
 
    service_tickets: Mapped[List["ServiceTickets"]] = db.relationship(
        "ServiceTickets",
        secondary=ticket_items,
        back_populates="inventory",
    )

