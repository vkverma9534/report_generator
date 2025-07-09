import streamlit as st
import os
import sqlite3
from fpdf import FPDF
import pandas as pd

# Ensure assets folder exists
os.makedirs("assets", exist_ok=True)

# Page setup
st.set_page_config(page_title="Product Insights Generator", layout="wide")
st.title("Product Insights Generator")
st.markdown("Upload your messy CSVs, generate trends, analyze issues, and download a final report.")
st.markdown("Instructions of uploads:-")
st.markdown("- This is report generator site and this requires some columns to be mandatorily be present.")
st.markdown("   for it's proper functioning.")
st.markdown("-> Inventory - 'product name','Vendor ID','stock quantity','upload date','category of product'.")
st.markdown("-> Sales - 'product name','Vendor ID','quantity sold','sell date','category of product'.")
st.markdown("-> Returns - 'product name','Vendor ID','return quantity','return date','category of product'.")
st.markdown("-> NOTE   -  You do not need to worry about order and name of columns as our AI powered tool will apprehend it")
st.markdown("             just keep the name easy to understand.")


# Upload section
inv_file = st.file_uploader("Upload Inventory CSV", type=["csv"])
sales_file = st.file_uploader("Upload Sales CSV", type=["csv"])
ret_file = st.file_uploader("Upload Returns CSV", type=["csv"])

def generate_pdf_report():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    # Add pie chart first
    pie_path = os.path.join("assets", "category_div.png")
    if os.path.exists(pie_path):
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Category Pie Chart", ln=True)
        pdf.image(pie_path, w=160)

    # Merge all CSVs in order
    tables = [
        ("Top 5 Sold Products", "top5sold.csv"),
        ("Top 5 Returned Products", "top5return.csv"),
        ("Top 5 Vendors", "top5vendors.csv"),
        ("Worst 5 Vendors", "worst5vendors.csv"),
        ("Top 5 Stock Deficiency", "top5stockdef.csv"),
        ("Category-wise Sales", "categories.csv"),
        ("Concern Inventory Rows", "concern_inventory.csv"),
        ("Concern Sales Rows", "concern_sales.csv"),
        ("Concern Return Rows", "concern_returns.csv"),
        ("Inventory Null Rows", "inventory_null.csv"),
        ("Sales Null Rows", "sales_null.csv"),
        ("Returns Null Rows", "returns_null.csv")
    ]

    pdf.set_font("Arial", "", 10)
    for title, csv_file in tables:
        if os.path.exists(csv_file):
            try:
                df = pd.read_csv(csv_file)
                pdf.ln(5)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, title, ln=True)
                pdf.set_font("Arial", "", 9)
                for _, row in df.iterrows():
                    row_str = " | ".join(str(x) for x in row.tolist())
                    pdf.multi_cell(0, 7, row_str)
            except Exception:
                continue

    pdf.output("assets/final_report.pdf")

if inv_file and sales_file and ret_file:
    with open("inventory_real_messy.csv", "wb") as f:
        f.write(inv_file.getbuffer())
    with open("sales_real_messy.csv", "wb") as f:
        f.write(sales_file.getbuffer())
    with open("returns_real_messy.csv", "wb") as f:
        f.write(ret_file.getbuffer())

    st.success("Files uploaded successfully. Starting processing pipeline...")

    from stage_1 import run as run_stage1
    run_stage1()
    st.success("Stage 1: Cleaning & renaming complete.")

    from stage_2a import run as run_stage2a
    run_stage2a()
    st.success("Stage 2A: Data loaded to SQLite.")

    from stage_2b import run as run_stage2b
    run_stage2b()
    st.success("Stage 2B: SQL analysis complete.")

    from stage_2c import run as run_stage2c
    run_stage2c()
    st.success("Stage 2C: Concern data exported.")

    from stage_3 import run as run_stage3
    run_stage3()

    generate_pdf_report()
    st.success("PDF report generated.")

    with open("assets/final_report.pdf", "rb") as f:
        st.download_button("Download Final PDF Report", f, file_name="Product_Report.pdf", mime="application/pdf")

# 🔍 Search Bar (Always visible)
product = st.text_input("Search for a product name (case-insensitive)")

if product:
    from stage_s import run as run_stage_s
    found = run_stage_s(product)
    if not found:
        st.warning("No data found for this product.")
    else:
        st.image("assets/sales_trend.png", caption="Sales Trend", use_column_width=True)
        st.image("assets/returns_trend.png", caption="Returns Trend", use_column_width=True)
