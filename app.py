import streamlit as st
import os
import sqlite3

# 🛠 Ensure assets folder exists
os.makedirs("assets", exist_ok=True)

# 🏷️ Page title
st.set_page_config(page_title="📦 Product Insights Generator", layout="wide")
st.title("📦 Product Insights Generator")

st.markdown("Upload your messy CSVs, generate trends, analyze issues, and download a final report.")

# 📤 Upload section
inv_file = st.file_uploader("Upload Inventory CSV", type=["csv"])
sales_file = st.file_uploader("Upload Sales CSV", type=["csv"])
ret_file = st.file_uploader("Upload Returns CSV", type=["csv"])

# ✅ Process files if all uploaded
if inv_file and sales_file and ret_file:
    with open("inventory_raw.csv", "wb") as f:
        f.write(inv_file.getbuffer())
    with open("sales_raw.csv", "wb") as f:
        f.write(sales_file.getbuffer())
    with open("returns_raw.csv", "wb") as f:
        f.write(ret_file.getbuffer())

    st.success("✅ Files uploaded successfully. Starting processing pipeline...")

    # 🚦 Stage 1: Renaming, cleaning, null extraction
    from stage_1 import run as run_stage1
    run_stage1()
    st.success("✅ Stage 1: Cleaning & renaming complete.")

    # 🔄 Stage 2A: Load cleaned CSVs into SQLite
    from stage_2a import run as run_stage2a
    run_stage2a()
    st.success("✅ Stage 2A: Data loaded to SQLite.")

    # 🧠 Stage 2B: SQL logic
    from stage_2b import run as run_stage2b
    run_stage2b()
    st.success("✅ Stage 2B: SQL analysis complete.")

    # 📤 Stage 2C: Export concern rows as CSV
    from stage_2c import run as run_stage2c
    run_stage2c()
    st.success("✅ Stage 2C: Concern data exported.")

    # 🔍 Search feature
    product = st.text_input("🔍 Search for a product name (case-insensitive)")

    if product:
        from stage_s import run as run_stage_s
        found = run_stage_s(product)
        if not found:
            st.warning("⚠️ No data found for this product.")
        else:
            st.image("assets/sales_trend.png", caption="📈 Sales vs Returns Trend", use_column_width=True)
            with open("assets/final_report.pdf", "rb") as f:
                st.download_button("📥 Download PDF Report", f, file_name=f"{product}_report.pdf", mime="application/pdf")

    st.markdown("---")

    # 📊 Category Pie Chart
    if st.button("📊 Show Category Distribution Pie Chart"):
        from stage_3 import run as run_stage3
        run_stage3()
        st.image("assets/category_pie.png", caption="🧩 Product Distribution by Category", use_column_width=True)

else:
    st.info("⬆️ Please upload all three messy CSVs to begin.")
