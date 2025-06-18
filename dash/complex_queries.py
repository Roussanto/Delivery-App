from datetime import datetime

import pandas as pd

from analysis import data

# Make a join table of workdays and orders and count tips for specific date
workdays_df = data["workdays"]
orders_df = data["orders"]

merged = pd.merge(workdays_df, orders_df, left_on="id", right_on="workday_id")

chosen_dates = [datetime(2024, 12, 6).date()]
specific_tips = merged.loc[merged["date"].isin(chosen_dates)]["tips"].sum()
