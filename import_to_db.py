import mysql.connector

from amigoes_data import coffee_basket, freddo_basket, filter_basket, chocolate_basket, weird_chocolate_basket
from amigoes_data import other_beverage_basket, tee_basket, chamomile_basket, smoothie_basket, food_basket
from amigoes_data import offer_basket

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

# Insert coffees
query = ("INSERT INTO coffees (type, size, variety, sugar, sugar_type, milk, extra, cost)"
         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
cursor.executemany(query, coffee_basket)
income_db.commit()

# Insert freddos and flats
query = ("INSERT INTO freddos_flats (type, size, variety, sugar, sugar_type, milk, extra, cost)"
         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
cursor.executemany(query, freddo_basket)
income_db.commit()

# Insert filters
query = ("INSERT INTO filters (type, size, sugar, sugar_type, milk, extra, cost)"
         "VALUES (%s, %s, %s, %s, %s, %s, %s)")
cursor.executemany(query, filter_basket)
income_db.commit()

# Insert chocolates
query = ("INSERT INTO chocolates (type, temperature, extra, cost)"
         "VALUES (%s, %s, %s, %s)")
cursor.executemany(query, chocolate_basket)
income_db.commit()

# Insert weird chocolates
query = ("INSERT INTO weird_chocolates (type, extra, cost)"
         "VALUES (%s, %s, %s)")
cursor.executemany(query, weird_chocolate_basket)
income_db.commit()

# Insert beverages
query = ("INSERT INTO beverages (type, cost)"
         "VALUES (%s, %s)")
cursor.executemany(query, other_beverage_basket)
income_db.commit()

# Insert tees
query = ("INSERT INTO tees (type, variety, sugar, sugar_type, milk, extra, cost)"
         "VALUES (%s, %s, %s, %s, %s, %s, %s)")
cursor.executemany(query, tee_basket)
income_db.commit()

# Insert chamomiles
query = ("INSERT INTO chamomiles (type, sugar, sugar_type, milk, extra, cost)"
         "VALUES (%s, %s, %s, %s, %s, %s)")
cursor.executemany(query, chamomile_basket)
income_db.commit()

# Insert smoothies
query = ("INSERT INTO smoothies (type, milk, cost)"
         "VALUES (%s, %s, %s)")
cursor.executemany(query, smoothie_basket)
income_db.commit()

# Insert foods
query = ("INSERT INTO foods (type, cost)"
         "VALUES (%s, %s)")
cursor.executemany(query, food_basket)
income_db.commit()

# Insert offers
query = ("INSERT INTO offers (description, cost)"
         "VALUES (%s, %s)")
cursor.executemany(query, offer_basket)
income_db.commit()
