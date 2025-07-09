def run():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt


    stocks_df = pd.read_csv("inventory_sql_clean.csv")
    sales_df=pd.read_csv("sales_sql_clean.csv")
    returns_df=pd.read_csv("returns_sql_clean.csv")
    categories_df=pd.read_csv("categories.csv")


    categories_df = categories_df.sort_values('total_quantity_sold', ascending=False).reset_index(drop=True)


    top_n = 8
    top_df = categories_df.iloc[:top_n].copy()
    others_sales = categories_df.iloc[top_n:]['total_quantity_sold'].sum()


    others_row = pd.DataFrame({
        'category': ['Others'],
        'total_quantity_sold': [others_sales]
    })
    df_combined = pd.concat([top_df, others_row], ignore_index=True)


    df_combined['sales_pct'] = df_combined['total_quantity_sold'] / df_combined['total_quantity_sold'].sum() * 100


    plt.figure(figsize=(6, 6))
    plt.pie(
        df_combined['sales_pct'],
        labels=df_combined['category'],
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Paired.colors  
    )
    plt.title('Sales Distribution')
    plt.axis('equal')  
    plt.savefig("assets/category_div.png")
    plt.close()
