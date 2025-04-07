import streamlit as st
import pandas as pd

# Mock functions

def normalize_product_name(item_name):
    normalized_products = {
        "pasta sauce": "Classico Tomato & Basil Pasta Sauce 650mL",
        "milk": "2% Reduced Fat Milk 1 Gallon",
        "eggs": "Large Grade A Eggs, 12 count",
        "bread": "Whole Wheat Bread, 1 Loaf",
        "butter": "Unsalted Butter, 1 lb"
    }
    return normalized_products.get(item_name.lower(), item_name.title())

def fetch_mock_price(store, product):
    base_prices = {
        "Classico Tomato & Basil Pasta Sauce 650mL": 3.99,
        "2% Reduced Fat Milk 1 Gallon": 2.79,
        "Large Grade A Eggs, 12 count": 2.49,
        "Whole Wheat Bread, 1 Loaf": 2.99,
        "Unsalted Butter, 1 lb": 3.49
    }
    multiplier = {
        "Walmart": 1.00,
        "Costco": 0.95,
        "Target": 1.05,
        "Whole Foods": 1.20,
        "Trader Joe's": 1.10
    }.get(store, 1.00)
    return round(base_prices.get(product, 4.00) * multiplier, 2)

def get_mock_tax_rate(country, region):
    tax_table = {
        ("USA", "California"): 0.0725,
        ("USA", "New York"): 0.08875,
        ("Canada", "Ontario"): 0.13,
        ("Canada", "Quebec"): 0.14975
    }
    return tax_table.get((country, region), 0.07)

# Streamlit UI
st.set_page_config(page_title="AI Grocery List Generator")
st.title("🛒 AI Grocery List Generator")

stores = ["Walmart", "Costco", "Target", "Whole Foods", "Trader Joe's"]
store = st.selectbox("Choose Grocery Store", stores)

items = st.text_area("Enter grocery items (one per line):")
quantity = st.number_input("Quantity for each item", min_value=1, value=1)

country = st.selectbox("Country", ["USA", "Canada"])
region = st.text_input("State/Province", "California")

if st.button("Generate List"):
    item_list = [i.strip() for i in items.splitlines() if i.strip()]
    tax_rate = get_mock_tax_rate(country, region)

    result_data = []
    subtotal = 0

    for item in item_list:
        normalized = normalize_product_name(item)
        price = fetch_mock_price(store, normalized)
        total_price = price * quantity
        tax_amount = total_price * tax_rate
        final_price = total_price + tax_amount

        result_data.append({
            "Item": normalized,
            "Quantity": quantity,
            "Unit Price": price,
            "Total Price": round(total_price, 2),
            "Tax": round(tax_amount, 2),
            "Final Price": round(final_price, 2)
        })
        subtotal += final_price

    df = pd.DataFrame(result_data)
    st.subheader("🧾 Grocery List")
    st.dataframe(df)

    st.markdown(f"### 🧮 Final Total: **${subtotal:.2f}**")

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv, file_name="grocery_list.csv", mime="text/csv")
