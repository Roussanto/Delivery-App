from datetime import datetime

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from colorama import Fore

from orm.model import Workday, Address, Customer
from func import check_none_type

# Create a connection
engine = create_engine(
    "mysql+pymysql://root:Roussanto171!@localhost:3306/income",
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
        query = select(Customer.name)
        db_customers = session.execute(query).scalars().all()

        if customer_name in db_customers:
            print(Fore.BLUE + "Customer already exists!")
        else:
            with session.begin():
                session.add(Customer(name=customer_name, floor=floor))
            print(Fore.GREEN + "Customer upload successful!")