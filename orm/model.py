from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Float, Numeric, Date, Time, Enum, ForeignKey


class Base(DeclarativeBase):
    pass


string_len = 64


class Coffee(Base):
    __tablename__ = "coffees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum("espresso", "espresso machiatto", "cappuccino", "espresso americano", "cappuccino latte", "nes", "frappe"), nullable=False)
    size = Column(Enum("single", "double", "quadruple"), nullable=False)
    variety = Column(Enum("80% arabica + 20% robusta", "100% arabica", "decaffeine"), nullable=False)
    sugar = Column(Enum("little", "medium", "medium-to-sweet", "sweet", "very sweet"))
    sugar_type = Column(Enum("white", "brown", "saccharin", "stevia", "honey"))
    milk = Column(Enum("fresh", "evapore", "almond", "coconut", "oat"))
    extra = Column(Enum("chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup", "vanilla syrup", "cinnamon powder", "chocolate powder"))
    cost = Column(Numeric(precision=4, scale=2), nullable=False)


class FreddoFlat(Base):
    __tablename__ = "freddos_flats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum("freddo espresso", "espresso cappuccino", "espresso cappuccino latte", "flat white cold", "flat white hot"), nullable=False)
    size = Column(Enum("regular", "XL"), nullable=False)
    variety = Column(Enum("80% arabica + 20% robusta", "100% arabica", "decaffeine"), nullable=False)
    sugar = Column(Enum("little", "medium", "medium-to-sweet", "sweet", "very sweet"))
    sugar_type = Column(Enum("white", "brown", "saccharin", "stevia", "honey"))
    milk = Column(Enum("fresh", "evapore", "almond", "coconut", "oat"))
    extra = Column(Enum("chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup", "vanilla syrup", "cinnamon powder", "chocolate powder"))
    cost = Column(Numeric(precision=4, scale=2), nullable=False)


class Filter(Base):
    __tablename__ = "filters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum("filter", "irish coffee", "ellinikos"), nullable=False)
    size = Column(Enum("single", "double"), nullable=False)
    sugar = Column(Enum("little", "medium", "medium-to-sweet", "sweet", "very sweet"))
    sugar_type = Column(Enum("white", "brown", "saccharin", "stevia", "honey"))
    milk = Column(Enum("fresh", "evapore", "almond", "coconut", "oat"))
    extra = Column(Enum("chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup", "vanilla syrup", "cinnamon powder", "chocolate powder"))
    cost = Column(Numeric(precision=4, scale=2), nullable=False)


class Chocolate(Base):
    __tablename__ = "chocolates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum("chocolate", "chocolate viennois", "chocolate white", "chocolate bitter", "chocolate orange", "chocolate hazelnut", "chocolate ruby", "chocolate salty caramel"), nullable=False)
    temperature = Column(Enum("hot", "cold"), nullable=False)
    extra = Column(Enum("chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup", "vanilla syrup"))
    cost = Column(Numeric(precision=4, scale=2), nullable=False)


class WeirdChocolate(Base):
    __tablename__ = "weird_chocolates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum("freddoccino", "mochaccino"), nullable=False)
    extra = Column(Enum("chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup", "vanilla syrup"))
    cost = Column(Numeric(precision=4, scale=2), nullable=False)


class Beverage(Base):
    __tablename__ = "beverages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(string_len), nullable=False)
    cost = Column(Numeric(precision=4, scale=2), nullable=False)


class Tee(Base):
    __tablename__ = "tees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum("tee"), nullable=False)
    variety = Column(Enum("green", "green with pergamot", "rooibos", "moroccan mint", "black with forest fruits", "english breakfast", "apple"))
    sugar = Column(Enum("little", "medium", "medium-to-sweet", "sweet", "very sweet"))
    sugar_type = Column(Enum("white", "brown", "saccharin", "stevia", "honey"))
    milk = Column(Enum("fresh", "evapore", "almond", "coconut", "oat"))
    extra = Column(Enum("chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup", "vanilla syrup", "cinnamon powder", "chocolate powder"))
    cost = Column(Numeric(precision=4, scale=2), nullable=False)


class Chamomile(Base):
    __tablename__ = "chamomiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum("chamomile"), nullable=False)
    sugar = Column(Enum("little", "medium", "medium-to-sweet", "sweet", "very sweet"))
    sugar_type = Column(Enum("white", "brown", "saccharin", "stevia", "honey"))
    milk = Column(Enum("fresh", "evapore", "almond", "coconut", "oat"))
    extra = Column(Enum("chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup", "vanilla syrup", "cinnamon powder", "chocolate powder"))
    cost = Column(Numeric(precision=4, scale=2), nullable=False)


class Smoothie(Base):
    __tablename__ = "smoothies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum("smoothie: ergati", "smoothie: kiklothimikou", "smoothie: popai", "smoothie: athliti", "smoothie: mogli", "smoothie: irakli"), nullable=False)
    milk = Column(Enum("light", "fat", "almond", "coconut"))
    cost = Column(Numeric(precision=4, scale=2), nullable=False)


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(string_len))
    cost = Column(Numeric(precision=4, scale=2), nullable=False)


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(string_len), nullable=False)
    cost = Column(Numeric(precision=4, scale=2), nullable=False)


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(string_len), nullable=False)
    latitude = Column(Float(precision=53))
    longitude = Column(Float(precision=53))


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(string_len), nullable=False)
    floor = Column(Integer, nullable=False)

    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)


class Workday(Base):
    __tablename__ = "workdays"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, unique=True, nullable=False)
    hours = Column(Numeric(precision=4, scale=2), nullable=False)
    payment = Column(Numeric(precision=4, scale=2), nullable=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_time = Column(Time, nullable=False)
    delivery_time = Column(Time)
    tips = Column(Numeric(precision=4, scale=2), nullable=False)
    tips_method = Column(Enum("Cash", "Card"))
    source = Column(Enum("Efood", "Wolt", "Box", "Phone"), nullable=True)
    payment_method = Column(Enum("Cash", "Card"), nullable=True)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    workday_id = Column(Integer, ForeignKey("workdays.id"), nullable=False)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, nullable=False)
    product_type = Column(Enum("coffee", "freddo or flat", "filter", "chocolate", "weird chocolate", "beverage", "tee", "chamomile", "smoothie", "food"), nullable=False)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    offer_id = Column(Integer, ForeignKey("offers.id"), nullable=False)


# Read view
class VOrdersSummary(Base):
    __tablename__ = "v_orders_summary"

    order_id = Column(Integer, primary_key=True)
    order_time = Column(Date)
    tips = Column(Numeric(precision=4, scale=2))
    tips_method = Column(String(string_len))
    source = Column(String(string_len))
    payment_method = Column(String(string_len))
    name = Column(String(string_len))
    latitude = Column(Float(precision=53))
    longitude = Column(Float(precision=53))







