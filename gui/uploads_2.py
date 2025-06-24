from datetime import datetime

from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session
from colorama import Fore

from orm.model import Workday, Address, Customer, Order, Coffee, FreddoFlat, Filter, Chocolate, WeirdChocolate, Beverage, Tee, Chamomile, Smoothie, Food, Offer
from func import check_none_type

# Create a connection
engine = create_engine(
    "mysql+pymysql://root:Roussanto171!@localhost:3306/income_dummy",
    pool_pre_ping=True
)


def upload_workday(dict_var):
    # Export the variables' input
    date = datetime.strptime(dict_var["date"].get(), "%Y-%m-%d").date()
    hours = dict_var["hours"].get()
    payment = dict_var["payment"].get()

    with Session(engine) as session:
        # Dates in the database
        query = select(Workday.date)
        db_dates = session.execute(query).scalars().all()

        if date in db_dates:
            print(Fore.BLUE + "Workday already exists!")
        else:
            with session.begin():
                session.add(Workday(date=date, hours=hours, payment=payment))
            print(Fore.GREEN + "Workday upload successful!")


def upload_address(dict_var):
    # Export the variables' input
    address = dict_var["address"].get()
    latitude = dict_var["latitude"].get()
    longitude = dict_var["longitude"].get()

    # check_none_type returns (val,) because it's only one value in tuple.
    # To extract the val itself we use val[0]
    address = check_none_type(address)[0]

    with Session(engine) as session:
        query = select(Address.name)
        db_addresses = session.execute(query).scalars().all()

        if address in db_addresses:
            print(Fore.BLUE + "Address already exists!")
        else:
            with session.begin():
                session.add(Address(name=address, latitude=latitude, longitude=longitude))
            print(Fore.GREEN + "Address upload successful!")


def upload_customer(dict_var, address_name):
    # Export the variables' input
    customer_name = dict_var["customer name"].get()
    floor = dict_var["floor"].get()

    # Empty customer, floor entries means that the input is a string of length 0.
    # We need to make it NoneType, so the db can decline the input of an empty input.
    customer_name, floor = check_none_type(customer_name, floor)

    # If the customer name already exists and is already associated with the inputted address,
    # then the customer already exists in the database
    # Else,they have to be inserted into the database.
    with Session(engine) as session:
        subquery = select(Address.id).where(Address.name == address_name)
        query = select(Customer.name).where(Customer.address_id.in_(subquery))
        db_customers = session.execute(query).scalars().all()

        if customer_name in db_customers:
            print(Fore.BLUE + "Customer already exists!")
        else:
            with session.begin():
                session.add(Customer(name=customer_name, floor=floor))
            print(Fore.GREEN + "Customer upload successful!")


def upload_order(dict_var, workday_date, customer_name, address_name):
    # Export the variables' input
    order_time = datetime.strptime(dict_var["order time"].get(), "%H:%M:%S").time()
    delivery_time = datetime.strptime(dict_var["delivery time"].get(), "%H:%M:%S").time()
    tips = dict_var["tips"].get()
    tips_method = dict_var["tips method"].get()
    source = dict_var["source"].get()
    payment_method = dict_var["payment method"].get()

    # Empty entries means that the input is a string of length 0.
    # We need to make it NoneType, so the db can decline the input of an empty input.
    order_time, delivery_time, tips, tips_method, source, payment_method = check_none_type(order_time,
                                                                                           delivery_time,
                                                                                           tips,
                                                                                           tips_method,
                                                                                           source,
                                                                                           payment_method)

    # If no tips have been added, make them 0
    if tips == "":
        tips = 0.0

    # Add an order for given workday, customer name and address
    with Session(engine) as session:
        # Workday id
        subquery_1 = select(Workday.id).where(Workday.date == workday_date)
        workday_id = session.execute(subquery_1).scalars()

        # Address id
        subquery_2 = select(Address.id).where(Address.name == address_name)
        address_id = session.execute(subquery_2).scalars()

        # Customer id
        subquery_3 = select(Customer.id).where(and_(
                                                    Customer.address_id == address_id,
                                                    Customer.name == customer_name
                                                   )
                                               )
        customer_id = session.execute(subquery_3).scalars()

        # Add order
        session.add(Order(workday_id=workday_id,
                          customer_id=customer_id,
                          order_time=order_time,
                          delivery_time=delivery_time,
                          tips=tips,
                          tips_method=tips_method,
                          source=source,
                          payment_method=payment_method)
                    )
        print(Fore.GREEN + "Order upload successful!")


def upload_items(basket):
    # Export the variables' input
    for item in basket:
        # Make empty StringVars to None
        for key in list(item.keys()):
            item[key] = check_none_type(item[key])[0]

        with Session(engine) as session:
            if item["category"] == "Coffee":
                new_item = Coffee(**item)
            elif item["category"] == "Freddo or Flat":
                new_item = FreddoFlat(**item)
            elif item["category"] == "Filter":
                new_item = Filter(**item)
            elif item["category"] == "Chocolate":
                new_item = Chocolate(**item)
            elif item["category"] == "Food":
                new_item = Food(**item)
            elif item["category"] == "Beverage":
                new_item = Beverage(**item)
            elif item["category"] == "Chamomile":
                new_item = Chamomile(**item)
            elif item["category"] == "Weird Chocolate":
                new_item = WeirdChocolate(**item)
            elif item["category"] == "Tee":
                new_item = Tee(**item)
            elif item["category"] == "Smoothie":
                new_item = Smoothie(**item)
            session.add(new_item)


def upload_items_polymorphic(basket, customer_dict, address_dict, workday_dict, order_dict):
    for item in basket:
        # Parse data
        workday_date = datetime.strptime(workday_dict["date"].get(), "%Y-%m-%d").date()
        order_time = datetime.strptime(order_dict["order time"].get(), "%H:%M:%S").time()
        customer_name = customer_dict["customer name"].get()
        address = address_dict["address"].get()

        # Select the order that was just inserted
        # add query with limit 1

