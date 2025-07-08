def run():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import os

    stocks_df = pd.read_csv("inventory_sql_clean.csv")
    sales_df = pd.read_csv("sales_sql_clean.csv")
    returns_df = pd.read_csv("returns_sql_clean.csv")
    categories_df = pd.read_csv("categories.csv")

    s = input("Enter the product name: ")

    filtered_df = sales_df[sales_df['product_name'] == s].copy()
    filtered_df = filtered_df.reset_index(drop=True)

    n = len(filtered_df)
    fractional_index = [i / n for i in range(n)] if n else []

    plt.figure(figsize=(8, 4))
    plt.plot(fractional_index, filtered_df['quantity_sold'], marker='o')
    plt.title(f"Sales for product: {s}")
    plt.xlabel("Normalized Index (i / total)")
    plt.ylabel("Quantity Sold")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("sale_trend.png")

    filtered_df = returns_df[returns_df['product_name'] == s].copy()
    filtered_df = filtered_df.reset_index(drop=True)

    n = len(filtered_df)
    fractional_index = [i / n for i in range(n)] if n else []

    plt.figure(figsize=(8, 4))
    plt.plot(fractional_index, filtered_df['return_quantity'], marker='o')
    plt.title(f"Returns for product: {s}")
    plt.xlabel("Normalized Index (i / total)")
    plt.ylabel("Return Quantity")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("return_trend.png")

    os.makedirs("assets", exist_ok=True)
