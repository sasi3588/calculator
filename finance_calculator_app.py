import streamlit as st
from datetime import datetime

def calculate_interest(start_date, end_date, amount, interest_rate):
    start_date = datetime.strptime(start_date, "%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%d/%m/%Y")

    months_diff = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

    start_of_last_month = start_date.replace(year=end_date.year, month=end_date.month)
    remaining_days = (end_date - start_of_last_month).days + months_diff
    if remaining_days >= 30:
        months_diff += 1
        remaining_days -= 30
    full_months_interest = round(amount * (interest_rate / 100) * months_diff, 2)
    remaining_days += 1
    amount_per_month = amount * (interest_rate / 100)
    partial_month_interest = round(amount_per_month * (remaining_days / 30), 2)

    total_interest = round(full_months_interest + partial_month_interest, 2)

    return months_diff, full_months_interest, remaining_days, partial_month_interest, total_interest


# Initialize session state for theme
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

# Theme toggle button
if st.sidebar.button("Toggle Dark Mode"):
    st.session_state["dark_mode"] = not st.session_state["dark_mode"]

# Apply dynamic theme
if st.session_state["dark_mode"]:
    background_color = "#121212"
    text_color = "#FFFFFF"
    result_color = "#FFD700"
    input_bg_color = "#333333"
    input_text_color = "#FFFFFF"
else:
    background_color = "#FFF8DC"
    text_color = "#333333"
    result_color = "#FF4500"
    input_bg_color = "#FFFFFF"
    input_text_color = "#000000"

# Streamlit App Configuration
st.set_page_config(page_title="Finance Calculator", page_icon="\U0001F4B0", layout="centered")

# Apply styling dynamically
st.markdown(
    f"""
    <style>
        .main-header {{
            font-size: 35px;
            font-weight: bold;
            text-align: center;
            color: {result_color};
            font-family: 'Arial', sans-serif;
            margin-top: 10px;
        }}
        .sub-header {{
            font-size: 18px;
            text-align: center;
            color: {text_color};
            margin-bottom: 20px;
        }}
        .stApp {{
            background-color: {background_color};
            color: {text_color};
        }}
        input {{
            border: 1px solid {result_color};
            padding: 10px;
            border-radius: 5px;
            width: 100%;
            background-color: {input_bg_color};
            color: {input_text_color};
        }}
        h2 {{
            color: {result_color};
        }}
        strong {{
            color: {result_color};
        }}
        p {{
            font-size: 18px;
            color: {text_color};
        }}
    </style>
    <div class="main-header">Finance Calculator</div>
    <div class="sub-header">Calculate your gold business interest with ease</div>
    """,
    unsafe_allow_html=True
)

# Input Section
st.markdown("### Enter Details")
start_date = st.text_input("Start Date (dd/mm/YYYY)", value="01/01/2024")
end_date = st.text_input("End Date (dd/mm/YYYY)", value="31/12/2024")
amount = st.number_input("Principal Amount (₹)", value=20000, min_value=0, step=1000)
interest_rate = st.number_input("Monthly Interest Rate (%)", value=1.75, min_value=0.0, step=0.01)

# Calculate Button
if st.button("Calculate Interest"):
    try:
        if datetime.strptime(start_date, "%d/%m/%Y") >= datetime.strptime(end_date, "%d/%m/%Y"):
            st.error("Start Date must be before End Date.")
        else:
            months_diff, full_months_interest, remaining_days, partial_month_interest, total_interest = calculate_interest(
                start_date, 
                end_date, 
                amount, 
                interest_rate
            )
            # Display results
            st.markdown(
                f"""
                <div style="text-align: center; margin-top: 20px;">
                    <h2>Calculation Results</h2>
                    <p>Number of Months: <strong>{months_diff}</strong></p>
                    <p>Interest for Full Months: <strong>₹{full_months_interest:.2f}</strong></p>
                    <p>Remaining Days: <strong>{remaining_days}</strong></p>
                    <p>Remaining Days Interest: <strong>₹{partial_month_interest}</strong></p>
                    <p>Total Interest: <strong>₹{total_interest}</strong></p>
                </div>
                """,
                unsafe_allow_html=True
            )
    except ValueError:
        st.error("Please enter dates in the correct format: dd/mm/YYYY.")

# Footer
st.markdown(
    f"""
    <hr style="border: 1px solid {result_color};">
    <p style="text-align: center; font-size: 14px; color: {text_color};">&copy; 2024 Gold Business Finance Calculator</p>
    """,
    unsafe_allow_html=True
)
