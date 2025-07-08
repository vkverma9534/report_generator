def run():
    import pandas as pd
    import sqlite3

    stocks_df = pd.read_csv("inventory_clean.csv")
    sales_df = pd.read_csv("sales_clean.csv")
    returns_df = pd.read_csv("returns_clean.csv")

    conn = sqlite3.connect("mydb.db")
    stocks_df.to_sql("INVENTORY", conn, if_exists="replace", index=False)
    conn.close()

    conn = sqlite3.connect("mydb.db")
    sales_df.to_sql("SALES", conn, if_exists="replace", index=False)
    conn.close()

    conn = sqlite3.connect("mydb.db")
    returns_df.to_sql("RETURNS", conn, if_exists="replace", index=False)
    conn.close()
