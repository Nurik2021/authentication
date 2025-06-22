from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from fastapp.app.core.database import Base


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    aircraft = Column(String)
    departure_city = Column(String)
    departure_date = Column(Date)
    departure_time = Column(DateTime)
    arrival_city = Column(String)
    arrival_date = Column(Date)
    arrival_time = Column(DateTime)
    price = Column(Integer)
    baggage = Column(String)
    duration = Column(Integer)

    # Исправляем back_populates
    orders = relationship("Order", back_populates="flight")


class OrderPassenger(Base):
    __tablename__ = "order_passengers"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))

    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(String)
    gender = Column(String)
    validity_period = Column(String)
    passport = Column(String)
    phone = Column(String)
    email = Column(String)

    order = relationship("Order", back_populates="passengers")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    # Исправляем ForeignKey - было "flight.id", стало "flights.id"
    flight_id = Column(Integer, ForeignKey("flights.id"))
    consultant_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="В ожидании")
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    consultant = relationship("User")
    # Исправляем back_populates - было "order", стало "orders"
    flight = relationship("Flight", back_populates="orders")
    passengers = relationship("OrderPassenger", back_populates="order")