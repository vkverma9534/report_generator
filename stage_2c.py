import pandas as pd



conn = sqlite3.connect("mydb.db")

df = pd.read_sql_query("SELECT * FROM INVENTORY", conn)
df.to_csv("inventory_sql_clean.csv", index=False)

df = pd.read_sql_query("SELECT * FROM SALES", conn)
df.to_csv("sales_sql_clean.csv", index=False)

df = pd.read_sql_query("SELECT * FROM RETURNS", conn)
df.to_csv("returns_sql_clean.csv", index=False)

df = pd.read_sql_query("SELECT * FROM concern_inventory", conn)
df.to_csv("concern_inventory.csv", index=False)

df = pd.read_sql_query("SELECT * FROM concern_sales", conn)
df.to_csv("concern_sales.csv", index=False)

df = pd.read_sql_query("SELECT * FROM concern_returns", conn)
df.to_csv("concern_returns.csv", index=False)

df = pd.read_sql_query("SELECT * FROM TOP5SOLD", conn)
df.to_csv("top5sold.csv", index=False)

df = pd.read_sql_query("SELECT * FROM TOP5RETURN", conn)
df.to_csv("top5return.csv", index=False)

df = pd.read_sql_query("SELECT * FROM TOP5VENDORS", conn)
df.to_csv("top5vendors.csv", index=False)

df = pd.read_sql_query("SELECT * FROM WORST5VENDORS", conn)
df.to_csv("worst5vendors.csv", index=False)

df = pd.read_sql_query("SELECT * FROM TOP5STOCKDEF", conn)
df.to_csv("top5stockdef.csv", index=False)

df = pd.read_sql_query("SELECT * FROM CATEGORIES", conn)
df.to_csv("categories.csv", index=False)

conn.close()
