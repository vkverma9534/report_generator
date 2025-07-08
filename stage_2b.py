import sqlite3

conn = sqlite3.connect("mydb.db")
cur = conn.cursor()

# Drop existing concern tables
cur.executescript("""
DROP TABLE IF EXISTS concern_inventory;
DROP TABLE IF EXISTS concern_sales;
DROP TABLE IF EXISTS concern_returns;

CREATE TABLE concern_inventory AS
SELECT product_name, vendor_id, stock_quantity, upload_date, category
FROM INVENTORY
WHERE (product_name IS NULL OR vendor_id IS NULL)
  AND stock_quantity > 400;

CREATE TABLE concern_sales AS
SELECT product_name, vendor_id, quantity_sold, sale_date, category
FROM SALES
WHERE (product_name IS NULL OR vendor_id IS NULL)
  AND quantity_sold > 600;

CREATE TABLE concern_returns AS
SELECT product_name, vendor_id, return_quantity, return_date, category
FROM RETURNS
WHERE (product_name IS NULL OR vendor_id IS NULL)
  AND return_quantity > 100;

DELETE FROM INVENTORY
WHERE product_name IS NULL OR vendor_id IS NULL OR stock_quantity IS NULL;

DELETE FROM SALES
WHERE product_name IS NULL OR vendor_id IS NULL OR quantity_sold IS NULL;

DELETE FROM RETURNS
WHERE product_name IS NULL OR vendor_id IS NULL OR return_quantity IS NULL;

DROP TABLE IF EXISTS TOP5SOLD;
DROP TABLE IF EXISTS TOP5RETURN;
DROP TABLE IF EXISTS TOP5VENDORS;
DROP TABLE IF EXISTS WORST5VENDORS;
DROP TABLE IF EXISTS TOP5STOCKDEF;

CREATE TABLE TOP5SOLD AS
SELECT 
    product_name,
    SUM(quantity_sold) AS total_quantity_sold
FROM 
    SALES
GROUP BY 
    product_name
ORDER BY 
    total_quantity_sold DESC
LIMIT 5;

CREATE TABLE TOP5RETURN AS
SELECT 
    product_name,
    SUM(return_quantity) AS total_quantity_returned
FROM 
    RETURNS
GROUP BY 
    product_name
ORDER BY 
    total_quantity_returned DESC
LIMIT 5;

CREATE TABLE TOP5VENDORS AS
SELECT 
    vendor_id,
    SUM(quantity_sold) AS total_quantity_sold
FROM 
    SALES
GROUP BY 
    vendor_id
ORDER BY 
    total_quantity_sold DESC
LIMIT 5;

CREATE TABLE WORST5VENDORS AS
SELECT 
    vendor_id,
    SUM(return_quantity) AS total_quantity_returned
FROM 
    RETURNS
GROUP BY 
    vendor_id
ORDER BY 
    total_quantity_returned DESC
LIMIT 5;

CREATE TABLE TOP5STOCKDEF AS
SELECT 
    product_name
FROM 
    INVENTORY
GROUP BY 
    product_name
ORDER BY 
    SUM(stock_quantity) ASC
LIMIT 5;

CREATE TABLE CATEGORIES AS
SELECT 
    category,
    SUM(quantity_sold) AS total_quantity_sold
FROM 
    SALES
GROUP BY 
    category;
""")

conn.commit()
conn.close()
