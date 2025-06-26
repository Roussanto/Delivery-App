from datetime import datetime
from fuzzywuzzy import fuzz
from colorama import Fore
import itertools


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


def data_validation(workday_info, address_info, customer_info, order_info, basket):
    # Instantiate flags
    workday_correct = False
    address_correct = False
    customer_correct = False
    order_correct = False
    items_correct = []

    # Check workday input
    try:
        date = datetime.strptime(workday_info["date"].get(), "%Y-%m-%d").date()
        hours = workday_info["hours"].get()
        payment = workday_info["payment"].get()
    except ValueError:
        print(Fore.RED + "Workday: wrong data")
    else:
        if date and hours > 0 and payment > 0:
            workday_correct = True
        else:
            print(Fore.RED + "Workday: wrong data")

    # Check address input
    address = address_info["address"].get()
    latitude = address_info["latitude"].get()
    longitude = address_info["longitude"].get()

    if address and 36.0 <= latitude <= 38.0 and 23.0 <= longitude <= 24.0:
        address_correct = True
    else:
        print(Fore.RED + "Address: wrong data")

    # Check customer input
    customer_name = customer_info["name"].get()

    if customer_name:
        customer_correct = True
    else:
        print(Fore.RED + "Customer: wrong data")

    # Check order input
    try:
        order_time = datetime.strptime(order_info["order time"].get(), "%H:%M:%S").time()
        delivery_time = datetime.strptime(order_info["delivery time"].get(), "%H:%M:%S").time()
        tips = order_info["tips"].get()
        source = order_info["source"].get()
        payment_method = order_info["payment method"].get()
    except ValueError:
        print(Fore.RED + "Order: wrong data")
    else:
        if order_time and delivery_time and tips >= 0 and source and payment_method:
            order_correct = True
        else:
            print(Fore.RED + "Order: wrong data")

    # Check item input
    for item in basket:
        if item["category"] in ["Freddo or Flat", "Coffee"]:
            if item["type"] and item["size"] and item["variety"]:
                items_correct.append(True)
            else:
                items_correct.append(False)


    # Validate results
    if workday_correct and address_correct and customer_correct and order_correct:
        return True
    else:
        workday_correct = False
        address_correct = False
        customer_correct = False
        order_correct = False

        return False




# For a selected workday create a dict containing addresses and their corresponding customers
def check_customer_misspellings():
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
