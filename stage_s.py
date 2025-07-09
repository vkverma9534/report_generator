def run(product_name):
    import pandas as pd
    import matplotlib.pyplot as plt
    import os

    os.makedirs("assets", exist_ok=True)

    stocks_df = pd.read_csv("inventory_sql_clean.csv")
    sales_df = pd.read_csv("sales_sql_clean.csv")
    returns_df = pd.read_csv("returns_sql_clean.csv")

    s = product_name

    # 🔹 Sales plot
    filtered_df = sales_df[sales_df['product_name'] == s].copy()
    filtered_df = filtered_df.reset_index(drop=True)
    n = len(filtered_df)
    if n > 0:
        fractional_index = [i / n for i in range(n)]
        plt.figure(figsize=(8, 4))
        plt.plot(fractional_index, filtered_df['quantity_sold'], marker='o', label="Sales")
        plt.title(f"Sales Trend for Product: {s}")
        plt.xlabel("Timeline")
        plt.ylabel("Quantity Sold")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("assets/sales_trend.png")
        plt.close()
    else:
        return False

    # 🔹 Returns plot
    filtered_df = returns_df[returns_df['product_name'] == s].copy()
    filtered_df = filtered_df.reset_index(drop=True)
    n = len(filtered_df)
    if n > 0:
        fractional_index = [i / n for i in range(n)]
        plt.figure(figsize=(8, 4))
        plt.plot(fractional_index, filtered_df['return_quantity'], marker='o', color='red', label="Returns")
        plt.title(f"Returns Trend for Product: {s}")
        plt.xlabel("Timeline")
        plt.ylabel("Return Quantity")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("assets/returns_trend.png")
        plt.close()

    return True
