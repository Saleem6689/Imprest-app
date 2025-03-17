import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Custom CSS for white background and maroon text
st.markdown(
    """
    <style>
    /* Set background color to white */
    body {
        background-color: white;
    }
    /* Set text color to maroon */
    .stApp, .stMarkdown, .stTextInput, .stNumberInput, .stDateInput, .stSelectbox, .stButton, .stDataFrame {
        color: maroon !important;
    }
    /* Center the title */
    .title {
        text-align: center;
        font-size: 60px !important;
        font-weight: bold;
        color: maroon !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add the logo to the upper-right corner using st.image
logo_url = "https://github.com/Saleem6689/Imprest-app/blob/main/tiet_logo.png?raw=true"

# Use columns to position the logo in the upper-right corner
col1, col2 = st.columns([1, 1])  # Create two columns
with col2:
    st.image(logo_url, width=400, use_container_width=False, output_format="PNG")

# Centered title
st.markdown('<p class="title">Imprest Account</p>', unsafe_allow_html=True)

# Rest of your app code...
st.title("MED, TIET, Patiala")
st.header("Bill & Adv. Entry")

# Input fields and other functionality...
initial_cash = st.number_input("Initial Cash in Hand*", min_value=0, value=0)
date = st.date_input("Date", value=datetime.today())
name = st.text_input("Name*")
lab = st.text_input("Lab")
approval = st.selectbox("Approval", ["Approved", "Pending", "Not Required"])
advance_given = st.number_input("Advance Given", min_value=0, value=0)
bill_number = st.text_input("Bill Number*")
bill_amount = st.number_input("Bill Amount*", min_value=0, value=0)
travel_allowance = st.number_input("Travel Allowance")
payment_return_from_person = st.number_input("Payment Return From Person", min_value=0, value=0)
payment_return_to_person = st.number_input("Payment Return To Person", min_value=0, value=0)
remark = st.text_input("Supplier Name & Items")

# Calculate totals
if bill_amount and advance_given and travel_allowance:
    total_cash = bill_amount + travel_allowance
    bill_balance_pending = advance_given - total_cash
    final_settlement = bill_amount - advance_given + travel_allowance
    cash_in_hand = initial_cash - total_cash
else:
    bill_balance_pending = 0
    final_settlement = 0
    total_cash = 0
    cash_in_hand = initial_cash

# Display calculated fields
st.write(f"**Bill/Balance/Pending Payment:** {bill_balance_pending}")
st.write(f"**Final Settlement:** {final_settlement}")
st.write(f"**Total Cash (Bill Amount + Travel Allowance):** {total_cash}")
st.write(f"**Cash in Hand (Initial Cash in Hand - Total Cash):** {cash_in_hand}")

# Save button
if st.button("Save"):
    data = {
        "Date": date,
        "Name": name,
        "Lab": lab,
        "Initial Cash in Hand": initial_cash,
        "Approval": approval,
        "Advance Given": advance_given,
        "Bill Number": bill_number,
        "Bill Amount": bill_amount,
        "Travel Allowance": travel_allowance,
        "Total Cash": total_cash,
        "Bill/Balance/Pending Payment": bill_balance_pending,
        "Final Settlement": final_settlement,
        "Payment Return From Person": payment_return_from_person,
        "Payment Return To Person": payment_return_to_person,
        "Cash in Hand": cash_in_hand,
        "Remarks": remark,
    }
    
    # Validate inputs
    if validate_inputs(data):
        # Calculate totals
        data = calculate_totals(data)
        # Save data
        save_data(data)

# Reset button
if st.button("Reset Saved Data"):
    reset_data()

# Display existing data
if os.path.exists("data.xlsx"):
    st.header("Saved Data")
    df = pd.read_excel("data.xlsx")
    st.dataframe(df)
else:
    st.info("No data saved yet.")
