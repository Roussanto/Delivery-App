import tkinter as tk
from tkinter import ttk
import _tkinter
from colorama import Fore

from uploads_2 import upload_data
from settings import WIDGET_PAD
from func import make_basket_str, prepare_item_tab_for_next_item, check_customer_misspellings
from data.costs import *

# Upload addresses
address_log = []
with open("address_log.txt", "r") as log:
    lines = log.readlines()
    for line in lines:
        line = line.rstrip()
        address_log.append(line)


# The app inherits from tk.Tk. The class is the main window.
class App(tk.Tk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")

        # We create the notebook and the n 2 "pages", the tabs, that we say they are part of the notebook
        # by making it their parent. Each page has its own attributes.
        # After creating the inheritance we add them to the notebook
        self.notebook = ttk.Notebook()

        # Create the tabs
        self.tab1 = Tab1Frame(self.notebook)
        self.tab2 = Tab2Frame(self.notebook)
        self.tab3 = Tab3Frame(self.notebook)
        self.tab4 = Tab4Frame(self.notebook)

        # Add them to the notebook
        self.notebook.add(self.tab1, text="Workday")
        self.notebook.add(self.tab2, text="Address and Customer")
        self.notebook.add(self.tab3, text="Order")
        self.notebook.add(self.tab4, text="Items")

        # Place the notebook on the app
        self.notebook.pack()

        # All items that will get into the basket will be stored here
        self.basket = []
        # Initialise order cost
        self.order_cost = 0

        # Order details: necessary details for Review tab(5) display
        self.order_details = {"basket_format": "",
                              "order_cost": 0,
                              "address": "",
                              "customer": ""}

        def press_add_to_basket():
            # Draw the tk.Var contents and save them as a list.
            item = {key: value.get() for key, value in self.tab4.item_dict.items()}
            # Create a basket of items
            self.basket.append(item)
            # Calculate total order cost
            # If item part of offer divide its cost by 3 (=amount of items of every offer)
            if item["offer"] == "None" or item["offer"] == "":
                self.order_cost += float(item["cost"])
            else:
                self.order_cost += self.tab4.general_info_frame.offer_cost_var.get()/3
            self.order_details.update({"order_cost": self.order_cost})

            # Format basket: list -> basket: str
            self.basket_format = make_basket_str(self.basket)
            self.order_details.update({"basket_format": self.basket_format})

            # Update the address and the customer in the order details for the review panel
            self.order_details.update({"address": self.tab2.address_frame.address_var.get()})
            self.order_details.update({"customer": self.tab2.customer_frame.customer_var.get()})

            # Update the address log
            if self.tab2.address_frame.address_var.get() not in address_log:
                with open("address_log.txt", "a") as log:
                    log.write(f"\n{self.tab2.address_frame.address_var.get()}")
                # Reopen the updated address log
                with open("address_log.txt", "r") as log:
                    lines = log.readlines()
                    for line in lines:
                        line = line.rstrip()
                        address_log.append(line)

            # As soon as an item is created, create the review tab
            # In order to update the tab every time we insert a new item we have to "blink" (like in Pygame)
            if len(self.basket_format) == 1:
                self.tab5 = Tab5Frame(self.notebook, self.order_details)
                self.notebook.add(self.tab5, text="Review")
            else:
                self.tab5.destroy()
                self.tab5 = Tab5Frame(self.notebook, self.order_details)
                self.notebook.add(self.tab5, text="Review")

            # Remove the item frame and clear the offer contents so the next item can be inserted
            prepare_item_tab_for_next_item(self.tab4)

        # When the Upload button is pressed the data will be stored in the database.
        def press_upload():
            if upload_data(self.basket, self.tab1, self.tab2, self.tab3):
                # Empty the basket
                self.basket.clear()
                # Clear order cost
                self.order_cost = 0
                # Clear Review panel
                self.tab5.destroy()

        def press_remove_from_basket():
            item_rem_num = self.remove_var.get()
            if item_rem_num > len(self.basket):
                print(Fore.RED + "Selected item index does not exists!")
            for i, item in enumerate(self.basket):
                if i + 1 == item_rem_num:
                    # Isolate the item to be removed
                    item_rem = item
                    # Remove it from the basket
                    self.basket.remove(item_rem)
                    # Update "Review" tab indexing visual - Update basket format and then "blink" tab 5
                    self.basket_format = make_basket_str(self.basket)
                    self.order_details.update({"basket_format": self.basket_format})
                    # Blip
                    self.tab5.destroy()
                    self.tab5 = Tab5Frame(self.notebook, self.order_details)
                    self.notebook.add(self.tab5, text="Review")
                    # If by deleting an item the basket becomes empty, complete destroy tab 5
                    if len(self.basket) == 0:
                        self.tab5.destroy()

        # When the 1st tab (Workdays) is selected, the "Check customer misspellings" button will appear
        # When the 3rd tab (Items) is pressed, the "Add to basket" button will appear.
        # When the 4th tab (Review) is pressed, the "Upload" button will appear.
        # Until either of the Review or Items tab is pressed an AttributeError appears:
        # '_tkinter.tkapp' object has no attribute 'upload_button'/'basket_button'.
        # An exception is added to prevent the display of this error until the Items or the Review tab is pressed.
        def on_tab_selected(event):
            try:
                selected_tab = self.notebook.tab(self.notebook.select(), "text")
                # Create the "Check customer misspellings" button
                if selected_tab == "Workday":
                    self.misspell_button = ttk.Button(self, text="Check customer misspellings", command=check_customer_misspellings)
                    self.misspell_button.pack()
                else:
                    self.misspell_button.pack_forget()

                # Create the "Add to basket" button
                if selected_tab == "Items":
                    self.basket_button = ttk.Button(self, text="Add to basket", command=press_add_to_basket)
                    self.basket_button.pack()
                else:
                    self.basket_button.pack_forget()

                # Create the "Upload" button, the "Remove Item" button and the "Remove Item" label and entry
                if selected_tab == "Review":
                    # IntVars
                    self.remove_var = tk.IntVar(value=1)

                    # Widgets
                    self.upload_button = ttk.Button(self, text="Upload", command=press_upload)

                    self.remove_label = ttk.Label(self, text="Choose item to remove: ")
                    self.remove_entry = ttk.Entry(self, textvariable=self.remove_var)
                    self.remove_button = ttk.Button(self, text="Remove Item", command=press_remove_from_basket)

                    # Widget placement
                    self.upload_button.pack(pady=5)
                    self.remove_label.pack()
                    self.remove_entry.pack()
                    self.remove_button.pack()

                else:
                    self.upload_button.pack_forget()
                    self.remove_label.pack_forget()
                    self.remove_entry.pack_forget()
                    self.remove_button.pack_forget()
            except AttributeError:
                pass

        self.notebook.bind("<<NotebookTabChanged>>", func=on_tab_selected)

        self.mainloop()


#############
# First tab - Workday
class Tab1Frame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.workday_frame = WorkdayFrame(self)


class WorkdayFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Place the frame
        self.pack()

        # Create the variables
        self.define_variables()
        # Create the widgets
        self.create_widgets()
        # Establish layout
        self.create_layout()

    def define_variables(self):
        self.date_var = tk.StringVar(value="2000-04-26")
        self.hours_var = tk.IntVar(value=10)
        self.payment_var = tk.DoubleVar(value=10.0)

        # Variables are stored in a dict -> sent easier as package to function "Upload"
        self.workday_dict = {"date": self.date_var,
                             "hours": self.hours_var,
                             "payment": self.payment_var}

    def create_widgets(self):
        # Frame header widget
        self.header = ttk.Label(self, text="Workday")

        # "Input date" widget
        self.date_label = ttk.Label(self, text="Input date: ")
        self.date_entry = ttk.Entry(self, textvariable=self.date_var)

        # "Input hours" widget
        self.hours_label = ttk.Label(self, text="Input hours: ")
        self.hours_entry = ttk.Entry(self, textvariable=self.hours_var)

        # "Input payment" widget
        self.payment_label = ttk.Label(self, text="Input payment: ")
        self.payment_entry = ttk.Entry(self, textvariable=self.payment_var)

    def create_layout(self):
        # Create 4x2 grid
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1)

        # Frame header position
        self.header.grid(row=0, column=0, columnspan=2)

        # "Input date" widget position
        self.date_label.grid(row=1, column=0, sticky="e", pady=WIDGET_PAD)
        self.date_entry.grid(row=1, column=1, pady=WIDGET_PAD)

        # "Input hours" widget position
        self.hours_label.grid(row=2, column=0, sticky="e", pady=WIDGET_PAD)
        self.hours_entry.grid(row=2, column=1, pady=WIDGET_PAD)

        # "Input payment" widget position
        self.payment_label.grid(row=3, column=0, sticky="e", pady=WIDGET_PAD)
        self.payment_entry.grid(row=3, column=1, pady=WIDGET_PAD)


#############
# Second tab - Address and Customer
class Tab2Frame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.address_frame = AddressFrame(self)
        self.customer_frame = CustomerFrame(self)


class AddressFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Place the frame
        self.pack()

        # Create the variables
        self.define_variables()
        # Create the widgets
        self.create_widgets()
        # Establish layout
        self.create_layout()

        self.address_entry.bind("<KeyRelease>", self.check_log)

    def define_variables(self):
        self.address_var = tk.StringVar(value="Kantouni")
        self.lat_var = tk.DoubleVar(value=37.0)
        self.long_var = tk.DoubleVar(value=23.5)

        # Variables are stored in a dict -> sent easier as package to function "Upload"
        self.address_dict = {"address": self.address_var,
                             "latitude": self.lat_var,
                             "longitude": self.long_var}

    def create_widgets(self):
        # Frame header widget
        self.header = ttk.Label(self, text="Address")

        # "Input address" widget
        self.address_label = ttk.Label(self, text="Input address: ")
        self.address_entry = ttk.Entry(self, textvariable=self.address_var)

        # "Input latitude" widget
        self.lat_label = ttk.Label(self, text="Input latitude: ")
        self.lat_entry = ttk.Entry(self, textvariable=self.lat_var)

        # "Input longitude" widget
        self.long_label = ttk.Label(self, text="Input longitude: ")
        self.long_entry = ttk.Entry(self, textvariable=self.long_var)

    def create_layout(self):
        # Create 4x2 grid
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1)

        # Frame header position
        self.header.grid(row=0, column=0, columnspan=2)

        # "Input address" widget position
        self.address_label.grid(row=1, column=0, sticky="e", pady=WIDGET_PAD)
        self.address_entry.grid(row=1, column=1, pady=WIDGET_PAD)

        # "Input latitude" widget position
        self.lat_label.grid(row=2, column=0, sticky="e", pady=WIDGET_PAD)
        self.lat_entry.grid(row=2, column=1, pady=WIDGET_PAD)

        # "Input longitude" widget position
        self.long_label.grid(row=3, column=0, sticky="e", pady=(WIDGET_PAD, WIDGET_PAD + 10))
        self.long_entry.grid(row=3, column=1, pady=(WIDGET_PAD, WIDGET_PAD + 10))

    def check_log(self, event):
        # Log the address - Used to identify easier
        # Make address entry green
        if self.address_var.get() in address_log:
            self.address_entry.configure(foreground="green")
        else:
            self.address_entry.configure(foreground="black")


class CustomerFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Place the frame
        self.pack()

        # Create the variables
        self.define_variables()
        # Create the widgets
        self.create_widgets()
        # Establish layout
        self.create_layout()

    def define_variables(self):
        self.customer_var = tk.StringVar(value="Eirini")
        self.floor_var = tk.IntVar()

        # Variables are stored in a dict -> sent easier as package to function "Upload"
        self.customer_dict = {"name": self.customer_var,
                              "floor": self.floor_var}

    def create_widgets(self):
        # Frame header widget
        self.header = ttk.Label(self, text="Customer")

        # "Input customer name" widget
        self.customer_label = ttk.Label(self, text="Input customer name: ")
        self.customer_entry = ttk.Entry(self, textvariable=self.customer_var)

        # "Input floor" widget
        self.floor_label = ttk.Label(self, text="Input floor: ")
        self.floor_entry = ttk.Entry(self, textvariable=self.floor_var)

    def create_layout(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2), weight=1)

        # Frame header position
        self.header.grid(row=0, column=0, columnspan=2)

        # "Input customer name" widget position
        self.customer_label.grid(row=1, column=0, sticky="e", pady=WIDGET_PAD)
        self.customer_entry.grid(row=1, column=1, pady=WIDGET_PAD)

        # "Input floor" widget position
        self.floor_label.grid(row=2, column=0, sticky="e", pady=WIDGET_PAD)
        self.floor_entry.grid(row=2, column=1, pady=WIDGET_PAD)


# Third tab - Order details
class Tab3Frame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.order_frame = OrderFrame(self)


class OrderFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Place the frame
        self.pack()

        # Create the variables
        self.define_variables()
        # Create the widgets
        self.create_widgets()
        # Establish layout
        self.create_layout()

    def define_variables(self):
        self.order_time_var = tk.StringVar(value="10:00:00")
        self.delivery_time_var = tk.StringVar(value="11:00:00")
        self.tips_var = tk.DoubleVar()
        self.tips_method_var = tk.StringVar()
        self.source_var = tk.StringVar(value="Efood")
        self.payment_method_var = tk.StringVar(value="Card")

        self.tips_var.trace_add("write", self.check_tips)
        self.tips_method_var.trace_add("write", self.auto_card_select)
        self.source_var.trace_add("write", self.auto_phone_cash)

        # Variables are stored in a dict -> sent easier as package to function "Upload"
        self.order_dict = {"order time": self.order_time_var,
                           "delivery time": self.delivery_time_var,
                           "tips": self.tips_var,
                           "tips method": self.tips_method_var,
                           "source": self.source_var,
                           "payment method": self.payment_method_var}

    def create_widgets(self):
        # Frame header widget
        self.header = ttk.Label(self, text="Order")

        # "Input order time" widget
        self.order_time_label = ttk.Label(self, text="Input time of the order: ")
        self.order_time_entry = ttk.Entry(self, textvariable=self.order_time_var)

        # "Input delivery time" widget
        self.delivery_time_label = ttk.Label(self, text="Input time of the delivery: ")
        self.delivery_time_entry = ttk.Entry(self, textvariable=self.delivery_time_var)

        # "Input tips amount" widget
        self.tips_label = ttk.Label(self, text="Input tips amount: ")
        self.tips_entry = ttk.Entry(self, textvariable=self.tips_var)

        # "Tips: cash or card" widget
        self.tips_method_label = ttk.Label(self, text="Tips in: ")
        self.tips_method_combo = ttk.Combobox(self, textvariable=self.tips_method_var, values=["Cash", "Card"])
        self.tips_method_combo.config(state="disabled")

        # "Input order source" widget
        self.source_label = ttk.Label(self, text="Order was made using: ")
        self.source_combo = ttk.Combobox(self, textvariable=self.source_var, values=["Efood", "Wolt", "Box", "Phone"])

        # "Payment: cash or card" widget
        self.payment_method_label = ttk.Label(self, text="Payment in: ")
        self.payment_method_combo = ttk.Combobox(self, textvariable=self.payment_method_var, values=["Cash", "Card"])

    def create_layout(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Frame header position
        self.header.grid(row=0, column=0, columnspan=2)

        # "Input order time" widget position
        self.order_time_label.grid(row=1, column=0, sticky="e", pady=WIDGET_PAD)
        self.order_time_entry.grid(row=1, column=1, pady=WIDGET_PAD)

        # "Input delivery time" widget position
        self.delivery_time_label.grid(row=2, column=0, sticky="e", pady=WIDGET_PAD)
        self.delivery_time_entry.grid(row=2, column=1, pady=WIDGET_PAD)

        # "Input tips" widget position
        self.tips_label.grid(row=3, column=0, sticky="e", pady=WIDGET_PAD)
        self.tips_entry.grid(row=3, column=1, pady=WIDGET_PAD)

        # "Input tips method" widget position
        self.tips_method_label.grid(row=4, column=0, sticky="e", pady=WIDGET_PAD)
        self.tips_method_combo.grid(row=4, column=1, pady=WIDGET_PAD)

        # "Input order source" widget position
        self.source_label.grid(row=5, column=0, sticky="e", pady=WIDGET_PAD)
        self.source_combo.grid(row=5, column=1, pady=WIDGET_PAD)

        # "Input payment method" widget position
        self.payment_method_label.grid(row=6, column=0, sticky="e", pady=WIDGET_PAD)
        self.payment_method_combo.grid(row=6, column=1, pady=WIDGET_PAD)

    # if no tips are added disable the option to add tips origin
    def check_tips(self, *args):
        try:
            if self.tips_var.get() == 0.0:
                self.tips_method_combo.config(state="disabled")
                self.tips_method_var.set("None")
            elif self.tips_var.get() in [0.5, 0.75, 1, 2]:
                self.tips_method_var.set("Card")
                self.tips_method_combo.config(state="normal")
            else:
                self.tips_method_var.set("Cash")
                self.tips_method_combo.config(state="normal")
        # for some reason if tips_var is empty _tkinter.TclError is raised. Disable tip option if this is raised
        except _tkinter.TclError:
            self.tips_method_combo.config(state="disabled")

    # If tips are given by card then payment method will be in card
    def auto_card_select(self, *args):
        if self.tips_method_var.get() == "Card":
            self.payment_method_var.set("Card")

    # If the source is "phone" then the payment will always be in cash
    def auto_phone_cash(self, *args):
        if self.source_var.get() == "Phone":
            self.payment_method_var.set("Cash")


############
# Fourth tab - Item insert
class Tab4Frame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.general_info_frame = GeneralInfoFrame(self)
        self.combo_select_num = 0

        self.general_info_frame.offer_combo.bind("<<ComboboxSelected>>", self.offer_combo_select)
        self.general_info_frame.item_type_combo.bind("<<ComboboxSelected>>", self.item_combo_select)

    def offer_combo_select(self, event):
        if self.general_info_frame.offer_var.get() == "None":
            self.general_info_frame.offer_cost_var.set(0.0)
        elif self.general_info_frame.offer_var.get() == "coffee, toast, fresh orange juice":
            self.general_info_frame.offer_cost_var.set(5.5)
        elif self.general_info_frame.offer_var.get() == "coffee, soft cookie, water":
            self.general_info_frame.offer_cost_var.set(4.0)
        elif self.general_info_frame.offer_var.get() == "coffee, bagel, mini donut":
            self.general_info_frame.offer_cost_var.set(4.3)

    def item_combo_select(self, event):
        self.combo_select_num += 1
        # Delete previous item frame to make space for the new one
        if self.combo_select_num >= 2:
            self.recipe_frame.pack_forget()

        self.item_dict = {"offer": self.general_info_frame.offer_var,
                          "category": self.general_info_frame.item_type_var}

        category = self.general_info_frame.item_type_var.get()

        if category == "Coffee":
            self.recipe_frame = CoffeeFrame(self, self.item_dict["offer"])
        elif category == "Freddo or Flat":
            self.recipe_frame = FreddoFlatFrame(self, self.item_dict["offer"])
        elif category == "Filter":
            self.recipe_frame = FilterFrame(self, self.item_dict["offer"])
        elif category == "Chocolate":
            self.recipe_frame = ChocolateFrame(self, self.item_dict["offer"])
        elif category == "Food":
            self.recipe_frame = FoodFrame(self, self.item_dict["offer"])
        elif category == "Beverage":
            self.recipe_frame = BeverageFrame(self, self.item_dict["offer"])
        elif category == "Chamomile":
            self.recipe_frame = ChamomileFrame(self, self.item_dict["offer"])
        elif category == "Weird Chocolate":
            self.recipe_frame = WeirdChocolateFrame(self, self.item_dict["offer"])
        elif category == "Tee":
            self.recipe_frame = TeeFrame(self, self.item_dict["offer"])
        elif category == "Smoothie":
            self.recipe_frame = SmoothieFrame(self, self.item_dict["offer"])
        else:
            pass

        self.item_dict.update(self.recipe_frame.recipe_dict)


class GeneralInfoFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Place the frame
        self.pack()

        # Create the variables
        self.define_variables()
        # Create the widgets
        self.create_widgets()
        # Establish layout
        self.create_layout()

        self.offer_cost_entry.config(state="disabled")

    def define_variables(self):
        self.offer_var = tk.StringVar(value="None")
        self.item_type_var = tk.StringVar()
        self.offer_cost_var = tk.DoubleVar()

    def create_widgets(self):
        # Frame header widget
        self.header = ttk.Label(self, text="General Info")

        # "Input offer" widget
        self.offer_label = ttk.Label(self, text="Input offer type: ")
        self.offer_combo = ttk.Combobox(self, textvariable=self.offer_var, values=["None",
                                                                                   "coffee, toast, fresh orange juice",
                                                                                   "coffee, soft cookie, water",
                                                                                   "coffee, bagel, mini donut"])

        self.offer_cost_label = ttk.Label(self, text=f"Offer's cost: ")
        self.offer_cost_entry = ttk.Entry(self, textvariable=self.offer_cost_var)

        # "Input item type" widget
        self.item_type_label = ttk.Label(self, text="Input item type: ")
        self.item_type_combo = ttk.Combobox(self, textvariable=self.item_type_var, values=["Coffee",
                                                                                           "Freddo or Flat",
                                                                                           "Filter",
                                                                                           "Food",
                                                                                           "Beverage",
                                                                                           "Chocolate",
                                                                                           "Chamomile",
                                                                                           "Tee",
                                                                                           "Weird Chocolate",
                                                                                           "Smoothie"])

    def create_layout(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1)

        # Frame header position
        self.header.grid(row=0, column=0, columnspan=2)

        # "Input offer type" widget position
        self.offer_label.grid(row=1, column=0, sticky="e", pady=WIDGET_PAD)
        self.offer_combo.grid(row=1, column=1, pady=WIDGET_PAD)

        # "Input offer cost" widget position
        self.offer_cost_label.grid(row=2, column=0, sticky="e", pady=WIDGET_PAD)
        self.offer_cost_entry.grid(row=2, column=1, pady=WIDGET_PAD)

        # "Input item type" widget position
        self.item_type_label.grid(row=3, column=0, sticky="e", pady=WIDGET_PAD)
        self.item_type_combo.grid(row=3, column=1, pady=WIDGET_PAD)


class CoffeeFrame(ttk.Frame):
    def __init__(self, master, offer_type):
        super().__init__(master)
        self.offer_type = offer_type

        # Place the frame
        self.pack()

        # Create the variables
        self.define_variables()
        # Create the widgets
        self.create_widgets()
        # Establish layout
        self.create_layout()

        self.coffee_type_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.size_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.variety_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.sugar_type_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.milk_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.extra_combo.bind("<<ComboboxSelected>>", self.calculate_price)

    def define_variables(self):
        self.coffee_type_var = tk.StringVar(value="cappuccino")
        self.size_var = tk.StringVar(value="double")
        self.variety_var = tk.StringVar(value="80% arabica + 20% robusta")
        self.sugar_var = tk.StringVar()
        self.sugar_type_var = tk.StringVar()
        self.milk_var = tk.StringVar()
        self.extra_var = tk.StringVar()
        self.cost_var = tk.DoubleVar(value=CAP_2)

        self.sugar_var.trace_add("write", self.check_sugar)

        self.recipe_dict = {"type": self.coffee_type_var,
                            "size": self.size_var,
                            "variety": self.variety_var,
                            "sugar": self.sugar_var,
                            "sugar_type": self.sugar_type_var,
                            "milk": self.milk_var,
                            "extra": self.extra_var,
                            "cost": self.cost_var}

    def create_widgets(self):
        # Frame header widget
        self.header = ttk.Label(self, text="Item Recipe")

        # "Input coffee type" widget
        self.coffee_type_label = ttk.Label(self, text="Coffee type: ")
        self.coffee_type_combo = ttk.Combobox(self, textvariable=self.coffee_type_var, values=["espresso",
                                                                                               "espresso machiatto",
                                                                                               "espresso americano",
                                                                                               "cappuccino",
                                                                                               "cappuccino latte",
                                                                                               "nes",
                                                                                               "frappe"])

        # "Input size" widget
        self.size_label = ttk.Label(self, text="Size: ")
        self.size_combo = ttk.Combobox(self, textvariable=self.size_var, values=["single",
                                                                                 "double",
                                                                                 "quadruple"])

        # "Input variety" widget
        self.variety_label = ttk.Label(self, text="Variety: ")
        self.variety_combo = ttk.Combobox(self, textvariable=self.variety_var, values=["80% arabica + 20% robusta",
                                                                                       "100% arabica",
                                                                                       "decaffeine"])

        # "Input sugar" widget
        self.sugar_label = ttk.Label(self, text="Sugar: ")
        self.sugar_combo = ttk.Combobox(self, textvariable=self.sugar_var, values=[None,
                                                                                   "little",
                                                                                   "medium",
                                                                                   "medium-to-sweet",
                                                                                   "sweet",
                                                                                   "very sweet"])

        # "Input sugar type" widget
        self.sugar_type_label = ttk.Label(self, text="Sugar Type: ")
        self.sugar_type_combo = ttk.Combobox(self, textvariable=self.sugar_type_var, values=[None,
                                                                                        "white",
                                                                                        "brown",
                                                                                        "saccharin",
                                                                                        "stevia",
                                                                                        "honey"])

        # "Input milk" widget
        self.milk_label = ttk.Label(self, text="Milk: ")
        self.milk_combo = ttk.Combobox(self, textvariable=self.milk_var, values=[None,
                                                                                 "fresh",
                                                                                 "evapore",
                                                                                 "almond",
                                                                                 "coconut",
                                                                                 "oat"])

        # "Input extra" widget
        self.extra_label = ttk.Label(self, text="Extra: ")
        self.extra_combo = ttk.Combobox(self, textvariable=self.extra_var, values=[None,
                                                                                   "chocolate syrup",
                                                                                   "strawberry syrup",
                                                                                   "caramel syrup",
                                                                                   "hazelnut syrup",
                                                                                   "vanilla syrup",
                                                                                   "cinnamon powder",
                                                                                   "chocolate powder"])

        # "Input cost" widget
        self.cost_label = ttk.Label(self, text="Cost: ")
        self.cost_entry = ttk.Entry(self, textvariable=self.cost_var)

    def create_layout(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        # Frame header position
        self.header.grid(row=0, column=0, columnspan=2)

        # "Input coffee type" widget position
        self.coffee_type_label.grid(row=1, column=0, sticky="e", pady=WIDGET_PAD)
        self.coffee_type_combo.grid(row=1, column=1, pady=WIDGET_PAD)

        # "Input size" widget position
        self.size_label.grid(row=2, column=0, sticky="e", pady=WIDGET_PAD)
        self.size_combo.grid(row=2, column=1, pady=WIDGET_PAD)

        # "Input variety" widget position
        self.variety_label.grid(row=3, column=0, sticky="e", pady=WIDGET_PAD)
        self.variety_combo.grid(row=3, column=1, pady=WIDGET_PAD)

        # "Input sugar" widget position
        self.sugar_label.grid(row=4, column=0, sticky="e", pady=WIDGET_PAD)
        self.sugar_combo.grid(row=4, column=1, pady=WIDGET_PAD)

        # "Input sugar type" widget position
        self.sugar_type_label.grid(row=5, column=0, sticky="e", pady=WIDGET_PAD)
        self.sugar_type_combo.grid(row=5, column=1, pady=WIDGET_PAD)

        # "Input milk" widget position
        self.milk_label.grid(row=6, column=0, sticky="e", pady=WIDGET_PAD)
        self.milk_combo.grid(row=6, column=1, pady=WIDGET_PAD)

        # "Input extra" widget position
        self.extra_label.grid(row=7, column=0, sticky="e", pady=WIDGET_PAD)
        self.extra_combo.grid(row=7, column=1, pady=WIDGET_PAD)

        # "Input cost" widget position
        self.cost_label.grid(row=8, column=0, sticky="e", pady=WIDGET_PAD)
        self.cost_entry.grid(row=8, column=1, sticky="w", pady=WIDGET_PAD)

    # if no sugar is added disable the option to add tips origin
    def check_sugar(self, *args):
        if self.sugar_var.get() == "None":
            self.sugar_type_var.set("None")
            self.sugar_type_combo.config(state="disabled")
        else:
            self.sugar_type_combo.config(state="normal")
            self.sugar_type_var.set("white")

    def calculate_price(self, event):
        # Initialise
        size_cost = 0
        # Sizes
        if self.coffee_type_var.get() == "espresso":
            if self.size_var.get() == "single":
                size_cost = ESP_1
            elif self.size_var.get() == "double":
                size_cost = ESP_2
            elif self.size_var.get() == "quadruple":
                size_cost = ESP_4
        elif self.coffee_type_var.get() == "espresso machiatto":
            if self.size_var.get() == "single":
                size_cost = ESP_MAC_1
            elif self.size_var.get() == "double":
                size_cost = ESP_MAC_2
            elif self.size_var.get() == "quadruple":
                size_cost = ESP_MAC_4
        elif self.coffee_type_var.get() == "espresso americano":
            if self.size_var.get() == "single":
                size_cost = ESP_AM_1
            elif self.size_var.get() == "double":
                size_cost = ESP_AM_2
            elif self.size_var.get() == "quadruple":
                size_cost = ESP_AM_4
        elif self.coffee_type_var.get() == "cappuccino":
            if self.size_var.get() == "single":
                size_cost = CAP_1
            elif self.size_var.get() == "double":
                size_cost = CAP_2
            elif self.size_var.get() == "quadruple":
                size_cost = CAP_4
        elif self.coffee_type_var.get() == "cappuccino latte":
            if self.size_var.get() == "single":
                size_cost = CAP_LAT_1
            elif self.size_var.get() == "double":
                size_cost = CAP_LAT_2
            elif self.size_var.get() == "quadruple":
                size_cost = CAP_LAT_4
        elif self.coffee_type_var.get() == "nes":
            if self.size_var.get() == "single":
                size_cost = NES_1
            elif self.size_var.get() == "double":
                size_cost = NES_2
            elif self.size_var.get() == "quadruple":
                size_cost = NES_4
        elif self.coffee_type_var.get() == "frappe":
            if self.size_var.get() == "single":
                size_cost = FRA_1
            elif self.size_var.get() == "double":
                size_cost = FRA_2
            elif self.size_var.get() == "quadruple":
                size_cost = FRA_4

        # Variety
        if self.variety_var.get() == "100% arabica":
            variety_cost = 0.2
        else:
            variety_cost = 0

        # Sugar type
        if self.sugar_type_var.get() == "honey":
            sugar_type_cost = HONEY
        else:
            sugar_type_cost = 0

        # Milk
        if self.milk_var.get() in ["almond", "coconut", "oat"]:
            milk_cost = OTH_MILK
        else:
            milk_cost = 0

        # Extras
        if self.extra_var.get() in ["chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup",
                                    "vanilla syrup"]:
            extra_cost = SYRUP
        else:
            extra_cost = 0

        # If item in offer -> price: 0, disable editing of cost
        new_cost = size_cost + variety_cost + sugar_type_cost + milk_cost + extra_cost
        if not self.offer_type.get() or self.offer_type.get() == "None":
            self.cost_var.set(round(new_cost, 2))
            self.cost_entry.config(state="normal")
        else:
            self.cost_var.set(0.0)
            self.cost_entry.config(state="disabled")


class FreddoFlatFrame(ttk.Frame):
    def __init__(self, master, offer_type):
        super().__init__(master)
        self.offer_type = offer_type

        # Place the frame
        self.pack()

        # Create the variables
        self.define_variables()
        # Create the widgets
        self.create_widgets()
        # Establish layout
        self.create_layout()

        self.coffee_type_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.size_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.variety_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.sugar_type_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.milk_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.extra_combo.bind("<<ComboboxSelected>>", self.calculate_price)

    def define_variables(self):
        self.coffee_type_var = tk.StringVar(value="freddo espresso")
        self.size_var = tk.StringVar(value="regular")
        self.variety_var = tk.StringVar(value="80% arabica + 20% robusta")
        self.sugar_var = tk.StringVar()
        self.sugar_type_var = tk.StringVar()
        self.milk_var = tk.StringVar()
        self.extra_var = tk.StringVar()
        self.cost_var = tk.DoubleVar(value=FRE_ESP_1)

        self.sugar_var.trace_add("write", self.check_sugar)

        self.recipe_dict = {"type": self.coffee_type_var,
                            "size": self.size_var,
                            "variety": self.variety_var,
                            "sugar": self.sugar_var,
                            "sugar_type": self.sugar_type_var,
                            "milk": self.milk_var,
                            "extra": self.extra_var,
                            "cost": self.cost_var}

    def create_widgets(self):
        # Frame header widget
        self.header = ttk.Label(self, text="Item Recipe")

        # "Input coffee type" widget
        self.coffee_type_label = ttk.Label(self, text="Freddo/Flat type: ")
        self.coffee_type_combo = ttk.Combobox(self, textvariable=self.coffee_type_var, values=["freddo espresso",
                                                                                               "freddo cappuccino",
                                                                                               "freddo cappuccino latte",
                                                                                               "flat white cold",
                                                                                               "flat white hot"])

        # "Input size" widget
        self.size_label = ttk.Label(self, text="Size: ")
        self.size_combo = ttk.Combobox(self, textvariable=self.size_var, values=["regular",
                                                                                 "XL"])

        # "Input variety" widget
        self.variety_label = ttk.Label(self, text="Variety: ")
        self.variety_combo = ttk.Combobox(self, textvariable=self.variety_var, values=["80% arabica + 20% robusta",
                                                                                       "100% arabica",
                                                                                       "decaffeine"])

        # "Input sugar" widget
        self.sugar_label = ttk.Label(self, text="Sugar: ")
        self.sugar_combo = ttk.Combobox(self, textvariable=self.sugar_var, values=[None,
                                                                                   "little",
                                                                                   "medium",
                                                                                   "medium-to-sweet",
                                                                                   "sweet",
                                                                                   "very sweet"])

        # "Input sugar type" widget
        self.sugar_type_label = ttk.Label(self, text="Sugar Type: ")
        self.sugar_type_combo = ttk.Combobox(self, textvariable=self.sugar_type_var, values=[None,
                                                                                        "white",
                                                                                        "brown",
                                                                                        "saccharin",
                                                                                        "stevia",
                                                                                        "honey"])

        # "Input milk" widget
        self.milk_label = ttk.Label(self, text="Milk: ")
        self.milk_combo = ttk.Combobox(self, textvariable=self.milk_var, values=[None,
                                                                                 "fresh",
                                                                                 "evapore",
                                                                                 "almond",
                                                                                 "coconut",
                                                                                 "oat"])

        # "Input extra" widget
        self.extra_label = ttk.Label(self, text="Extra: ")
        self.extra_combo = ttk.Combobox(self, textvariable=self.extra_var, values=[None,
                                                                                   "chocolate syrup",
                                                                                   "strawberry syrup",
                                                                                   "caramel syrup",
                                                                                   "hazelnut syrup",
                                                                                   "vanilla syrup",
                                                                                   "cinnamon powder",
                                                                                   "chocolate powder"])

        # "Input cost" widget
        self.cost_label = ttk.Label(self, text="Cost: ")
        self.cost_entry = ttk.Entry(self, textvariable=self.cost_var)

    def create_layout(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        # Frame header position
        self.header.grid(row=0, column=0, columnspan=2)

        # "Input coffee type" widget position
        self.coffee_type_label.grid(row=1, column=0, sticky="e", pady=WIDGET_PAD)
        self.coffee_type_combo.grid(row=1, column=1, pady=WIDGET_PAD)

        # "Input size" widget position
        self.size_label.grid(row=2, column=0, sticky="e", pady=WIDGET_PAD)
        self.size_combo.grid(row=2, column=1, pady=WIDGET_PAD)

        # "Input variety" widget position
        self.variety_label.grid(row=3, column=0, sticky="e", pady=WIDGET_PAD)
        self.variety_combo.grid(row=3, column=1, pady=WIDGET_PAD)

        # "Input sugar" widget position
        self.sugar_label.grid(row=4, column=0, sticky="e", pady=WIDGET_PAD)
        self.sugar_combo.grid(row=4, column=1, pady=WIDGET_PAD)

        # "Input sugar type" widget position
        self.sugar_type_label.grid(row=5, column=0, sticky="e", pady=WIDGET_PAD)
        self.sugar_type_combo.grid(row=5, column=1, pady=WIDGET_PAD)

        # "Input milk" widget position
        self.milk_label.grid(row=6, column=0, sticky="e", pady=WIDGET_PAD)
        self.milk_combo.grid(row=6, column=1, pady=WIDGET_PAD)

        # "Input extra" widget position
        self.extra_label.grid(row=7, column=0, sticky="e", pady=WIDGET_PAD)
        self.extra_combo.grid(row=7, column=1, pady=WIDGET_PAD)

        # "Input cost" widget position
        self.cost_label.grid(row=8, column=0, sticky="e", pady=WIDGET_PAD)
        self.cost_entry.grid(row=8, column=1, sticky="w", pady=WIDGET_PAD)

    # if no sugar is added disable the option to add tips origin
    def check_sugar(self, *args):
        if self.sugar_var.get() == "None":
            self.sugar_type_var.set("None")
            self.sugar_type_combo.config(state="disabled")
        else:
            self.sugar_type_combo.config(state="normal")
            self.sugar_type_var.set("white")

    def calculate_price(self, event):
        # Initialise
        size_cost = 0
        # Sizes
        if self.coffee_type_var.get() == "freddo espresso":
            if self.size_var.get() == "regular":
                size_cost = FRE_ESP_1
            elif self.size_var.get() == "XL":
                size_cost = FRE_ESP_4
        elif self.coffee_type_var.get() == "freddo cappuccino":
            if self.size_var.get() == "regular":
                size_cost = FRE_CAP_1
            elif self.size_var.get() == "XL":
                size_cost = FRE_CAP_4
        elif self.coffee_type_var.get() == "freddo cappuccino latte":
            if self.size_var.get() == "regular":
                size_cost = FRE_CAP_LAT_1
            elif self.size_var.get() == "XL":
                size_cost = FRE_CAP_LAT_4
        elif self.coffee_type_var.get() == "flat white cold":
            if self.size_var.get() == "regular":
                size_cost = FLAT_C_1
            elif self.size_var.get() == "XL":
                size_cost = FLAT_C_4
        elif self.coffee_type_var.get() == "flat white hot":
            if self.size_var.get() == "regular":
                size_cost = FLAT_H_1
            elif self.size_var.get() == "XL":
                size_cost = FLAT_H_4

        # Variety
        if self.variety_var.get() == "100% arabica":
            variety_cost = 0.2
        else:
            variety_cost = 0

        # Sugar type
        if self.sugar_type_var.get() == "honey":
            sugar_type_cost = HONEY
        else:
            sugar_type_cost = 0

        # Milk
        if self.milk_var.get() in ["almond", "coconut", "oat"]:
            milk_cost = OTH_MILK
        else:
            milk_cost = 0

        # Extras
        if self.extra_var.get() in ["chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup",
                                    "vanilla syrup"]:
            extra_cost = SYRUP
        else:
            extra_cost = 0

        # If item in offer -> price: 0, disable editing of cost
        new_cost = size_cost + variety_cost + sugar_type_cost + milk_cost + extra_cost
        if not self.offer_type.get() or self.offer_type.get() == "None":
            self.cost_var.set(round(new_cost, 2))
            self.cost_entry.config(state="normal")
        else:
            self.cost_var.set(0.0)
            self.cost_entry.config(state="disabled")


class FilterFrame(ttk.Frame):
    def __init__(self, master, offer_type):
        super().__init__(master)
        self.offer_type = offer_type

        # Place the frame
        self.pack()

        # Create the variables
        self.define_variables()
        # Create the widgets
        self.create_widgets()
        # Establish layout
        self.create_layout()

        self.coffee_type_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.size_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.sugar_type_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.milk_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.extra_combo.bind("<<ComboboxSelected>>", self.calculate_price)

    def define_variables(self):
        self.coffee_type_var = tk.StringVar()
        self.size_var = tk.StringVar()
        self.sugar_var = tk.StringVar()
        self.sugar_type_var = tk.StringVar()
        self.milk_var = tk.StringVar()
        self.extra_var = tk.StringVar()
        self.cost_var = tk.DoubleVar()

        self.sugar_var.trace_add("write", self.check_sugar)

        self.recipe_dict = {"type": self.coffee_type_var,
                            "size": self.size_var,
                            "sugar": self.sugar_var,
                            "sugar_type": self.sugar_type_var,
                            "milk": self.milk_var,
                            "extra": self.extra_var,
                            "cost": self.cost_var}

    def create_widgets(self):
        # Frame header widget
        self.header = ttk.Label(self, text="Item Recipe")

        # "Input coffee type" widget
        self.coffee_type_label = ttk.Label(self, text="Filter type: ")
        self.coffee_type_combo = ttk.Combobox(self, textvariable=self.coffee_type_var, values=["filter",
                                                                                               "irish coffee",
                                                                                               "ellinikos"])

        # "Input size" widget
        self.size_label = ttk.Label(self, text="Size: ")
        self.size_combo = ttk.Combobox(self, textvariable=self.size_var, values=["single",
                                                                                 "double"])

        # "Input sugar" widget
        self.sugar_label = ttk.Label(self, text="Sugar: ")
        self.sugar_combo = ttk.Combobox(self, textvariable=self.sugar_var, values=[None,
                                                                                   "little",
                                                                                   "medium",
                                                                                   "medium-to-sweet",
                                                                                   "sweet",
                                                                                   "very sweet"])

        # "Input sugar type" widget
        self.sugar_type_label = ttk.Label(self, text="Sugar Type: ")
        self.sugar_type_combo = ttk.Combobox(self, textvariable=self.sugar_type_var, values=[None,
                                                                                        "white",
                                                                                        "brown",
                                                                                        "saccharin",
                                                                                        "stevia",
                                                                                        "honey"])

        # "Input milk" widget
        self.milk_label = ttk.Label(self, text="Milk: ")
        self.milk_combo = ttk.Combobox(self, textvariable=self.milk_var, values=[None,
                                                                                 "fresh",
                                                                                 "evapore",
                                                                                 "almond",
                                                                                 "coconut",
                                                                                 "oat"])

        # "Input extra" widget
        self.extra_label = ttk.Label(self, text="Extra: ")
        self.extra_combo = ttk.Combobox(self, textvariable=self.extra_var, values=[None,
                                                                                   "chocolate syrup",
                                                                                   "strawberry syrup",
                                                                                   "caramel syrup",
                                                                                   "hazelnut syrup",
                                                                                   "vanilla syrup",
                                                                                   "cinnamon powder",
                                                                                   "chocolate powder"])

        # "Input cost" widget
        self.cost_label = ttk.Label(self, text="Cost: ")
        self.cost_entry = ttk.Entry(self, textvariable=self.cost_var)

    def create_layout(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        # Frame header position
        self.header.grid(row=0, column=0, columnspan=2)

        # "Input coffee type" widget position
        self.coffee_type_label.grid(row=1, column=0, sticky="e", pady=WIDGET_PAD)
        self.coffee_type_combo.grid(row=1, column=1, pady=WIDGET_PAD)

        # "Input size" widget position
        self.size_label.grid(row=2, column=0, sticky="e", pady=WIDGET_PAD)
        self.size_combo.grid(row=2, column=1, pady=WIDGET_PAD)

        # "Input sugar" widget position
        self.sugar_label.grid(row=3, column=0, sticky="e", pady=WIDGET_PAD)
        self.sugar_combo.grid(row=3, column=1, pady=WIDGET_PAD)

        # "Input sugar type" widget position
        self.sugar_type_label.grid(row=4, column=0, sticky="e", pady=WIDGET_PAD)
        self.sugar_type_combo.grid(row=4, column=1, pady=WIDGET_PAD)

        # "Input milk" widget position
        self.milk_label.grid(row=5, column=0, sticky="e", pady=WIDGET_PAD)
        self.milk_combo.grid(row=5, column=1, pady=WIDGET_PAD)

        # "Input extra" widget position
        self.extra_label.grid(row=6, column=0, sticky="e", pady=WIDGET_PAD)
        self.extra_combo.grid(row=6, column=1, pady=WIDGET_PAD)

        # "Input cost" widget position
        self.cost_label.grid(row=7, column=0, sticky="e", pady=WIDGET_PAD)
        self.cost_entry.grid(row=7, column=1, sticky="w", pady=WIDGET_PAD)

    # if no sugar is added disable the option to add tips origin
    def check_sugar(self, *args):
        if self.sugar_var.get() == "None":
            self.sugar_type_var.set("None")
            self.sugar_type_combo.config(state="disabled")
        else:
            self.sugar_type_combo.config(state="normal")
            self.sugar_type_var.set("white")

    def calculate_price(self, event):
        # Initialise
        size_cost = 0
        # Sizes
        if self.coffee_type_var.get() == "filter":
            if self.size_var.get() == "single":
                size_cost = FILT_1
            elif self.size_var.get() == "double":
                size_cost = FILT_2
        elif self.coffee_type_var.get() == "irish coffee":
            if self.size_var.get() == "single":
                size_cost = IRIS_1
            elif self.size_var.get() == "double":
                size_cost = IRIS_2
        elif self.coffee_type_var.get() == "ellinikos":
            if self.size_var.get() == "single":
                size_cost = ELL_1
            elif self.size_var.get() == "double":
                size_cost = ELL_2

        # Sugar types
        if self.sugar_type_var.get() == "honey":
            sugar_type_cost = HONEY
        else:
            sugar_type_cost = 0

        # Milk
        if self.milk_var.get() in ["almond", "coconut", "oat"]:
            milk_cost = OTH_MILK
        else:
            milk_cost = 0

        # Extras
        if self.extra_var.get() in ["chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup",
                                    "vanilla syrup"]:
            extra_cost = SYRUP
        else:
            extra_cost = 0

        # If item in offer -> price: 0, disable editing of cost
        new_cost = size_cost + sugar_type_cost + milk_cost + extra_cost
        if not self.offer_type.get() or self.offer_type.get() == "None":
            self.cost_var.set(round(new_cost, 2))
            self.cost_entry.config(state="normal")
        else:
            self.cost_var.set(0.0)
            self.cost_entry.config(state="disabled")


class FoodFrame(ttk.Frame):
    def __init__(self, master, offer_type):
        super().__init__(master)
        self.offer_type = offer_type

        # Place the frame
        self.pack()

        # Create the variables
        self.define_variables()
        # Create the widgets
        self.create_widgets()
        # Establish layout
        self.create_layout()

        self.food_type_combo.bind("<<ComboboxSelected>>", self.calculate_price)

    def define_variables(self):
        self.food_type_var = tk.StringVar()
        self.cost_var = tk.DoubleVar()

        self.recipe_dict = {"type": self.food_type_var,
                            "cost": self.cost_var}

    def create_widgets(self):
        # Frame header widget
        self.header = ttk.Label(self, text="Item Recipe")

        # "Input food type" widget
        self.food_type_label = ttk.Label(self, text="Food type: ")
        self.food_type_combo = ttk.Combobox(self, textvariable=self.food_type_var, values=sorted(["croissant",
                                                                                                  "croissant: turkey, gouda, mayonnaise",
                                                                                                  "croissant: hazelnut cream",
                                                                                                  "croissant: hazelnut cream, banana",
                                                                                                  "croissant: cheese cream, turkey, tomato",
                                                                                                  "bagel: cheese cream, turkey",
                                                                                                  "toast: turkey, cheese",
                                                                                                  "toast: double cheese",
                                                                                                  "sandwich: mediterranean",
                                                                                                  "sandwich: fouantre",
                                                                                                  "sandwich: salmon",
                                                                                                  "sandwich: chicken",
                                                                                                  "sandwich: prosciutto",
                                                                                                  "focacce: prosciutto mozzarella",
                                                                                                  "focacce: mortadella provolone",
                                                                                                  "bar: chocolate, peanutbutter, cranberry, nuts",
                                                                                                  "bar: peanutbutter, biscuit, caramel, bitter",
                                                                                                  "cookie: triple chocolate",
                                                                                                  "cookie: caramel",
                                                                                                  "cookie: red velvet",
                                                                                                  "cookie: peanutbutter",
                                                                                                  "cookie: chocolate chip",
                                                                                                  "cookie: lemon pie",
                                                                                                  "mini donut: chocolate",
                                                                                                  "mini donut: vanilla",
                                                                                                  "yogurt: peanutbutter",
                                                                                                  "yogurt: fruits",
                                                                                                  "yogurt: classic",
                                                                                                  "coffee bag: espresso blend",
                                                                                                  "coffee bag: espresso 100% Arabica"]))

        # "Input cost" widget
        self.cost_label = ttk.Label(self, text="Cost: ")
        self.cost_entry = ttk.Entry(self, textvariable=self.cost_var)

    def create_layout(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2), weight=1)

        # Frame header position
        self.header.grid(row=0, column=0, columnspan=2)

        # "Input food type" widget position
        self.food_type_label.grid(row=1, column=0, sticky="e", pady=WIDGET_PAD)
        self.food_type_combo.grid(row=1, column=1, pady=WIDGET_PAD)

        # "Input cost" widget position
        self.cost_label.grid(row=4, column=0, sticky="e", pady=WIDGET_PAD)
        self.cost_entry.grid(row=4, column=1, sticky="w", pady=WIDGET_PAD)

    def calculate_price(self, event):
        # Cases
        if self.food_type_var.get() in ["bar: chocolate, peanutbutter, cranberry, nuts", "cookie: triple chocolate", "cookie: caramel", "cookie: red velvet", "cookie: peanutbutter", "cookie: chocolate chip"]:
            new_cost = 1.7
        elif self.food_type_var.get() in ["croissant: turkey, gouda, mayonnaise", "croissant: cheese cream, turkey, tomato"]:
            new_cost = 2.9
        elif self.food_type_var.get() in ["bagel: cheese cream, turkey", "bar: peanutbutter, biscuit, caramel, bitter"]:
            new_cost = 2.2
        elif self.food_type_var.get() in ["croissant", "toast: turkey, cheese", "toast: double cheese"]:
            new_cost = 1.8
        elif self.food_type_var.get() in ["focacce: mortadella provolone", "yogurt: fruits"]:
            new_cost = 4.8
        elif self.food_type_var.get() in ["mini donut: chocolate", "mini donut: vanilla"]:
            new_cost = 0.6
        elif self.food_type_var.get() == "cookie: lemon pie":
            new_cost = 1.9
        elif self.food_type_var.get() == "coffee bag: espresso blend":
            new_cost = 8.5
        elif self.food_type_var.get() == "coffee bag: espresso 100% Arabica":
            new_cost = 9.5
        elif self.food_type_var.get() == "croissant: hazelnut cream":
            new_cost = 2.5
        elif self.food_type_var.get() == "croissant: hazelnut cream, banana":
            new_cost = 2.8
        elif self.food_type_var.get() == "focacce: prosciutto mozzarella":
            new_cost = 5.4
        elif self.food_type_var.get() == "sandwich: fouantre":
            new_cost = 3.8
        elif self.food_type_var.get() == "sandwich: mediterranean":
            new_cost = 3.5
        elif self.food_type_var.get() == "sandwich: salmon":
            new_cost = 3.7
        elif self.food_type_var.get() == "sandwich: prosciutto":
            new_cost = 3.9
        elif self.food_type_var.get() == "sandwich: chicken":
            new_cost = 3.1
        elif self.food_type_var.get() == "yogurt: peanutbutter":
            new_cost = 4.6
        elif self.food_type_var.get() == "yogurt: classic":
            new_cost = 4.4

        # If item in offer -> price: 0, disable editing of cost
        if not self.offer_type.get() or self.offer_type.get() == "None":
            self.cost_var.set(round(new_cost, 2))
            self.cost_entry.config(state="normal")
        else:
            self.cost_var.set(0.0)
            self.cost_entry.config(state="disabled")


class BeverageFrame(ttk.Frame):
    def __init__(self, master, offer_type):
        self.offer_type = offer_type

        super().__init__(master)
        # Place the frame
        self.pack()

        # Create the variables
        self.define_variables()
        # Create the widgets
        self.create_widgets()
        # Establish layout
        self.create_layout()

        self.beverage_type_combo.bind("<<ComboboxSelected>>", self.calculate_price)

    def define_variables(self):
        self.beverage_type_var = tk.StringVar()
        self.cost_var = tk.DoubleVar()

        self.recipe_dict = {"type": self.beverage_type_var,
                            "cost": self.cost_var}

    def create_widgets(self):
        # Frame header widget
        self.header = ttk.Label(self, text="Item Recipe")

        # "Input beverage type" widget
        self.beverage_type_label = ttk.Label(self, text="Beverage type: ")
        self.beverage_type_combo = ttk.Combobox(self, textvariable=self.beverage_type_var, values=sorted(["orange juice",
                                                                                                   "mixed juice",
                                                                                                   "special mixed juice",
                                                                                                   "popsicle: strawberry",
                                                                                                   "popsicle: lime",
                                                                                                   "popsicle: raspberry",
                                                                                                   "popsicle: mango",
                                                                                                   "popsicle: pineapple",
                                                                                                   "popsicle: water mellom",
                                                                                                   "arizona: lemon",
                                                                                                   "arizona: honey",
                                                                                                   "arizona: zero sugar",
                                                                                                   "arizona: blueberry",
                                                                                                   "arizona: peach",
                                                                                                   "arizona: pomegranate",
                                                                                                   "coca-cola",
                                                                                                   "fanta: blue",
                                                                                                   "fanta: orange",
                                                                                                   "fanta lemon",
                                                                                                   "schweppes",
                                                                                                   "redbull",
                                                                                                   "water"]))

        # "Input cost" widget
        self.cost_label = ttk.Label(self, text="Cost: ")
        self.cost_entry = ttk.Entry(self, textvariable=self.cost_var)

    def create_layout(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2), weight=1)

        # Frame header position
        self.header.grid(row=0, column=0, columnspan=2)

        # "Input beverage type" widget position
        self.beverage_type_label.grid(row=1, column=0, sticky="e", pady=WIDGET_PAD)
        self.beverage_type_combo.grid(row=1, column=1, pady=WIDGET_PAD)

        # "Input cost" widget position
        self.cost_label.grid(row=4, column=0, sticky="e", pady=WIDGET_PAD)
        self.cost_entry.grid(row=4, column=1, sticky="w", pady=WIDGET_PAD)

    def calculate_price(self, event):
        # Cases
        if self.beverage_type_var.get() in ["popsicle: strawberry", "popsicle: lime", "popsicle: raspberry", "popsicle: mango", "popsicle: pineapple", "popsicle: water mellom", "redbull"]:
            new_cost = 2.5
        elif self.beverage_type_var.get() in ["arizona: lemon", "arizona: honey", "arizona: zero sugar", "arizona: blueberry", "arizona: peach", "arizona: pomegranate", "orange juice"]:
            new_cost = 2.4
        elif self.beverage_type_var.get() in ["coca-cola", "fanta: blue", "fanta: orange", "fanta lemon", "schweppes"]:
            new_cost = 1.5
        elif self.beverage_type_var.get() == "mixed juice":
            new_cost = 3
        elif self.beverage_type_var.get() == "special mixed juice":
            new_cost = 3.5
        elif self.beverage_type_var.get() == "water":
            new_cost = 0.5

        # If item in offer -> price: 0, disable editing of cost
        if not self.offer_type.get() or self.offer_type.get() == "None":
            self.cost_var.set(round(new_cost, 2))
            self.cost_entry.config(state="normal")
        else:
            self.cost_var.set(0.0)
            self.cost_entry.config(state="disabled")


class ChocolateFrame(ttk.Frame):
    def __init__(self, master, offer_type):
        self.offer_type = offer_type

        super().__init__(master)
        # Place the frame
        self.pack()

        # Create the variables
        self.define_variables()
        # Create the widgets
        self.create_widgets()
        # Establish layout
        self.create_layout()

        self.chocolate_type_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.extra_combo.bind("<<ComboboxSelected>>", self.calculate_price)

    def define_variables(self):
        self.chocolate_type_var = tk.StringVar()
        self.temperature_var = tk.StringVar()
        self.extra_var = tk.StringVar()
        self.cost_var = tk.DoubleVar()

        self.recipe_dict = {"type": self.chocolate_type_var,
                            "temperature": self.temperature_var,
                            "extra": self.extra_var,
                            "cost": self.cost_var}

    def create_widgets(self):
        # Frame header widget
        self.header = ttk.Label(self, text="Item Recipe")

        # "Input chocolate type" widget
        self.chocolate_type_label = ttk.Label(self, text="Chocolate type: ")
        self.chocolate_type_combo = ttk.Combobox(self, textvariable=self.chocolate_type_var, values=["chocolate",
                                                                                               "chocolate viennois",
                                                                                               "chocolate white",
                                                                                               "chocolate bitter",
                                                                                               "chocolate orange",
                                                                                               "chocolate hazelnut",
                                                                                               "chocolate ruby",
                                                                                               "chocolate salty caramel"])

        # "Input temperature" widget
        self.temperature_label = ttk.Label(self, text="Temperature: ")
        self.temperature_combo = ttk.Combobox(self, textvariable=self.temperature_var, values=["hot",
                                                                                        "cold"])

        # "Input extra" widget
        self.extra_label = ttk.Label(self, text="Extra: ")
        self.extra_combo = ttk.Combobox(self, textvariable=self.extra_var, values=[None,
                                                                                   "chocolate syrup",
                                                                                   "strawberry syrup",
                                                                                   "caramel syrup",
                                                                                   "hazelnut syrup",
                                                                                   "vanilla syrup"])

        # "Input cost" widget
        self.cost_label = ttk.Label(self, text="Cost: ")
        self.cost_entry = ttk.Entry(self, textvariable=self.cost_var)

    def create_layout(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        # Frame header position
        self.header.grid(row=0, column=0, columnspan=2)

        # "Input chocolate type" widget position
        self.chocolate_type_label.grid(row=1, column=0, sticky="e", pady=WIDGET_PAD)
        self.chocolate_type_combo.grid(row=1, column=1, pady=WIDGET_PAD)

        # "Input temperature" widget position
        self.temperature_label.grid(row=2, column=0, sticky="e", pady=WIDGET_PAD)
        self.temperature_combo.grid(row=2, column=1, pady=WIDGET_PAD)

        # "Input sugar" widget position
        self.extra_label.grid(row=3, column=0, sticky="e", pady=WIDGET_PAD)
        self.extra_combo.grid(row=3, column=1, pady=WIDGET_PAD)

        # "Input cost" widget position
        self.cost_label.grid(row=4, column=0, sticky="e", pady=WIDGET_PAD)
        self.cost_entry.grid(row=4, column=1, sticky="w", pady=WIDGET_PAD)

    def calculate_price(self, event):
        # Cases
        if self.chocolate_type_var.get() == "chocolate":
            chocolate_type_cost = 2.5
        else:
            chocolate_type_cost = 2.6

        if self.extra_var.get() == "None" or self.extra_var.get() == "":
            extra_cost = 0
        else:
            extra_cost = 0.3

        new_cost = chocolate_type_cost + extra_cost
        # If item in offer -> price: 0, disable editing of cost
        if not self.offer_type.get() or self.offer_type.get() == "None":
            self.cost_var.set(round(new_cost, 2))
            self.cost_entry.config(state="normal")
        else:
            self.cost_var.set(0.0)
            self.cost_entry.config(state="disabled")


class ChamomileFrame(ttk.Frame):
    def __init__(self, master, offer_type):
        super().__init__(master)
        self.offer_type = offer_type

        # Place the frame
        self.pack()

        # Create the variables
        self.define_variables()
        # Create the widgets
        self.create_widgets()
        # Establish layout
        self.create_layout()

        self.chamomile_type_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.sugar_type_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.milk_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.extra_combo.bind("<<ComboboxSelected>>", self.calculate_price)

    def define_variables(self):
        self.chamomile_type_var = tk.StringVar()
        self.sugar_var = tk.StringVar()
        self.sugar_type_var = tk.StringVar()
        self.milk_var = tk.StringVar()
        self.extra_var = tk.StringVar()
        self.cost_var = tk.DoubleVar()

        self.sugar_var.trace_add("write", self.check_sugar)

        self.recipe_dict = {"type": self.chamomile_type_var,
                            "sugar": self.sugar_var,
                            "sugar_type": self.sugar_type_var,
                            "milk": self.milk_var,
                            "extra": self.extra_var,
                            "cost": self.cost_var}

    def create_widgets(self):
        # Frame header widget
        self.header = ttk.Label(self, text="Item Recipe")

        # "Input chamomile type" widget
        self.chamomile_type_label = ttk.Label(self, text="Chamomile type: ")
        self.chamomile_type_combo = ttk.Combobox(self, textvariable=self.chamomile_type_var, values=["chamomile"])

        # "Input sugar" widget
        self.sugar_label = ttk.Label(self, text="Sugar: ")
        self.sugar_combo = ttk.Combobox(self, textvariable=self.sugar_var, values=[None,
                                                                                   "little",
                                                                                   "medium",
                                                                                   "medium-to-sweet",
                                                                                   "sweet",
                                                                                   "very sweet"])

        # "Input sugar type" widget
        self.sugar_type_label = ttk.Label(self, text="Sugar Type: ")
        self.sugar_type_combo = ttk.Combobox(self, textvariable=self.sugar_type_var, values=[None,
                                                                                        "white",
                                                                                        "brown",
                                                                                        "saccharin",
                                                                                        "stevia",
                                                                                        "honey"])

        # "Input milk" widget
        self.milk_label = ttk.Label(self, text="Milk: ")
        self.milk_combo = ttk.Combobox(self, textvariable=self.milk_var, values=[None,
                                                                                 "fresh",
                                                                                 "evapore",
                                                                                 "almond",
                                                                                 "coconut",
                                                                                 "oat"])

        # "Input extra" widget
        self.extra_label = ttk.Label(self, text="Extra: ")
        self.extra_combo = ttk.Combobox(self, textvariable=self.extra_var, values=[None,
                                                                                   "chocolate syrup",
                                                                                   "strawberry syrup",
                                                                                   "caramel syrup",
                                                                                   "hazelnut syrup",
                                                                                   "vanilla syrup",
                                                                                   "cinnamon powder",
                                                                                   "chocolate powder"])

        # "Input cost" widget
        self.cost_label = ttk.Label(self, text="Cost: ")
        self.cost_entry = ttk.Entry(self, textvariable=self.cost_var)

    def create_layout(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        # Frame header position
        self.header.grid(row=0, column=0, columnspan=2)

        # "Input chamomile type" widget position
        self.chamomile_type_label.grid(row=1, column=0, sticky="e", pady=WIDGET_PAD)
        self.chamomile_type_combo.grid(row=1, column=1, pady=WIDGET_PAD)

        # "Input sugar" widget position
        self.sugar_label.grid(row=2, column=0, sticky="e", pady=WIDGET_PAD)
        self.sugar_combo.grid(row=2, column=1, pady=WIDGET_PAD)

        # "Input sugar type" widget position
        self.sugar_type_label.grid(row=3, column=0, sticky="e", pady=WIDGET_PAD)
        self.sugar_type_combo.grid(row=3, column=1, pady=WIDGET_PAD)

        # "Input milk" widget position
        self.milk_label.grid(row=4, column=0, sticky="e", pady=WIDGET_PAD)
        self.milk_combo.grid(row=4, column=1, pady=WIDGET_PAD)

        # "Input extra" widget position
        self.extra_label.grid(row=5, column=0, sticky="e", pady=WIDGET_PAD)
        self.extra_combo.grid(row=5, column=1, pady=WIDGET_PAD)

        # "Input cost" widget position
        self.cost_label.grid(row=6, column=0, sticky="e", pady=WIDGET_PAD)
        self.cost_entry.grid(row=6, column=1, sticky="w", pady=WIDGET_PAD)

    # if no sugar is added disable the option to add tips origin
    def check_sugar(self, *args):
        if self.sugar_var.get() == "None":
            self.sugar_type_var.set("None")
            self.sugar_type_combo.config(state="disabled")
        else:
            self.sugar_type_combo.config(state="normal")
            self.sugar_type_var.set("white")

    def calculate_price(self, event):
        # Chamomile type
        if self.chamomile_type_var.get() == "chamomile":
            chamomile_type_cost = CHAMOMILE
        else:
            chamomile_type_cost = 0

        # Sugar type
        if self.sugar_type_var.get() == "honey":
            sugar_type_cost = HONEY
        else:
            sugar_type_cost = 0

        # Milk
        if self.milk_var.get() in ["almond", "coconut", "oat"]:
            milk_cost = OTH_MILK
        else:
            milk_cost = 0

        # Extras
        if self.extra_var.get() in ["chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup",
                                    "vanilla syrup"]:
            extra_cost = SYRUP
        else:
            extra_cost = 0

        # If item in offer -> price: 0, disable editing of cost
        new_cost = chamomile_type_cost + sugar_type_cost + milk_cost + extra_cost
        if not self.offer_type.get() or self.offer_type.get() == "None":
            self.cost_var.set(round(new_cost, 2))
            self.cost_entry.config(state="normal")
        else:
            self.cost_var.set(0.0)
            self.cost_entry.config(state="disabled")


class TeeFrame(ttk.Frame):
    def __init__(self, master, offer_type):
        self.offer_type = offer_type

        super().__init__(master)
        # Place the frame
        self.pack()

        # Create the variables
        self.define_variables()
        # Create the widgets
        self.create_widgets()
        # Establish layout
        self.create_layout()

        self.tee_type_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.sugar_type_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.milk_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.extra_combo.bind("<<ComboboxSelected>>", self.calculate_price)

    def define_variables(self):
        self.tee_type_var = tk.StringVar()
        self.variety_var = tk.StringVar()
        self.sugar_var = tk.StringVar()
        self.sugar_type_var = tk.StringVar()
        self.milk_var = tk.StringVar()
        self.extra_var = tk.StringVar()
        self.cost_var = tk.DoubleVar()

        self.sugar_var.trace_add("write", self.check_sugar)

        self.recipe_dict = {"type": self.tee_type_var,
                            "variety": self.variety_var,
                            "sugar": self.sugar_var,
                            "sugar_type": self.sugar_type_var,
                            "milk": self.milk_var,
                            "extra": self.extra_var,
                            "cost": self.cost_var}

    def create_widgets(self):
        # Frame header widget
        self.header = ttk.Label(self, text="Item Recipe")

        # "Input tee type" widget
        self.tee_type_label = ttk.Label(self, text="Tee type: ")
        self.tee_type_combo = ttk.Combobox(self, textvariable=self.tee_type_var, values=["tee"])

        # "Input variety" widget
        self.variety_label = ttk.Label(self, text="Variety: ")
        self.variety_combo = ttk.Combobox(self, textvariable=self.variety_var, values=["green",
                                                                                       "green with pergamot",
                                                                                       "rooibos",
                                                                                       "moroccan mint",
                                                                                       "black with forest fruits",
                                                                                       "english breakfast",
                                                                                       "apple"])

        # "Input sugar" widget
        self.sugar_label = ttk.Label(self, text="Sugar: ")
        self.sugar_combo = ttk.Combobox(self, textvariable=self.sugar_var, values=[None,
                                                                                   "little",
                                                                                   "medium",
                                                                                   "medium-to-sweet",
                                                                                   "sweet",
                                                                                   "very sweet"])

        # "Input sugar type" widget
        self.sugar_type_label = ttk.Label(self, text="Sugar Type: ")
        self.sugar_type_combo = ttk.Combobox(self, textvariable=self.sugar_type_var, values=[None,
                                                                                        "white",
                                                                                        "brown",
                                                                                        "saccharin",
                                                                                        "stevia",
                                                                                        "honey"])

        # "Input milk" widget
        self.milk_label = ttk.Label(self, text="Milk: ")
        self.milk_combo = ttk.Combobox(self, textvariable=self.milk_var, values=[None,
                                                                                 "fresh",
                                                                                 "evapore",
                                                                                 "almond",
                                                                                 "coconut",
                                                                                 "oat"])

        # "Input extra" widget
        self.extra_label = ttk.Label(self, text="Extra: ")
        self.extra_combo = ttk.Combobox(self, textvariable=self.extra_var, values=[None,
                                                                                   "chocolate syrup",
                                                                                   "strawberry syrup",
                                                                                   "caramel syrup",
                                                                                   "hazelnut syrup",
                                                                                   "vanilla syrup",
                                                                                   "cinnamon powder",
                                                                                   "chocolate powder"])

        # "Input cost" widget
        self.cost_label = ttk.Label(self, text="Cost: ")
        self.cost_entry = ttk.Entry(self, textvariable=self.cost_var)

    def create_layout(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        # Frame header position
        self.header.grid(row=0, column=0, columnspan=2)

        # "Input tee type" widget position
        self.tee_type_label.grid(row=1, column=0, sticky="e", pady=WIDGET_PAD)
        self.tee_type_combo.grid(row=1, column=1, pady=WIDGET_PAD)

        # "Input variety" widget position
        self.variety_label.grid(row=2, column=0, sticky="e", pady=WIDGET_PAD)
        self.variety_combo.grid(row=2, column=1, pady=WIDGET_PAD)

        # "Input sugar" widget position
        self.sugar_label.grid(row=3, column=0, sticky="e", pady=WIDGET_PAD)
        self.sugar_combo.grid(row=3, column=1, pady=WIDGET_PAD)

        # "Input sugar type" widget position
        self.sugar_type_label.grid(row=4, column=0, sticky="e", pady=WIDGET_PAD)
        self.sugar_type_combo.grid(row=4, column=1, pady=WIDGET_PAD)

        # "Input milk" widget position
        self.milk_label.grid(row=5, column=0, sticky="e", pady=WIDGET_PAD)
        self.milk_combo.grid(row=5, column=1, pady=WIDGET_PAD)

        # "Input extra" widget position
        self.extra_label.grid(row=6, column=0, sticky="e", pady=WIDGET_PAD)
        self.extra_combo.grid(row=6, column=1, pady=WIDGET_PAD)

        # "Input cost" widget position
        self.cost_label.grid(row=7, column=0, sticky="e", pady=WIDGET_PAD)
        self.cost_entry.grid(row=7, column=1, sticky="w", pady=WIDGET_PAD)

    # if no sugar is added disable the option to add tips origin
    def check_sugar(self, *args):
        if self.sugar_var.get() == "None":
            self.sugar_type_var.set("None")
            self.sugar_type_combo.config(state="disabled")
        else:
            self.sugar_type_combo.config(state="normal")
            self.sugar_type_var.set("white")

    def calculate_price(self, event):
        # Chamomile type
        if self.tee_type_var.get() == "tee":
            tee_type_cost = TEE
        else:
            tee_type_cost = 0

        # Sugar type
        if self.sugar_type_var.get() == "honey":
            sugar_type_cost = HONEY
        else:
            sugar_type_cost = 0

        # Milk
        if self.milk_var.get() in ["almond", "coconut", "oat"]:
            milk_cost = OTH_MILK
        else:
            milk_cost = 0

        # Extras
        if self.extra_var.get() in ["chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup",
                                    "vanilla syrup"]:
            extra_cost = SYRUP
        else:
            extra_cost = 0

        # If item in offer -> price: 0, disable editing of cost
        new_cost = tee_type_cost + sugar_type_cost + milk_cost + extra_cost
        if not self.offer_type.get() or self.offer_type.get() == "None":
            self.cost_var.set(round(new_cost, 2))
            self.cost_entry.config(state="normal")
        else:
            self.cost_var.set(0.0)
            self.cost_entry.config(state="disabled")


class WeirdChocolateFrame(ttk.Frame):
    def __init__(self, master, offer_type):
        super().__init__(master)
        self.offer_type = offer_type

        # Place the frame
        self.pack()

        # Create the variables
        self.define_variables()
        # Create the widgets
        self.create_widgets()
        # Establish layout
        self.create_layout()

        self.weird_chocolate_type_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.extra_combo.bind("<<ComboboxSelected>>", self.calculate_price)

    def define_variables(self):
        self.weird_chocolate_type_var = tk.StringVar()
        self.extra_var = tk.StringVar()
        self.cost_var = tk.DoubleVar()

        self.recipe_dict = {"type": self.weird_chocolate_type_var,
                            "extra": self.extra_var,
                            "cost": self.cost_var}

    def create_widgets(self):
        # Frame header widget
        self.header = ttk.Label(self, text="Item Recipe")

        # "Input weird chocolate type" widget
        self.weird_chocolate_type_label = ttk.Label(self, text="Weird chocolate type: ")
        self.weird_chocolate_type_combo = ttk.Combobox(self, textvariable=self.weird_chocolate_type_var, values=["freddoccino",
                                                                                                                 "mochaccino"])

        # "Input extra" widget
        self.extra_label = ttk.Label(self, text="Extra: ")
        self.extra_combo = ttk.Combobox(self, textvariable=self.extra_var, values=[None,
                                                                                   "chocolate syrup",
                                                                                   "strawberry syrup",
                                                                                   "caramel syrup",
                                                                                   "hazelnut syrup",
                                                                                   "vanilla syrup"])

        # "Input cost" widget
        self.cost_label = ttk.Label(self, text="Cost: ")
        self.cost_entry = ttk.Entry(self, textvariable=self.cost_var)

    def create_layout(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1)

        # Frame header position
        self.header.grid(row=0, column=0, columnspan=2)

        # "Input weird chocolate type" widget position
        self.weird_chocolate_type_label.grid(row=1, column=0, sticky="e", pady=WIDGET_PAD)
        self.weird_chocolate_type_combo.grid(row=1, column=1, pady=WIDGET_PAD)

        # "Input sugar" widget position
        self.extra_label.grid(row=2, column=0, sticky="e", pady=WIDGET_PAD)
        self.extra_combo.grid(row=2, column=1, pady=WIDGET_PAD)

        # "Input cost" widget position
        self.cost_label.grid(row=3, column=0, sticky="e", pady=WIDGET_PAD)
        self.cost_entry.grid(row=3, column=1, sticky="w", pady=WIDGET_PAD)

    def calculate_price(self, event):
        # Chamomile type
        if self.weird_chocolate_type_var.get() in ["freddoccino", "mochaccino"]:
            tee_type_cost = 2.6
        else:
            tee_type_cost = 0

        # Extras
        if self.extra_var.get() in ["chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup",
                                    "vanilla syrup"]:
            extra_cost = SYRUP
        else:
            extra_cost = 0

        # If item in offer -> price: 0, disable editing of cost
        new_cost = tee_type_cost + extra_cost
        if not self.offer_type.get() or self.offer_type.get() == "None":
            self.cost_var.set(round(new_cost, 2))
            self.cost_entry.config(state="normal")
        else:
            self.cost_var.set(0.0)
            self.cost_entry.config(state="disabled")


class SmoothieFrame(ttk.Frame):
    def __init__(self, master, offer_type):
        super().__init__(master)
        self.offer_type = offer_type

        # Place the frame
        self.pack()

        # Create the variables
        self.define_variables()
        # Create the widgets
        self.create_widgets()
        # Establish layout
        self.create_layout()

        self.smoothie_type_combo.bind("<<ComboboxSelected>>", self.calculate_price)
        self.milk_combo.bind("<<ComboboxSelected>>", self.calculate_price)

    def define_variables(self):
        self.smoothie_type_var = tk.StringVar()
        self.milk_var = tk.StringVar()
        self.cost_var = tk.DoubleVar()

        self.recipe_dict = {"type": self.smoothie_type_var,
                            "milk": self.milk_var,
                            "cost": self.cost_var}

    def create_widgets(self):
        # Frame header widget
        self.header = ttk.Label(self, text="Item Recipe")

        # "Input smoothie type" widget
        self.smoothie_type_label = ttk.Label(self, text="Smoothie type: ")
        self.smoothie_type_combo = ttk.Combobox(self, textvariable=self.smoothie_type_var, values=["smoothie: ergati",
                                                                                                   "smoothie: kiklothimikou",
                                                                                                   "smoothie: popai",
                                                                                                   "smoothie: athliti",
                                                                                                   "smoothie: mogli",
                                                                                                   "smoothie: irakli"])

        # "Input milk" widget
        self.milk_label = ttk.Label(self, text="Milk: ")
        self.milk_combo = ttk.Combobox(self, textvariable=self.milk_var, values=["light",
                                                                                 "fat",
                                                                                 "almond",
                                                                                 "coconut",
                                                                                 "oat"])

        # "Input cost" widget
        self.cost_label = ttk.Label(self, text="Cost: ")
        self.cost_entry = ttk.Entry(self, textvariable=self.cost_var)

    def create_layout(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1)

        # Frame header position
        self.header.grid(row=0, column=0, columnspan=2)

        # "Input smoothie type" widget position
        self.smoothie_type_label.grid(row=1, column=0, sticky="e", pady=WIDGET_PAD)
        self.smoothie_type_combo.grid(row=1, column=1, pady=WIDGET_PAD)

        # "Input milk" widget position
        self.milk_label.grid(row=5, column=0, sticky="e", pady=WIDGET_PAD)
        self.milk_combo.grid(row=5, column=1, pady=WIDGET_PAD)

        # "Input cost" widget position
        self.cost_label.grid(row=7, column=0, sticky="e", pady=WIDGET_PAD)
        self.cost_entry.grid(row=7, column=1, sticky="w", pady=WIDGET_PAD)

    def calculate_price(self, event):
        # Chamomile type
        if self.smoothie_type_var.get() in ["smoothie: ergati", "smoothie: mogli"]:
            smoothie_type_cost = 3.6
        elif self.smoothie_type_var.get() in ["smoothie: kiklothimikou", "smoothie: popai"]:
            smoothie_type_cost = 3.1
        elif self.smoothie_type_var.get() == "smoothie: athliti":
            smoothie_type_cost = 3.4
        elif self.smoothie_type_var.get() == "smoothie: irakli":
            smoothie_type_cost = 3.9

        # Extras
        if self.milk_var.get() in ["almond", "oat", "coconut"]:
            milk_cost = OTH_MILK
        else:
            milk_cost = 0

        # If item in offer -> price: 0, disable editing of cost
        new_cost = smoothie_type_cost + milk_cost
        if not self.offer_type.get() or self.offer_type.get() == "None":
            self.cost_var.set(round(new_cost, 2))
            self.cost_entry.config(state="normal")
        else:
            self.cost_var.set(0.0)
            self.cost_entry.config(state="disabled")


############
# Fifth tab - Order Review
class Tab5Frame(ttk.Frame):
    def __init__(self, master, order_details):
        super().__init__(master)
        self.order_details = order_details

        self.basket = order_details["basket_format"]
        self.order_cost = order_details["order_cost"]
        self.address = order_details["address"]
        self.customer = order_details["customer"]

        self.labels = []

        # Place the frame
        self.pack()
        # Create the widgets
        self.create_widgets()
        # Establish layout
        self.create_layout()

    def create_widgets(self):
        # General info header widget
        self.general_header = ttk.Label(self, text="General Info")

        # Show address
        self.address_label = ttk.Label(self, text=f"Address: {self.address}")

        # Show customer
        self.customer_label = ttk.Label(self, text=f"Customer: {self.customer}")

        # Order cost widgets
        self.order_cost_label = ttk.Label(self, text=f"Order cost: {self.order_cost}")

        # Item header widget
        self.item_header = ttk.Label(self, text="Items")

        # Display all items in the basket
        for item in self.basket:
            label = ttk.Label(self, text=item)
            self.labels.append(label)

    def create_layout(self):
        # General info position
        self.general_header.pack()

        # Address position
        self.address_label.pack()

        # Customer position
        self.customer_label.pack()

        # Order cost position
        self.order_cost_label.pack(pady=10)

        # Item position
        self.item_header.pack()

        for label in self.labels:
            label.pack(fill="x")


app = App("Delivery App", (500, 500))
