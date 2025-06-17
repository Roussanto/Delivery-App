import itertools
import pandas as pd

coffee_basket = []
freddo_basket = []
filter_basket = []
chocolate_basket = []
weird_chocolate_basket = []
other_beverage_basket = []
tee_basket = []
chamomile_basket = []
smoothie_basket = []
food_basket = []
offer_basket = []


class Coffees:
    def __init__(self, coffee_type, **kwargs):
        self.coffee_type = coffee_type

        # Get cost of coffee size: changes depending on the coffee object
        self.single_cost = kwargs.get("single", 0)
        self.double_cost = kwargs.get("double", 0)
        self.quadruple_cost = kwargs.get("quadruple", 0)
        self.sizes_catalog = {
            "single": self.single_cost,
            "double": self.double_cost,
            "quadruple": self.quadruple_cost,
        }

        # All the other costs are fixed
        self.env_fee = 0.1
        self.varieties_catalog = {
            "80% arabica + 20% Robusta": 0,
            "100% arabica": 0.2,
            "Decaffeine": 0,
        }
        self.sugars_catalog = {
            None: 0,
            "little": 0,
            "medium": 0,
            "medium-to-sweet": 0,
            "sweet": 0,
            "very sweet": 0,
        }
        self.sugar_types_catalog = {
            "white": 0,
            "brown": 0,
            "saccharin": 0,
            "stevia": 0,
            "honey": 0.3,
        }
        self.milks_catalog = {
            None: 0,
            "fresh": 0,
            "evapore": 0,
            "almond": 0.4,
            "coconut": 0.4,
            "oat": 0.4,
        }
        self.extras_catalog = {
            None: 0,
            "chocolate syrup": 0.3,
            "strawberry syrup": 0.3,
            "caramel syrup": 0.3,
            "hazelnut syrup": 0.3,
            "vanilla syrup": 0.3,
            "cinnamon powder": 0,
            "chocolate powder": 0
        }

        # Get ingredients from the catalogs
        self.sizes = list(self.sizes_catalog.keys())
        self.varieties = list(self.varieties_catalog.keys())
        self.sugars = list(self.sugars_catalog.keys())
        self.sugar_types = list(self.sugar_types_catalog.keys())
        self.milks = list(self.milks_catalog.keys())
        self.extras = list(self.extras_catalog.keys())

        # Collect all costs in a sing catalog: ingredients_catalog
        self.ingredients_catalog = self.sizes_catalog
        self.ingredients_catalog.update(self.varieties_catalog)
        self.ingredients_catalog.update(self.sugars_catalog)
        self.ingredients_catalog.update(self.sugar_types_catalog)
        self.ingredients_catalog.update(self.milks_catalog)
        self.ingredients_catalog.update(self.extras_catalog)
        self.ingredients_catalog.update({"env_fee": self.env_fee})

        # coffee_type is a string. Need to input it inside [] to be regarded as 1 word instead of a char list
        self.coffees = list(
            itertools.product(
                [self.coffee_type], self.sizes, self.varieties, self.sugars, self.sugar_types, self.milks, self.extras
            )
        )

    # Find cost of each coffee.
    # A coffee is a random combination of ingredients.
    # Exclude from the cost computation the string coffe_type
    def add_cost(self):
        menu = []
        for coffee in self.coffees:
            coffee = list(coffee)

            # If the coffee is sugarless there is no point in choosing a type of sugar
            if coffee[3] is None:
                coffee[4] = None

            # If a size does not exist (coffee[1]) then remove the coffee
            size_exist = True
            if (
                (coffee[1] == "single" and self.ingredients_catalog["single"] == 0)
                or (coffee[1] == "double" and self.ingredients_catalog["double"] == 0)
                or (coffee[1] == "quadruple" and self.ingredients_catalog["quadruple"] == 0)
            ):
                size_exist = False

            coffee_cost = sum([self.ingredients_catalog[ingredient] for ingredient in coffee if ingredient != self.coffee_type])

            # Add the cost of coffee and the environmental fee to the list of ingredients to make a coffee product
            coffee.append(coffee_cost + self.env_fee)

            # Do not include duplicates. Duplicates exist because we removed sugar types when the coffee is sugarless

            if coffee not in menu and size_exist:
                menu.append(coffee)

        # menu is local, coffee_basket is the same but global
        coffee_basket.extend(menu)
        return menu

    def __str__(self):
        return f"{list(self.coffees)}"


# Freddos are exactly like Coffees but with different size names
class Freddos:
    def __init__(self, coffee_type, **kwargs):
        self.coffee_type = coffee_type

        # Get cost of coffee size: changes depending on the coffee object
        self.regular_cost = kwargs.get("regular", 0)
        self.XL_cost = kwargs.get("XL", 0)
        self.sizes_catalog = {
            "regular": self.regular_cost,
            "XL": self.XL_cost,
        }

        # All the other costs are fixed
        self.env_fee = 0.1
        self.varieties_catalog = {
            "80% arabica + 20% Robusta": 0,
            "100% arabica": 0.2,
            "Decaffeine": 0,
        }
        self.sugars_catalog = {
            None: 0,
            "little": 0,
            "medium": 0,
            "medium-to-sweet": 0,
            "sweet": 0,
            "very sweet": 0,
        }
        self.sugar_types_catalog = {
            "white": 0,
            "brown": 0,
            "saccharin": 0,
            "stevia": 0,
            "honey": 0.3,
        }
        self.milks_catalog = {
            None: 0,
            "fresh": 0,
            "evapore": 0,
            "almond": 0.4,
            "coconut": 0.4,
            "oat": 0.4,
        }
        self.extras_catalog = {
            None: 0,
            "chocolate syrup": 0.3,
            "strawberry syrup": 0.3,
            "caramel syrup": 0.3,
            "hazelnut syrup": 0.3,
            "vanilla syrup": 0.3,
            "cinnamon powder": 0,
            "chocolate powder": 0
        }

        # Get ingredients from the catalogs
        self.sizes = list(self.sizes_catalog.keys())
        self.varieties = list(self.varieties_catalog.keys())
        self.sugars = list(self.sugars_catalog.keys())
        self.sugar_types = list(self.sugar_types_catalog.keys())
        self.milks = list(self.milks_catalog.keys())
        self.extras = list(self.extras_catalog.keys())

        # Collect all costs in a sing catalog: ingredients_catalog
        self.ingredients_catalog = self.sizes_catalog
        self.ingredients_catalog.update(self.varieties_catalog)
        self.ingredients_catalog.update(self.sugars_catalog)
        self.ingredients_catalog.update(self.sugar_types_catalog)
        self.ingredients_catalog.update(self.milks_catalog)
        self.ingredients_catalog.update(self.extras_catalog)
        self.ingredients_catalog.update({"env_fee": self.env_fee})

        # coffee_type is a string. Need to input it inside [] to be regarded as 1 word instead of a char list
        self.coffees = list(
            itertools.product(
                [self.coffee_type], self.sizes, self.varieties, self.sugars, self.sugar_types, self.milks, self.extras
            )
        )

    # Find cost of each coffee.
    # A coffee is a random combination of ingredients.
    # Exclude from the cost computation the string coffe_type
    def add_cost(self):
        menu = []
        for coffee in self.coffees:
            coffee = list(coffee)

            # If the coffee is sugarless there is no point in choosing a type of sugar
            if coffee[3] is None:
                coffee[4] = None

            # If a size does not exist (coffee[1]) then remove the coffee
            size_exist = True
            if (
                (coffee[1] == "regular" and self.ingredients_catalog["regular"] == 0)
                or (coffee[1] == "XL" and self.ingredients_catalog["XL"] == 0)
            ):
                size_exist = False

            coffee_cost = sum([self.ingredients_catalog[ingredient] for ingredient in coffee if ingredient != self.coffee_type])

            # Add the cost of coffee and the environmental fee to the list of ingredients to make a coffee product
            coffee.append(coffee_cost + self.env_fee)

            # Do not include duplicates. Duplicates exist because we removed sugar types when the coffee is sugarless

            if coffee not in menu and size_exist:
                menu.append(coffee)

        freddo_basket.extend(menu)
        return menu

    def __str__(self):
        return f"{list(self.coffees)}"


# Filters are exactly like Coffees but with no variety
class Filters:
    def __init__(self, coffee_type, single, double=0.0):
        self.coffee_type = coffee_type

        # Get cost of coffee size: changes depending on the coffee object
        self.single_cost = single
        self.double_cost = double
        self.sizes_catalog = {
            "single": self.single_cost,
            "double": self.double_cost
        }

        # All the other costs are fixed
        self.env_fee = 0.1
        self.sugars_catalog = {
            None: 0,
            "little": 0,
            "medium": 0,
            "medium-to-sweet": 0,
            "sweet": 0,
            "very sweet": 0,
        }
        self.sugar_types_catalog = {
            "white": 0,
            "brown": 0,
            "saccharin": 0,
            "stevia": 0,
            "honey": 0.3,
        }
        self.milks_catalog = {
            None: 0,
            "fresh": 0,
            "evapore": 0,
            "almond": 0.4,
            "coconut": 0.4,
            "oat": 0.4,
        }
        self.extras_catalog = {
            None: 0,
            "chocolate syrup": 0.3,
            "strawberry syrup": 0.3,
            "caramel syrup": 0.3,
            "hazelnut syrup": 0.3,
            "vanilla syrup": 0.3,
            "cinnamon powder": 0,
            "chocolate powder": 0
        }

        # Get ingredients from the catalogs
        self.sizes = list(self.sizes_catalog.keys())
        self.sugars = list(self.sugars_catalog.keys())
        self.sugar_types = list(self.sugar_types_catalog.keys())
        self.milks = list(self.milks_catalog.keys())
        self.extras = list(self.extras_catalog.keys())

        # Collect all costs in a single catalog: ingredients_catalog
        self.ingredients_catalog = self.sizes_catalog
        self.ingredients_catalog.update(self.sugars_catalog)
        self.ingredients_catalog.update(self.sugar_types_catalog)
        self.ingredients_catalog.update(self.milks_catalog)
        self.ingredients_catalog.update(self.extras_catalog)
        self.ingredients_catalog.update({"env_fee": self.env_fee})

        # coffee_type is a string. Need to input it inside [] to be regarded as 1 word instead of a char list
        self.coffees = list(
            itertools.product(
                [self.coffee_type], self.sizes, self.sugars, self.sugar_types, self.milks, self.extras
            )
        )

    # Find cost of each coffee.
    # A coffee is a random combination of ingredients.
    # Exclude from the cost computation the string coffe_type
    def add_cost(self):
        menu = []
        for coffee in self.coffees:
            coffee = list(coffee)

            # If the coffee is sugarless there is no point in choosing a type of sugar
            if coffee[3] is None:
                coffee[4] = None

            # If a size does not exist (coffee[1]) then remove the coffee
            size_exist = True
            if coffee[1] == "double" and self.ingredients_catalog["double"] == 0:
                size_exist = False

            coffee_cost = sum([self.ingredients_catalog[ingredient] for ingredient in coffee if ingredient != self.coffee_type])

            # Add the cost of coffee and the environmental fee to the list of ingredients to make a coffee product
            coffee.append(coffee_cost + self.env_fee)

            # Do not include duplicates. Duplicates exist because we removed sugar types when the coffee is sugarless

            if coffee not in menu and size_exist:
                menu.append(coffee)

        filter_basket.extend(menu)
        return menu

    def __str__(self):
        return f"{list(self.coffees)}"


class Chocolates:
    def __init__(self, chocolate_type, cost):
        self.chocolate_type = chocolate_type
        self.cost = cost
        self.temperatures = ["hot", "cold"]

        # Fixed costs
        self.env_fee = 0.1
        self.temperatures_catalog = {
            "hot": 0,
            "cold": 0
        }
        self.extras_catalog = {
            None: 0,
            "chocolate syrup": 0.3,
            "caramel syrup": 0.3,
            "strawberry syrup": 0.3,
            "hazelnut syrup": 0.3,
            "vanilla syrup": 0.3
        }

        # Ingredients
        self.temperatures = list(self.temperatures_catalog.keys())
        self.extras = list(self.extras_catalog.keys())

        # Collect all costs in a single catalog: ingredients_catalog.
        self.ingredients_catalog = self.extras_catalog
        self.ingredients_catalog.update(self.temperatures_catalog)
        self.ingredients_catalog.update({"env_fee": self.env_fee})

        # chocolate_type is a string. Need to input it inside [] to be regarded as 1 word instead of a char list
        self.chocolates = list(
            itertools.product(
                [self.chocolate_type], self.temperatures, self.extras
            )
        )

    def __str__(self):
        return f"{list(self.chocolates)}"

    def add_cost(self):
        menu = []
        for chocolate in self.chocolates:
            chocolate = list(chocolate)
            chocolate_cost = sum([self.ingredients_catalog[ingredient] for ingredient in chocolate if ingredient != self.chocolate_type]) + self.cost

            chocolate.append(chocolate_cost + self.env_fee)

            if chocolate not in menu:
                menu.append(chocolate)

        chocolate_basket.extend(menu)
        return menu


# freddoccinos and mochaccinos do not have temperatures. All other attributes are the same
class WeirdChocolates:
    def __init__(self, chocolate_type, cost):
        self.chocolate_type = chocolate_type
        self.cost = cost

        # Fixed costs
        self.env_fee = 0.1
        self.extras_catalog = {
            None: 0,
            "chocolate syrup": 0.3,
            "caramel syrup": 0.3,
            "strawberry syrup": 0.3,
            "hazelnut syrup": 0.3,
            "vanilla syrup": 0.3
        }

        # Ingredients
        self.extras = list(self.extras_catalog.keys())

        # Collect all costs in a single catalog: ingredients_catalog.
        self.ingredients_catalog = self.extras_catalog
        self.ingredients_catalog.update({"env_fee": self.env_fee})

        # chocolate_type is a string. Need to input it inside [] to be regarded as 1 word instead of a char list
        self.chocolates = list(
            itertools.product(
                [self.chocolate_type], self.extras
            )
        )

    def __str__(self):
        return f"{list(self.chocolates)}"

    def add_cost(self):
        menu = []
        for chocolate in self.chocolates:
            chocolate = list(chocolate)
            chocolate_cost = sum([self.ingredients_catalog[ingredient] for ingredient in chocolate if ingredient != self.chocolate_type])

            chocolate.append(chocolate_cost + self.env_fee + self.cost)

            if chocolate not in menu:
                menu.append(chocolate)

        weird_chocolate_basket.extend(menu)
        return menu


class OtherBeverage:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
        self.env_fee = 0.1

        self.total_cost = self.cost + self.env_fee

    def __str__(self):
        return f"{list(self.name)}"

    def add_cost(self):
        other_beverage_basket.extend([[self.name, self.total_cost]])
        return [self.name, self.total_cost]


class Tees:
    def __init__(self, cost):
        self.cost = cost

        # All the other costs are fixed
        self.env_fee = 0.1
        self.varieties_catalog = {
            "green": 0,
            "green with pergamot": 0,
            "rooibos": 0,
            "moroccan mint": 0,
            "black with forest fruits": 0,
            "english breakfast": 0,
            "apple": 0
        }
        self.sugars_catalog = {
            None: 0,
            "little": 0,
            "medium": 0,
            "medium-to-sweet": 0,
            "sweet": 0,
            "very sweet": 0,
        }
        self.sugar_types_catalog = {
            None: 0,
            "white": 0,
            "brown": 0,
            "saccharin": 0,
            "stevia": 0,
            "honey": 0.3,
        }
        self.milks_catalog = {
            None: 0,
            "fresh": 0,
            "evapore": 0,
            "almond": 0.4,
            "coconut": 0.4,
            "oat": 0.4,
        }
        self.extras_catalog = {
            None: 0,
            "chocolate syrup": 0.3,
            "strawberry syrup": 0.3,
            "caramel syrup": 0.3,
            "hazelnut syrup": 0.3,
            "vanilla syrup": 0.3,
            "cinnamon powder": 0,
            "chocolate powder": 0
        }

        # Get ingredients from the catalogs
        self.varieties = list(self.varieties_catalog.keys())
        self.sugars = list(self.sugars_catalog.keys())
        self.sugar_types = list(self.sugar_types_catalog.keys())
        self.milks = list(self.milks_catalog.keys())
        self.extras = list(self.extras_catalog.keys())

        # Collect all costs in a sing catalog: ingredients_catalog
        self.ingredients_catalog = self.varieties_catalog
        self.ingredients_catalog.update(self.sugars_catalog)
        self.ingredients_catalog.update(self.sugar_types_catalog)
        self.ingredients_catalog.update(self.milks_catalog)
        self.ingredients_catalog.update(self.extras_catalog)
        self.ingredients_catalog.update({"env_fee": self.env_fee})

        # coffee_type is a string. Need to input it inside [] to be regarded as 1 word instead of a char list
        self.tees = list(
            itertools.product(
                ["tee"], self.varieties, self.sugars, self.sugar_types, self.milks, self.extras
            )
        )

    # Find cost of each tee.
    # A coffee is a random combination of ingredients.
    # Exclude from the cost computation the string coffe_type
    def add_cost(self):
        menu = []
        for tee in self.tees:
            tee = list(tee)

            ingredients_cost = sum([self.ingredients_catalog[ingredient] for ingredient in tee if ingredient != "tee"])

            # Add the cost of coffee and the environmental fee to the list of ingredients to make a coffee product
            tee.append(ingredients_cost + self.env_fee + self.cost)

            # Do not include duplicates. Duplicates exist because we removed sugar types when the coffee is sugarless
            if tee not in menu:
                menu.append(tee)

        tee_basket.extend(menu)
        return menu

    def __str__(self):
        return f"{list(self.tees)}"


# Same as Tees but without varieties
class Chamomiles:
    def __init__(self, cost):
        self.cost = cost

        # All the other costs are fixed
        self.env_fee = 0.1
        self.sugars_catalog = {
            None: 0,
            "little": 0,
            "medium": 0,
            "medium-to-sweet": 0,
            "sweet": 0,
            "very sweet": 0,
        }
        self.sugar_types_catalog = {
            None: 0,
            "white": 0,
            "brown": 0,
            "saccharin": 0,
            "stevia": 0,
            "honey": 0.3,
        }
        self.milks_catalog = {
            None: 0,
            "fresh": 0,
            "evapore": 0,
            "almond": 0.4,
            "coconut": 0.4,
            "oat": 0.4,
        }
        self.extras_catalog = {
            None: 0,
            "chocolate syrup": 0.3,
            "strawberry syrup": 0.3,
            "caramel syrup": 0.3,
            "hazelnut syrup": 0.3,
            "vanilla syrup": 0.3,
            "cinnamon powder": 0,
            "chocolate powder": 0
        }

        # Get ingredients from the catalogs
        self.sugars = list(self.sugars_catalog.keys())
        self.sugar_types = list(self.sugar_types_catalog.keys())
        self.milks = list(self.milks_catalog.keys())
        self.extras = list(self.extras_catalog.keys())

        # Collect all costs in a sing catalog: ingredients_catalog
        self.ingredients_catalog = self.sugars_catalog
        self.ingredients_catalog.update(self.sugar_types_catalog)
        self.ingredients_catalog.update(self.milks_catalog)
        self.ingredients_catalog.update(self.extras_catalog)
        self.ingredients_catalog.update({"env_fee": self.env_fee})

        # coffee_type is a string. Need to input it inside [] to be regarded as 1 word instead of a char list
        self.chamomiles = list(
            itertools.product(
                ["chamomile"], self.sugars, self.sugar_types, self.milks, self.extras
            )
        )

    # Find cost of each chamomile.
    # A coffee is a random combination of ingredients.
    # Exclude from the cost computation the string coffe_type
    def add_cost(self):
        menu = []
        for chamomile in self.chamomiles:
            chamomile = list(chamomile)

            ingredients_cost = sum([self.ingredients_catalog[ingredient] for ingredient in chamomile if ingredient != "chamomile"])

            # Add the cost of coffee and the environmental fee to the list of ingredients to make a coffee product
            chamomile.append(ingredients_cost + self.env_fee + self.cost)

            # Do not include duplicates. Duplicates exist because we removed sugar types when the coffee is sugarless
            if chamomile not in menu:
                menu.append(chamomile)

        chamomile_basket.extend(menu)
        return menu

    def __str__(self):
        return f"{list(self.chamomiles)}"


class Smoothies:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

        # Fixed costs
        self.env_fee = 0.1
        self.milks_catalog = {
            "light": 0,
            "fat": 0,
            "almond": 0.4,
            "coconut": 0.4
        }

        # Ingredients
        self.milks = list(self.milks_catalog.keys())

        # Collect all costs in a single catalog: ingredients_catalog.
        self.ingredients_catalog = self.milks_catalog
        self.ingredients_catalog.update({"env_fee": self.env_fee})

        # name is a string. Need to input it inside [] to be regarded as 1 word instead of a char list
        self.smoothies = list(
            itertools.product(
                [self.name], self.milks
            )
        )

    def __str__(self):
        return f"{list(self.smoothies)}"

    def add_cost(self):
        menu = []
        for smoothie in self.smoothies:
            smoothie = list(smoothie)
            chocolate_cost = sum([self.ingredients_catalog[ingredient] for ingredient in smoothie if ingredient != self.name])

            smoothie.append(chocolate_cost + self.env_fee + self.cost)

            if smoothie not in menu:
                menu.append(smoothie)

        smoothie_basket.extend(menu)
        return menu


class Food:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

        self.total_cost = self.cost

    def __str__(self):
        return f"{list(self.name)}"

    def add_cost(self):
        food_basket.extend([[self.name, self.total_cost]])
        return [self.name, self.total_cost]


class Offer:
    def __init__(self, description, cost):
        self.description = description
        self.cost = cost

        self.total_cost = self.cost

    def __str__(self):
        return f"{list(self.description)}"

    def add_cost(self):
        offer_basket.extend([[self.description, self.total_cost]])
        return [self.description, self.total_cost]


# Get combinations
espressos = Coffees("espresso", single=1.7, double=1.9, quadruple=2.9).add_cost()
espressos_macchiato = Coffees("espresso machiatto", single=2, double=2.3).add_cost()
espressos_americano = Coffees("espresso americano", double=1.9, quadruple=2.9).add_cost()
cappuccinos = Coffees("cappuccino", single=2, double=2.3, quadruple=3.3).add_cost()
cappuccinos_latte = Coffees("cappuccino latte", single=2.3, double=3.3).add_cost()
nes = Coffees("nes", single=1.9).add_cost()
frappes = Coffees("frappe", single=1.9).add_cost()

freddos_espresso = Freddos("freddo espresso", regular=2, XL=3).add_cost()
freddos_cappuccino = Freddos("freddo cappuccino", regular=2.3, XL=3.3).add_cost()
freddos_cappuccino_latte = Freddos("freddo cappuccino latte", regular=2.3, XL=3.3).add_cost()
flat_white_colds = Freddos("flat white cold", regular=2.3, XL=3.3).add_cost()
flat_white_hots = Freddos("flat white hot", regular=2.3, XL=3.3).add_cost()

filters = Filters("filter", single=1.9).add_cost()
irish_coffees = Filters("irish coffee", single=3.2).add_cost()
ellinikos = Filters("ellinikos", single=1.4, double=1.6).add_cost()

chocolates = Chocolates("chocolate", 2.5).add_cost()
chocolates_viennois = Chocolates("chocolate viennois", 2.8).add_cost()
chocolates_white = Chocolates("chocolate white", 2.6).add_cost()
chocolates_bitter = Chocolates("chocolate bitter", 2.6).add_cost()
chocolates_orange = Chocolates("chocolate orange", 2.6).add_cost()
chocolates_hazelnut = Chocolates("chocolate hazelnut", 2.6).add_cost()
chocolates_ruby = Chocolates("chocolate ruby", 2.6).add_cost()
chocolates_salty_caramel = Chocolates("chocolate salty caramel", 2.6).add_cost()
freddoccinos = WeirdChocolates("freddoccino", 2.6).add_cost()
mochaccinos = WeirdChocolates("mochaccino", 2.6).add_cost()

fresh_orange_juice = OtherBeverage("fresh orange juice", 2.4).add_cost()
fresh_mixed_juice = OtherBeverage("fresh mixed juice", 3).add_cost()
special_fresh_mixed_juice = OtherBeverage("special fresh mixed juice", 3.5).add_cost()
strawberry_popsicle = OtherBeverage("strawberry popsicle", 2.5).add_cost()
lime_popsicle = OtherBeverage("lime popsicle", 2.5).add_cost()
raspberry_popsicle = OtherBeverage("raspberry popsicle", 2.5).add_cost()
mango_popsicle = OtherBeverage("mango popsicle", 2.5).add_cost()
pineapple_popsicle = OtherBeverage("pineapple popsicle", 2.5).add_cost()
watermelon_popsicle = OtherBeverage("watermelon popsicle", 2.5).add_cost()
arabica_bag = OtherBeverage("arabica bag", 9.5).add_cost()
blend_bag = OtherBeverage("blend bag", 8.5).add_cost()
arizona_lemon = OtherBeverage("arizona lemon", 2.4).add_cost()
arizona_peach = OtherBeverage("arizona peach", 2.4).add_cost()
arizona_diet = OtherBeverage("arizona diet", 2.4).add_cost()
arizona_ginseng = OtherBeverage("arizona ginseng", 2.4).add_cost()
arizona_pomegranate = OtherBeverage("arizona pomegranate", 2.4).add_cost()
arizona_blueberry = OtherBeverage("arizona blueberry", 2.4).add_cost()
coca_cola = OtherBeverage("coca cola", 1.5).add_cost()
fanta_red = OtherBeverage("fanta red", 1.5).add_cost()
fanta_blue = OtherBeverage("fanta blue", 1.5).add_cost()
fanta_lemon = OtherBeverage("fanta lemon", 1.5).add_cost()
schweppes = OtherBeverage("schweppes", 1.5).add_cost()
red_bull = OtherBeverage("red bull", 2.5).add_cost()
water = OtherBeverage("water", 0.5).add_cost()

tees = Tees(1.7).add_cost()

chamomiles = Chamomiles(1.7).add_cost()

ergati_smoothies = Smoothies("ergati smoothie", 3.6).add_cost()
kiklothimikou_smoothies = Smoothies("kiklothimikou smoothie", 3.1).add_cost()
popai_smoothies = Smoothies("popai smoothie", 3.1).add_cost()
athliti_smoothies = Smoothies("athliti smoothie", 3.4).add_cost()
mogli_smoothies = Smoothies("mogli smoothie", 3.6).add_cost()
irakli_smoothies = Smoothies("irakli smoothie", 3.9).add_cost()

butter_croissant = Food("butter croissant", 1.8).add_cost()
turkey_cheese_tomato_croissant = Food("turkey cheese tomato croissant", 2.9).add_cost()
turkey_gouda_mayonnaise_croissant = Food("turkey gouda mayonnaise croissant", 2.9).add_cost()
butter_hazelnut_croissant = Food("butter hazelnut croissant", 2.5).add_cost()
butter_hazelnut_banana_croissant = Food("butter hazelnut banana croissant", 2.8).add_cost()
turkey_bagel = Food("turkey bagel", 2.2).add_cost()
toast = Food("toast", 1.8).add_cost()
double_cheese_toast = Food("double cheese toast", 1.8).add_cost()
chicken_sandwich = Food("chicken sandwich", 3.1).add_cost()
mozzarella_sandwich = Food("mozzarella sandwich", 2.9).add_cost()
salmon_sandwich = Food("salmon sandwich", 3.2).add_cost()
crete_sandwich = Food("crete sandwich", 3.3).add_cost()
turkey_sandwich = Food("turkey sandwich", 3).add_cost()
cereal_bar = Food("cereal bar", 1.7).add_cost()
protein_bitter_bar = Food("protein bitter bar", 2.2).add_cost()
protein_white_bar = Food("protein white bar", 2.2).add_cost()
red_velvet_cookie = Food("red velvet cookie", 1.7).add_cost()
triple_chocolate_cookie = Food("triple chocolate cookie", 1.7).add_cost()
caramel_cookie = Food("caramel cookie", 1.7).add_cost()
chocolate_chip_cookie = Food("caramel chip cookie", 1.7).add_cost()
peanut_butter_cookie = Food("peanut butter cookie", 1.7).add_cost()
lemon_pie_cookie = Food("lemon pie cookie", 1.7).add_cost()
bounty_cookie = Food("bounty cookie", 1.7).add_cost()
cheesecake_strawberry_cookie = Food("cheesecake strawberry cookie", 1.9).add_cost()
cranberry_almond_cookie = Food("cranberry almond cookie", 1.7).add_cost()
bavaria_donut = Food("bavaria donut", 0.6).add_cost()
chocolate_donut = Food("chocolate donut", 0.6).add_cost()

coffee_toast_orange_juice = Offer("1 coffee, 1 toast, 1 fresh orange juice", 5.5).add_cost()
coffee_cookie_water = Offer("1 coffee, 1 soft cookie, 1 water", 4).add_cost()

# Create dataframes
coffees_df = pd.DataFrame(coffee_basket, columns=["coffee_type", "size", "variety", "sugar", "sugar_type", "milk", "extra", "cost"])
freddos_df = pd.DataFrame(freddo_basket, columns=["coffee_type", "size", "variety", "sugar", "sugar_type", "milk", "extra", "cost"])
filters_df = pd.DataFrame(filter_basket, columns=["coffee_type", "size", "sugar", "sugar_type", "milk", "extra", "cost"])
chocolates_df = pd.DataFrame(chocolate_basket, columns=["chocolate_type", "temperature", "extra", "cost"])
weird_chocolates_df = pd.DataFrame(weird_chocolate_basket, columns=["chocolate_type", "extra", "cost"])
other_beverages_df = pd.DataFrame(other_beverage_basket, columns=["name", "cost"])
tees_df = pd.DataFrame(tee_basket, columns=["tee_type", "variety", "sugar", "sugar_type", "milk", "extra", "cost"])
chamomiles_df = pd.DataFrame(chamomile_basket, columns=["chamomile_type", "sugar", "sugar_type", "milk", "extra", "cost"])
smoothies_df = pd.DataFrame(smoothie_basket, columns=["name", "milk", "cost"])
foods_df = pd.DataFrame(food_basket, columns=["name", "cost"])
offers_df = pd.DataFrame(offer_basket, columns=["description", "cost"])

coffees_df.to_csv("data/coffees.csv", index=False)
freddos_df.to_csv("data/freddos.csv", index=False)
filters_df.to_csv("data/filters.csv", index=False)
chocolates_df.to_csv("data/chocolates.csv", index=False)
weird_chocolates_df.to_csv("data/weird_chocolates.csv", index=False)
other_beverages_df.to_csv("data/other beverages.csv", index=False)
tees_df.to_csv("data/tees.csv", index=False)
chamomiles_df.to_csv("data/chamomiles.csv", index=False)
smoothies_df.to_csv("data/smoothies.csv", index=False)
foods_df.to_csv("data/foods.csv", index=False)
offers_df.to_csv("data/offers.csv", index=False)
