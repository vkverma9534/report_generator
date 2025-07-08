def run():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import requests

    stocks_df = pd.read_csv("inventory_real_messy.csv")
    sales_df = pd.read_csv("sales_real_messy.csv")
    returns_df = pd.read_csv("returns_real_messy.csv")

    # Renaming the columns
    column_names_stocks = np.array(stocks_df.columns, dtype=str)
    column_names_sales = np.array(sales_df.columns, dtype=str)
    column_names_returns = np.array(returns_df.columns, dtype=str)

    column_names_sales = np.unique(column_names_sales)
    column_names_stocks = np.unique(column_names_stocks)
    column_names_returns = np.unique(column_names_returns)

    def rename_stocks(column_names_stocks, dictionary_stocks, model="llama3-8b-8192", api_key=None):
        if api_key is None:
            api_key = st.secrets["GROQ_API_KEY"]

        prompt = f"""
You are given a list of messy column names. Your job is to map each of them to at most one matching field from this dictionary:

{', '.join(dictionary_stocks)}

Messy column names:
{column_names_stocks}

Instructions:
- Match each dictionary name to the **best matching column name from the list**.
- Dictionary order must be preserved in output.
- One input per dictionary name. No duplicates.
- Skip dictionary fields if no matching input column is found.
- Format: dictionary_name:input_name
- Output must be strictly space-separated. No punctuation. No explanation. No duplicate targets.
- there might be usage of code intead of id
- try to make sense and be accountable of what you output it might be life saving for many people

Example Output:
product_name:name vendor_id:v_id stock_quantity:available_quantity upload_date:uploadDate category:item_category

Now give only the output:
"""

        try:
            response = requests.post(
                url="https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0,
                    "max_tokens": 100
                }
            )
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()

        except requests.exceptions.RequestException as e:
            st.error(f"🚨 API request failed: {e}")
            return ""

        except ValueError:
            st.error("🚨 Could not parse Groq API response as JSON.")
            st.text("Response content:")
            st.text(response.text)
            return ""

    def rename_sales(column_names_sales, dictionary_sales, model="llama3-8b-8192", api_key=None):
        if api_key is None:
            api_key = st.secrets["GROQ_API_KEY"]

        prompt = f"""
You are given a list of messy column names. Your job is to map each of them to at most one matching field from this dictionary:

{', '.join(dictionary_sales)}

Messy column names:
{column_names_sales}

🧠 Instructions:
- Match each dictionary name to the **best matching column name from the list**.
- Dictionary order must be preserved in output.
- One input per dictionary name. No duplicates.
- Skip dictionary fields if no matching input column is found.
- Format: dictionary_name:input_name
- Output must be strictly space-separated. No punctuation. No explanation. No duplicate targets.
- there might be usage of code intead of id
- try to make sense and be accountable of what you output it might be life saving for many people

✅ Example Output:
product_name:prod_name vendor_id:v_code quantity_sold:sold_qty sale_date:saleDate category:item_category

Now give only the output:
"""

        try:
            response = requests.post(
                url="https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0,
                    "max_tokens": 100
                }
            )
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()

        except requests.exceptions.RequestException as e:
            st.error(f"🚨 API request failed: {e}")
            return ""

        except ValueError:
            st.error("🚨 Could not parse Groq API response as JSON.")
            st.text("Raw response content:")
            st.text(response.text)
            return ""

    def rename_returns(column_names_returns, dictionary_returns, model="llama3-8b-8192", api_key=None):
        if api_key is None:
            api_key = st.secrets["GROQ_API_KEY"]

        prompt = f"""
You are given a list of messy column names. Your job is to map each of them to at most one matching field from this dictionary:

{', '.join(dictionary_returns)}

Messy column names:
{column_names_returns}

🧠 Instructions:
- Match each dictionary name to the **best matching column name from the list**.
- Dictionary order must be preserved in output.
- One input per dictionary name. No duplicates.
- Skip dictionary fields if no matching input column is found.
- Format: dictionary_name:input_name
- Output must be strictly space-separated. No punctuation. No explanation. No duplicate targets.
- there might be usage of code instead of id
- try to make sense and be accountable of what you output it might be life saving for many people

✅ Example Output:
product_name:prod_name vendor_id:v_id return_quantity:qty return_date:date category:item_category

Now give only the output:
"""

        try:
            response = requests.post(
                url="https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0,
                    "max_tokens": 100
                }
            )
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()

        except requests.exceptions.RequestException as e:
            st.error(f"🚨 API request failed: {e}")
            return ""

        except ValueError:
            st.error("🚨 Could not parse Groq API response as JSON.")
            st.text("Raw response content:")
            st.text(response.text)
            return ""

    # Column mapping
    dictionary_stocks = ["product_name", "vendor_id", "stock_quantity", "upload_date", "category"]
    assigned_name_stocks = rename_stocks(column_names_stocks, dictionary_stocks)

    dictionary_sales = ["product_name", "vendor_id", "quantity_sold", "sale_date", "category"]
    assigned_name_sales = rename_sales(column_names_sales, dictionary_sales)

    dictionary_returns = ["product_name", "vendor_id", "return_quantity", "return_date", "category"]
    assigned_name_returns = rename_returns(column_names_returns, dictionary_returns)

    def apply_column_mapping(df, mapping_string):
        part = mapping_string.split(" ", 5)
        old = [None] * 5
        new = [None] * 5
        for i in range(5):
            split_pair = part[i].split(":", 1)
            new[i] = split_pair[0]
            old[i] = split_pair[1] if len(split_pair) > 1 else ""
        df.rename(columns=dict(zip(old, new)), inplace=True)
        df.drop(columns=[c for c in df.columns if c not in new], inplace=True)
        return df, new

    stocks_df, stocks_cols = apply_column_mapping(stocks_df, assigned_name_stocks)
    sales_df, sales_cols = apply_column_mapping(sales_df, assigned_name_sales)
    returns_df, returns_cols = apply_column_mapping(returns_df, assigned_name_returns)

    # Null filtering
    stocks_null_df = stocks_df[stocks_df.isnull().any(axis=1)]
    sales_null_df = sales_df[sales_df.isnull().any(axis=1)]
    returns_null_df = returns_df[returns_df.isnull().any(axis=1)]

    # Sorting
    stocks_df.sort_values(by='upload_date', ascending=True, inplace=True)
    sales_df.sort_values(by='sale_date', ascending=True, inplace=True)
    returns_df.sort_values(by='return_date', ascending=True, inplace=True)
    stocks_null_df.sort_values(by='upload_date', ascending=True, inplace=True)
    sales_null_df.sort_values(by='sale_date', ascending=True, inplace=True)
    returns_null_df.sort_values(by='return_date', ascending=True, inplace=True)

    # Save cleaned & null files
    stocks_df.to_csv('inventory_clean.csv', index=False)
    sales_df.to_csv('sales_clean.csv', index=False)
    returns_df.to_csv('returns_clean.csv', index=False)

    stocks_null_df.to_csv('inventory_null.csv', index=False)
    sales_null_df.to_csv('sales_null.csv', index=False)
    returns_null_df.to_csv('returns_null.csv', index=False)

   
