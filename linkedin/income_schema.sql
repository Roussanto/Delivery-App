
-- SQL schema for the 'income' database

USE income;

CREATE TABLE IF NOT EXISTS coffees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM("espresso", "espresso machiatto", "espresso americano", "cappuccino", "cappuccino latte", "nes", "frappe") NOT NULL,
    size ENUM("single", "double", "quadruple") NOT NULL,
    variety ENUM("80% arabica + 20% robusta", "100% arabica", "decaffeine") NULL,
    sugar ENUM("little", "medium", "medium-to-sweet", "sweet", "very sweet") NULL,
    sugar_type ENUM("white", "brown", "saccharin", "stevia", "honey") NULL,
    milk ENUM("fresh", "evapore", "almond", "coconut", "oat") NULL,
    extra ENUM("chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup", "vanilla syrup", "cinnamon powder", "chocolate powder") NULL,
    cost DECIMAL(4,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS freddos_flats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM("freddo espresso", "freddo cappuccino", "freddo cappuccino latte", "flat white cold", "flat white hot") NOT NULL,
    size ENUM("regular", "XL") NOT NULL,
    variety ENUM("80% arabica + 20% robusta", "100% arabica", "decaffeine") NOT NULL,
    sugar ENUM("little", "medium", "medium-to-sweet", "sweet", "very sweet") NULL,
    sugar_type ENUM("white", "brown", "saccharin", "stevia", "honey") NULL,
    milk ENUM("fresh", "evapore", "almond", "coconut", "oat") NULL,
    extra ENUM("chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup", "vanilla syrup", "cinnamon powder", "chocolate powder"),
    cost DECIMAL(4,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS filters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM("filter", "irish coffee", "ellinikos") NOT NULL,
    size ENUM("single", "double") NOT NULL,
    sugar ENUM("little", "medium", "medium-to-sweet", "sweet", "very sweet") NULL,
    sugar_type ENUM("white", "brown", "saccharin", "stevia", "honey") NULL,
    milk ENUM("fresh", "evapore", "almond", "coconut", "oat") NULL,
    extra ENUM("chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup", "vanilla syrup", "cinnamon powder", "chocolate powder"),
    cost DECIMAL(4,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS chocolates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM("chocolate", "chocolate viennois", "chocolate white", "chocolate bitter", "chocolate orange", "chocolate hazelnut", "chocolate ruby", "chocolate salty caramel") NOT NULL,
    temperature ENUM("hot", "cold"),
    extra ENUM("chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup", "vanilla syrup"),
    cost DECIMAL(4,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS weird_chocolates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM("freddoccino", "mochaccino") NOT NULL,
    extra ENUM("chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup", "vanilla syrup"),
    cost DECIMAL(4,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS beverages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(40),
    cost DECIMAL(4,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS tees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM("tee") NOT NULL,
    variety ENUM("green", "green with pergamot", "rooibos", "moroccan mint", "black with forest fruits", "english breakfast", "apple") NOT NULL,
    sugar ENUM("little", "medium", "medium-to-sweet", "sweet", "very sweet") NULL,
    sugar_type ENUM("white", "brown", "saccharin", "stevia", "honey") NULL,
    milk ENUM("fresh", "evapore", "almond", "coconut", "oat") NULL,
    extra ENUM("chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup", "vanilla syrup", "cinnamon powder", "chocolate powder"),
    cost DECIMAL(4,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS chamomiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM("chamomile") NOT NULL,
    sugar ENUM("little", "medium", "medium-to-sweet", "sweet", "very sweet") NULL,
    sugar_type ENUM("white", "brown", "saccharin", "stevia", "honey") NULL,
    milk ENUM("fresh", "evapore", "almond", "coconut", "oat") NULL,
    extra ENUM("chocolate syrup", "strawberry syrup", "caramel syrup", "hazelnut syrup", "vanilla syrup", "cinnamon powder", "chocolate powder"),
    cost DECIMAL(4,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS smoothies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM("smoothie: ergati", "smoothie: kiklothimikou", "smoothie: popai", "smoothie: athliti", "smoothie: mogli", "smoothie: irakli") NOT NULL,
    milk ENUM("light", "fat", "almond", "coconut") NOT NULL,
    cost DECIMAL(4,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS foods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(40),
    cost DECIMAL(4,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    latitude DOUBLE,
    longitude DOUBLE
);

CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    address_id INT,
    floor INT NOT NULL,
    FOREIGN KEY(address_id) REFERENCES addresses(id)
);

CREATE TABLE IF NOT EXISTS workdays (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    hours DECIMAL(4,2) NOT NULL,
    payment DECIMAL(4,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    workday_id INT,
    order_time TIME NOT NULL,
    delivery_time TIME,
    tips DECIMAL(4,2) NULL,
    tips_method ENUM("Cash", "Card") NULL,
    source ENUM("Efood", "Wolt", "Box", "Phone") NOT NULL,
    payment_method ENUM("Cash", "Card") NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(workday_id) REFERENCES workdays(id)
);

CREATE TABLE IF NOT EXISTS offers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(64) NOT NULL,
    cost DECIMAL(4,2) NULL
);

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    offer_id INT NULL,
    product_id INT,
    product_type ENUM("coffee", "freddo or flat", "filter", "chocolate", "weird chocolate", "beverage", "tee", "chamomile", "smoothie", "food") NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(offer_id) REFERENCES offers(id)
);

CREATE OR REPLACE VIEW v_orders_summary AS
SELECT 
    o.id AS order_id,
    o.order_time,
    o.delivery_time,
    o.tips,
    o.source,
    o.payment_method,
    c.name AS customer_name,
    a.name AS address_name,
    a.latitude,
    a.longitude
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id
LEFT JOIN addresses a ON c.address_id = a.id;

CREATE INDEX idx_orders_customer_id ON orders(customer_id);
