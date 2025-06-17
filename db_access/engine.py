import mysql.connector

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

cursor.execute("SELECT id FROM workdays WHERE date = '2024-10-10';")
print(cursor.fetchall()[0][0])

dct = {"a": 1, "b": 2, "c": 10, "d": 18}
lst = [val for key, val in list(dct.items()) if key not in ["a", "c"]]
tpl = tuple(lst)
print(tpl)
