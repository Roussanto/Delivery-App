from datetime import datetime

import mysql.connector
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

from analysis_helpers import find_product

# Create a connection with the database
income_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Roussanto171!"
)

# Create a cursor
cursor = income_db.cursor()
# Access the database
cursor.execute("USE income;")

# Draw the data
data = {}
query = "SHOW TABLES;"
cursor.execute(query)
tables = [table_tuple[0] for table_tuple in cursor.fetchall()]
for table in tables:
    query = f"SELECT * FROM {table};"
    cursor.execute(query)
    table_df = pd.DataFrame(data=cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    table_df.set_index(keys="id", inplace=True)
    data.update({table: table_df})

# Get totals
totals = {}

# Tips
query = "SELECT SUM(tips) FROM orders;"
cursor.execute(query)
totals.update({"tips": float(cursor.fetchall()[0][0])})

# Orders
query = "SELECT COUNT(id) FROM orders;"
cursor.execute(query)
totals.update({"orders": cursor.fetchall()[0][0]})

# Money contributed
total_cost = 0
category_cost = {}
for table, df in list(data.items()):
    if "cost" in list(df.columns):
        category_cost.update({table: float(df["cost"].sum())})
        total_cost += df["cost"].sum()
totals.update({"money": total_cost})

# Revenue
totals.update({"revenue": float(data["workdays"]["payment"].sum()) + totals["tips"]})

# Select a date to analyze
orders_df = data["orders"]
X = orders_df["tips_method"]
y = np.array(orders_df["tips"]).reshape(-1, 1)

sns.scatterplot(data=orders_df, x="order_time", y="tips")
plt.show()

# Make categorical into numeric
le = LabelEncoder()
X = le.fit_transform(X).reshape(-1, 1)

# Create a model
model = LinearRegression()

# Train the model
model.fit(X, y)

# Predict
z = model.predict(np.array([[1]]))
print(z)
