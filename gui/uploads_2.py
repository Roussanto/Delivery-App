import tkinter
from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from colorama import Fore

from orm.model import Workday, Address, Customer, Order, Coffee, FreddoFlat, Filter, Chocolate, WeirdChocolate, Beverage, Tee, Chamomile, Smoothie, Food, Offer, Item
from orm.engine import engine
from func import check_none_type, data_valid


def upload_workday(info: dict[str, tkinter.Variable]):
    # Export the variables' input
    date = datetime.strptime(info["date"].get(), "%Y-%m-%d").date()
    hours = info["hours"].get()
    payment = info["payment"].get()

    with Session(engine) as session:
        # Dates in the database
        query = select(Workday.date)
        db_dates = session.execute(query).scalars().all()

        if date in db_dates:
            print(Fore.BLUE + "Workday already exists!")
        else:
            session.add(Workday(date=date, hours=hours, payment=payment))
            session.commit()
            print(Fore.GREEN + "Workday upload successful!")


def upload_address(info: dict[str, tkinter.Variable]):
    # Export the variables' input
    address = info["address"].get()
    latitude = info["latitude"].get()
    longitude = info["longitude"].get()

    # check_none_type returns (val,) because it's only one value in tuple.
    # To extract the val itself we use val[0]
    address = check_none_type(address)[0]

    with Session(engine) as session:
        query = select(Address.name)
        db_addresses = session.execute(query).scalars().all()

        if address in db_addresses:
            print(Fore.BLUE + "Address already exists!")
        else:
            session.add(Address(name=address, latitude=latitude, longitude=longitude))
            session.commit()
            print(Fore.GREEN + "Address upload successful!")


def upload_customer(info: dict[str, tkinter.Variable], address_name):
    # Export the variables' input
    customer_name = info["name"].get()
    floor = info["floor"].get()

    # Empty customer, floor entries means that the input is a string of length 0.
    # We need to make it NoneType, so the db can decline the input of an empty input.
    customer_name, floor = check_none_type(customer_name, floor)

    # If the customer name already exists and is already associated with the inputted address,
    # then the customer already exists in the database
    # Else,they have to be inserted into the database.
    with Session(engine) as session:
        subquery = select(Address.id).where(Address.name == address_name)
        sub_address_id = session.execute(subquery).scalars().first()
        query = select(Customer.name).where(Customer.address_id == sub_address_id)
        db_customers = session.execute(query).scalars().all()

        if customer_name in db_customers:
            print(Fore.BLUE + "Customer already exists!")
        else:
            session.add(Customer(name=customer_name, floor=floor, address_id=sub_address_id))
            session.commit()
            print(Fore.GREEN + "Customer upload successful!")


def upload_order(info: dict[str, tkinter.Variable], workday_date, customer_name, address_name):
    # Export the variables' input
    order_time = datetime.strptime(info["order time"].get(), "%H:%M:%S").time()
    delivery_time = datetime.strptime(info["delivery time"].get(), "%H:%M:%S").time()
    tips = info["tips"].get()
    tips_method = info["tips method"].get()
    source = info["source"].get()
    payment_method = info["payment method"].get()

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
        workday_id = session.execute(subquery_1).scalars().first()

        # Address id
        subquery_2 = select(Address.id).where(Address.name == address_name)
        address_id = session.execute(subquery_2).scalars().first()

        # Customer id
        subquery_3 = select(Customer.id).where(and_(
                                                    Customer.address_id == address_id,
                                                    Customer.name == customer_name
                                                   )
                                               )
        customer_id = session.execute(subquery_3).scalars().first()

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
        session.commit()
        print(Fore.GREEN + "Order upload successful!")
        print()


def upload_items(basket):
    basket_updated = []
    # Export the variables' input
    for item in basket:
        # Remove non-ingredient variables
        offer = item.pop("offer")
        category = item.pop("category")

        # Make empty StringVars to None
        for key in list(item.keys()):
            item[key] = check_none_type(item[key])[0]

        with Session(engine) as session:
            if category == "Coffee":
                new_item_info = {
                    "item": Coffee(**item),
                    "table": Coffee,
                    "product_type": "coffee",
                    "offer": offer
                }
            elif category == "Freddo or Flat":
                new_item_info = {
                    "item": FreddoFlat(**item),
                    "table": FreddoFlat,
                    "product_type": "freddo or flat",
                    "offer": offer
                }
            elif category == "Filter":
                new_item_info = {
                    "item": Filter(**item),
                    "table": Filter,
                    "product_type": "filter",
                    "offer": offer
                }
            elif category == "Chocolate":
                new_item_info = {
                    "item": Chocolate(**item),
                    "table": Chocolate,
                    "product_type": "chocolate",
                    "offer": offer
                }
            elif category == "Food":
                new_item_info = {
                    "item": Food(**item),
                    "table": Food,
                    "product_type": "food",
                    "offer": offer
                }
            elif category == "Beverage":
                new_item_info = {
                    "item": Beverage(**item),
                    "table": Beverage,
                    "product_type": "beverage",
                    "offer": offer
                }
            elif category == "Chamomile":
                new_item_info = {
                    "item": Chamomile(**item),
                    "table": Coffee,
                    "product_type": "chamomile",
                    "offer": offer
                }
            elif category == "Weird Chocolate":
                new_item_info = {
                    "item": WeirdChocolate(**item),
                    "table": WeirdChocolate,
                    "product_type": "weird chocolate",
                    "offer": offer
                }
            elif category == "Tee":
                new_item_info = {
                    "item": Tee(**item),
                    "table": Tee,
                    "product_type": "tee",
                    "offer": offer
                }
            elif category == "Smoothie":
                new_item_info = {
                    "item": Smoothie(**item),
                    "table": Smoothie,
                    "product_type": "smoothie",
                    "offer": offer
                }
            # Add the new item to the corresponding table
            session.add(new_item_info["item"])
            session.commit()

            # Store the new item info
            basket_updated.append(new_item_info)

    # Return the new item's info
    return basket_updated


def upload_items_polymorphic(basket_updated):
    for new_item_info in basket_updated:
        # Select the order that was just inserted
        with Session(engine) as session:
            # Find last recorder order id
            query = select(Order.id).order_by(Order.id.desc())
            order_id = session.execute(query).scalars().first()

            # Find offer id
            query = select(Offer.id).where(Offer.description == new_item_info["offer"])
            offer_id = session.execute(query).scalars().first()

            # Find product id
            query = select(new_item_info["table"].id).order_by(new_item_info["table"].id.desc())
            product_id = session.execute(query).scalars().first()

            # Extract product type
            product_type = new_item_info["product_type"]

            # Insert into "items"
            new_item = Item(product_id=product_id,
                            product_type=product_type,
                            order_id=order_id,
                            offer_id=offer_id)
            session.add(new_item)
            session.commit()


def upload_data(basket, tab1, tab2, tab3):
    # Get dicts
    workday_info = tab1.workday_frame.workday_dict
    address_info = tab2.address_frame.address_dict
    customer_info = tab2.customer_frame.customer_dict
    order_info = tab3.order_frame.order_dict

    # Perform check-up
    if data_valid(workday_info, address_info, customer_info, order_info, basket):
        # Upload workday
        upload_workday(workday_info)
        # Upload address
        upload_address(address_info)
        # Upload customer
        upload_customer(customer_info, address_info["address"].get())
        # Upload order
        upload_order(order_info, workday_info["date"].get(), customer_info["name"].get(), address_info["address"].get())
        # Upload items in category: Coffee, Food etc
        basket_updated = upload_items(basket)
        # Upload items in items' junction table
        upload_items_polymorphic(basket_updated)

        return True

    else:
        print(Fore.YELLOW + "Please validate your inputs")
        print()

        return False
