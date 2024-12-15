import streamlit as st
from datetime import datetime

def calculate_interest(start_date, end_date, amount, interest_rate):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    months_diff = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

    full_months_interest = amount * (interest_rate / 100) * months_diff

    start_of_last_month = start_date.replace(year=end_date.year, month=end_date.month)
    remaining_days = (end_date - start_of_last_month).days+months_diff

    amount_per_month = amount * (interest_rate / 100)
    partial_month_interest = amount_per_month * (remaining_days/ 30)

    total_interest = round(full_months_interest + partial_month_interest, 2)
    
    return months_diff, full_months_interest, remaining_days, total_interest

# Streamlit App
st.set_page_config(page_title="Finance Calculator", page_icon="\U0001F4B0", layout="centered")

# Header Section
st.markdown(
    """
    <style>
        .main-header {
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            color: #FFD700;
            font-family: 'Arial', sans-serif;
        }
        .sub-header {
            font-size: 20px;
            text-align: center;
            color: #555;
            margin-bottom: 40px;
        }
        .stApp {
            background-color: #FFF8DC;
        }
    </style>
    <div class="main-header">Finance Calculator</div>
    <div class="sub-header">Calculate your gold business interest with ease</div>
    """,
    unsafe_allow_html=True
)

# Input Section
st.sidebar.header("Enter Details")

start_date = st.sidebar.date_input("Start Date", value=datetime(2024, 1, 1))
end_date = st.sidebar.date_input("End Date", value=datetime(2024, 12, 31))
amount = st.sidebar.number_input("Principal Amount (₹)", value=20000, min_value=0, step=1000)
interest_rate = st.sidebar.number_input("Monthly Interest Rate (%)", value=1.75, min_value=0.0, step=0.01)

# Calculate Button
if st.sidebar.button("Calculate Interest"):
    if start_date >= end_date:
        st.error("Start Date must be before End Date.")
    else:
        months_diff, full_months_interest, remaining_days, total_interest = calculate_interest(
            start_date.strftime('%Y-%m-%d'), 
            end_date.strftime('%Y-%m-%d'), 
            amount, 
            interest_rate
        )
        # Display results
        st.markdown(
            f"""
            <div style="text-align: center; margin-top: 30px;">
                <h2 style="color: #008000;">Calculation Results</h2>
                <p style="font-size: 20px;">Number of Months: <strong style="color: #FF4500;">{months_diff}</strong></p>
                <p style="font-size: 20px;">Interest for Full Months: <strong style="color: #FF4500;">₹{full_months_interest:.2f}</strong></p>
                <p style="font-size: 20px;">Remaining Days: <strong style="color: #FF4500;">{remaining_days}</strong></p>
                <p style="font-size: 20px;">Total Interest: <strong style="color: #FF4500;">₹{total_interest}</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("Enter your details and click 'Calculate Interest' to see the results.")

# Footer
st.markdown(
    """
    <hr style="border: 1px solid #FFD700;">
    <p style="text-align: center; font-size: 14px; color: #888;">&copy; 2024 Gold Business Finance Calculator</p>
    """,
    unsafe_allow_html=True
)
