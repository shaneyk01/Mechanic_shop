from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
from datetime import date
from typing import List

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Association table for many-to-many ServiceTickets <-> Mechanic
ticket_mechanic = db.Table(
    "ticket_mechanic",
    Base.metadata,
    db.Column("ticket_id", ForeignKey("service_tickets.id"), primary_key=True),
    db.Column("mechanic_id", ForeignKey("mechanics.id"), primary_key=True),
)

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(255), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    # one-to-many: Customer -> ServiceTickets
    service_tickets: Mapped[List["ServiceTickets"]] = db.relationship(
        "ServiceTickets", back_populates="customer", cascade="all, delete-orphan"
    )

class Mechanic(Base):
    __tablename__ = "mechanics"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    salary: Mapped[int] = mapped_column(db.Integer, nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    # many-to-many with ServiceTickets
    service_tickets: Mapped[List["ServiceTickets"]] = db.relationship(
        "ServiceTickets",
        secondary=ticket_mechanic,
        back_populates="mechanics",
    )

class ServiceTickets(Base):
    __tablename__ = "service_tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(db.Date, nullable=False)
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