from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, Numeric, Enum

Base = declarative_base()


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40))
    latitude = Column(Float(precision=53))
    longitude = Column(Float(precision=53))


class Beverage(Base):
    __tablename__ = "beverages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(40))
    cost = Column(Numeric(precision=4, scale=2))

class Chamomile(Base):
    __tablename__ = "chamomiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(40))
    cost = Column(Numeric(precision=4, scale=2))
