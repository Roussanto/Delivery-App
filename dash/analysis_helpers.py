def find_product(table):
    product = 0
    if table == "coffees":
        product = "coffee"
    elif table == "freddos_flats":
        product = "freddo or flat"
    elif table == "filters":
        product = "filter"
    elif table == "beverages":
        product = "beverage"
    elif table == "chamomiles":
        product = "chamomile"
    elif table == "chocolates":
        product = "chocolate"
    elif table == "foods":
        product = "food"
    elif table == "smoothies":
        product = "smoothie"
    elif table == "tees":
        product = "tee"
    elif table == "weird_chocolates":
        product = "weird_chocolate"

    return product