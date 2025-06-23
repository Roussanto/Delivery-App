from datetime import datetime
from fuzzywuzzy import fuzz
from colorama import Fore
import itertools
import mysql.connector


# This function connects to the mysql database and returns the database itself.
# The database is used as an input to upload into it data
def connect_database():
    # Connect to database
    income_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Roussanto171!"
    )

    # Create cursor object
    cursor = income_db.cursor()

    # Use database
    cursor.execute("USE income;")

    return income_db


# Empty address entry means that the input is a string of length 0.
# We need to make it NoneType, so the db can decline the input of an empty address.
# args is a tuple -> immutable. So, we create a list, new_vars, which we store the NoneTypes or initial existing values.
# new_args is returned unpacked
def check_none_type(*args):
    new_args = []
    for arg in args:
        if arg == "" or arg == "None":
            new_args.append(None)
        else:
            new_args.append(arg)

    return *new_args,


def workday_exists(database, date):
    cursor = database.cursor()
    # This query will produce a list of all the dates in the database
    query = "SELECT date FROM workdays"
    cursor.execute(query)

    # Collect all the dates that have been stored in the database
    db_dates = [db_workday[0] for db_workday in cursor.fetchall()]

    # If the GUI date is in the dates already stored in the database, then the workday already exists.
    if date in db_dates:
        return True
    else:
        return False


def address_exists(database, address):
    cursor = database.cursor()
    # This query will produce a list of all the addresses in the database
    query = "SELECT name FROM addresses"
    cursor.execute(query)

    # Collect all the address names that have been stored in the database
    db_addresses = [db_address[0] for db_address in cursor.fetchall()]

    # If the GUI address is in the addresses already stored in the database, then the address already exists.
    if address in db_addresses:
        return True
    else:
        return False


def customer_exists(database, address_name, customer_name):
    cursor = database.cursor()
    # This query will produce a list of all the customers who live in this address
    query = ("SELECT name FROM customers "
             f"WHERE address_id IN (SELECT id FROM addresses WHERE name = '{address_name}');")
    cursor.execute(query)

    # Collect all the residents of this address
    residents = [resident[0] for resident in cursor.fetchall()]

    # If the customer name is in the residents of the GUI address that have already been stored,
    # then the customer exists.
    if customer_name in residents:
        return True
    else:
        return False


def prepare_item_tab_for_next_item(tab4):
    # If multiple item categories are selected their frames stack up.
    # With the pack_forget() method we omit the previous frame if a new one is selected.
    tab4.recipe_frame.pack_forget()

    # Set offer combobox to "None"
    tab4.general_info_frame.offer_var.set("None")

    # Clear contents of item_dict so the next item of the same order can fill it
    tab4.item_dict.clear()


def make_basket_str(basket):
    basket_str = []
    for i, item_dict in enumerate(basket):
        item_str = f"Item {i + 1}: "
        for j, elem in enumerate(list(item_dict.values())):
            # The first element is always the offer type
            if j == 0:
                item_str += f"Offer - {elem}"
            # The second element is always the item category
            elif j == 1:
                item_str += f", Category - {elem}"
            # The first ingredient string is followed by ':' and a space
            elif j == 2:
                item_str += f": {elem}"
            # If an element does not exist, practically skip the appending
            elif elem == "":
                item_str += ""
            # If an element exists append it with a comma and a white space
            else:
                item_str += f", {elem}"
        # Fill the string basket with the new string item
        basket_str.append(item_str)
    return basket_str


# Create the strings necessary for the SQL query
def make_columns_str(item):
    column_str = "("
    values_str = "("
    for i, column in enumerate(list(item.keys())):
        if i != len(list(item.keys())) - 1:
            if column == "offer" or column == "category":
                column_str += ""
                values_str += ""
            else:
                column_str += f"{column}, "
                values_str += "%s, "
        else:
            column_str += f"{column})"
            values_str += "%s)"

    return column_str, values_str


def create_relations(cursor, item, customer_dict, address_dict, workday_dict, order_dict, db_tablename):
    # Detect order id
    workday_date = datetime.strptime(workday_dict["date"].get(), "%Y-%m-%d").date()
    order_time = datetime.strptime(order_dict["order time"].get(), "%H:%M:%S").time()
    customer_name = customer_dict["customer name"].get()
    address = address_dict["address"].get()
    query = (f"SELECT id FROM orders "
             f"WHERE customer_id = ("
             f"  SELECT id FROM customers"
             f"  WHERE name = '{customer_name}'"
             f"  AND address_id = ("
             f"     SELECT id FROM addresses"
             f"     WHERE name = '{address}'"
             f"  )"
             f")"
             f"AND workday_id = ("
             f"  SELECT id FROM workdays"
             f"  WHERE date = '{workday_date}'"
             f")"
             f"AND order_time = '{order_time}';")
    cursor.execute(query)
    order_id = cursor.fetchall()[0][0]

    # Detect offer id
    offer_desc = item["offer"]
    query = (f"SELECT id FROM offers "
             f"WHERE description = '{offer_desc}';")
    cursor.execute(query)
    offer_id = cursor.fetchall()[0][0]

    # Detect product id - We look for the item just inserted
    query = (f"SELECT id FROM {db_tablename} "
             f"ORDER BY id DESC LIMIT 1;")
    cursor.execute(query)
    product_id = cursor.fetchall()[0][0]

    # Detect product type
    product_type = str(item["category"]).lower()

    # Insert into "items"
    query = (f"INSERT INTO items (order_id, offer_id, product_id, product_type) "
             f"VALUES ({order_id}, {offer_id}, {product_id}, '{product_type}');")
    cursor.execute(query)


# For a selected workday create a dict containing addresses and their corresponding customers
def check_customer_misspellings():
    # Connect to the database
    database = connect_database()

    cursor = database.cursor()

    # Draw the addresses
    query = "SELECT name from addresses;"

    cursor.execute(query)
    selected_addresses = [add_tpl[0] for add_tpl in cursor.fetchall()]

    checks = []
    for add in selected_addresses:
        query = ("SELECT name FROM customers WHERE address_id IN ("
                 "  SELECT id FROM addresses"
                 f" WHERE name = '{add}');")
        cursor.execute(query)
        custs = [cust_tpl[0] for cust_tpl in cursor.fetchall()]
        checks.append({"address": add, "customers": custs})

    prob_checks = []
    for check in checks:
        for cust1, cust2 in list(itertools.product(check["customers"], repeat=2)):
            simil = fuzz.ratio(cust1, cust2)
            if 90 <= simil <= 99:
                if check not in prob_checks:
                    prob_checks.append(check)

    if prob_checks:
        for prob_check in prob_checks:
            print(prob_check)
    else:
        print(Fore.BLUE, "No misspellings!")
