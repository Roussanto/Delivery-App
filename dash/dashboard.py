from datetime import datetime

import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd

from analysis import data, totals
from analysis_helpers import find_product

# Instantiate the app
app = dash.Dash(__name__)

app.layout = (html.Div(
    children=[
        html.H1(children=f"Revenue: {totals["revenue"]}€", id="revenue-stat"),
        html.H1(children=f"Total tips: {round(totals["tips"])}€", id="tips-stat"),
        html.H1(children=f"Total orders: {totals["orders"]}", id="orders-stat"),
        html.H1(children=f"Money contributed: {totals["money"]}€", id="money_cont-stat"),
        dcc.Dropdown(options=data["workdays"]["date"].values,
                     multi=True,
                     id="dropdown-workdays"),
        dcc.Dropdown(options=["80% arabica + 20% robusta", "100% arabica", "decaffeine"],
                     multi=True,
                     id="dropdown-fig"),
        dcc.Graph(figure=px.bar(data_frame=data["coffees"], x="type", color="variety", barmode="stack"),
                  id="coffees-fig")
    ])
)


@callback(
    Output(component_id="revenue-stat", component_property="children"),
    Output(component_id="tips-stat", component_property="children"),
    Output(component_id="orders-stat", component_property="children"),
    Output(component_id="money_cont-stat", component_property="children"),
    Input(component_id="dropdown-workdays", component_property="value")
)
def update_earnings(work_dates: list[str]):
    if not work_dates:
        return (f"Revenue: {totals["revenue"]}€",
                f"Total tips: {round(totals["tips"])}€",
                f"Total orders: {totals["orders"]}",
                f"Money contributed: {totals["money"]}€")
    else:
        # Make dropdown values to datetime() objects to compare with workdays dates()
        for i in range(len(work_dates)):
            work_dates[i] = datetime.strptime(work_dates[i], "%Y-%m-%d").date()
        # Access dataframes
        workdays_df = data["workdays"]
        orders_df = data["orders"]
        items_df = data["items"]
        # Filter workday payment
        filtered_workdays_df = workdays_df.loc[workdays_df["date"].isin(work_dates)]
        filtered_payment = filtered_workdays_df["payment"].sum()
        # Filter tips
        merged_wd_ord = pd.merge(workdays_df, orders_df, left_on="id", right_on="workday_id")
        filtered_tips = merged_wd_ord.loc[merged_wd_ord["date"].isin(work_dates)]["tips"].sum()
        # Filter orders
        filtered_orders = merged_wd_ord.loc[merged_wd_ord["date"].isin(work_dates)]["order_time"].count()
        # Filter contributed money
        merged_contrib = pd.merge(data["orders"], data["items"], left_on="id", right_on="order_id")
        merged_contrib = pd.merge(merged_contrib, data["workdays"], left_on="workday_id", right_on="id")
        filtered_contrib = merged_contrib.loc[merged_contrib["date"].isin(work_dates)]
        total_cost_filtered = 0
        # For every table if a table has the column "cost" (which means that it is an item table)
        # then calculate its individual cost and the total cost
        for table, df in list(data.items()):
            if "cost" in list(df.columns):
                product = find_product(table)
                filtered_contrib_tab = pd.merge(filtered_contrib.loc[filtered_contrib["product_type"] == product],
                                                df,
                                                left_on="product_id",
                                                right_on="id")
                table_cost = filtered_contrib_tab["cost"].sum()
                total_cost_filtered += table_cost

        return (f"Revenue: {filtered_payment + filtered_tips}€",
                f"Tips: {filtered_tips}€",
                f"Total orders: {filtered_orders}",
                f"Money contributed: {total_cost_filtered}€")


@callback(
    Output(component_id="coffees-fig", component_property="figure"),
    Input(component_id="dropdown-fig", component_property="value")
)
def update_fig(varieties: list[str]):
    # Necessary to state that I will fall back on my default figure if no varieties are selected
    if not varieties:
        return px.bar(data_frame=data["coffees"], x="type", color="variety", barmode="stack")
    else:
        coffees_df = data["coffees"]
        filtered_coffees_df = coffees_df.loc[coffees_df["variety"].isin(varieties)]
        coffees_fig = px.bar(data_frame=filtered_coffees_df, x="type", color="variety", barmode="stack")
        return coffees_fig


if __name__ == "__main__":
    app.run(debug=True)
