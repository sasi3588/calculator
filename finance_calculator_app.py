import streamlit as st
from datetime import datetime

# Function to calculate interest
def calculate_interest(start_date, end_date, amount, interest_rate):
    # Parse the input dates
    start_date = datetime.strptime(start_date, "%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%d/%m/%Y")
    
    total_interest = 0.0
    principal = amount

    # Calculate the total number of full years and the remaining period
    years_diff = end_date.year - start_date.year
    remaining_end_date = start_date.replace(year=start_date.year + years_diff)

    # If the remaining_end_date exceeds the end_date, adjust the years_diff and remaining period
    if remaining_end_date > end_date:
        years_diff -= 1
        remaining_end_date = start_date.replace(year=start_date.year + years_diff)
    
    # Calculate interest for each full year with compounding
    for year in range(years_diff):
        year_start_date = start_date.replace(year=start_date.year + year)
        year_end_date = year_start_date.replace(year=year_start_date.year + 1) - timedelta(days=1)
        
        # Calculate interest for one year with compounding
        yearly_interest = principal * (interest_rate / 100) * 12  # 12 months
        total_interest += yearly_interest
        principal += yearly_interest  # Compound the interest into the principal
    
    # Calculate interest for the remaining months/days
    remaining_months = (end_date.year - remaining_end_date.year) * 12 + end_date.month - remaining_end_date.month
    start_of_last_month = remaining_end_date.replace(day=1, month=end_date.month)
    remaining_days = (end_date - start_of_last_month).days
    
    if remaining_days >= 30:
        remaining_months += 1
        remaining_days -= 30
    
    # Calculate interest for full remaining months
    remaining_months_interest = principal * (interest_rate / 100) * remaining_months
    total_interest += remaining_months_interest

    # Calculate interest for remaining days
    amount_per_month = principal * (interest_rate / 100)
    remaining_days_interest = round(amount_per_month * (remaining_days / 30), 2)
    total_interest += remaining_days_interest

    return years_diff, total_interest, remaining_months, remaining_days, remaining_months_interest, remaining_days_interest

# Streamlit App Configuration
st.set_page_config(page_title="Finance Calculator", page_icon="\U0001F4B0", layout="centered")

# App Styling
st.markdown(
    """
    <style>
        .main-header {
            font-size: 35px;
            font-weight: bold;
            text-align: center;
            color: #FFD700;
            font-family: 'Arial', sans-serif;
            margin-top: 10px;
        }
        .sub-header {
            font-size: 18px;
            text-align: center;
            color: #555;
            margin-bottom: 20px;
        }
        .light-mode {
            background-color: #FFF8DC;
            color: #000;
        }
        .dark-mode {
            background-color: #2C2C2C;
            color: #FFF;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Mode Toggle
mode = st.radio("Select Mode", ["Light", "Dark"], horizontal=True)
mode_class = "light-mode" if mode == "Light" else "dark-mode"

# Header
st.markdown(
    f"""
    <div class="{mode_class}">
        <div class="main-header">Finance Calculator</div>
        <div class="sub-header">Calculate your gold business interest with ease</div>
    </div>
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
                <div style="text-align: center; margin-top: 20px; color: {'#FFF' if mode == 'Dark' else '#000'};">
                    <h2 style="color: #008000;">Calculation Results</h2>
                    <p style="font-size: 18px;">Number of Months: <strong style="color: #FF4500;">{months_diff}</strong></p>
                    <p style="font-size: 18px;">Interest for Full Months: <strong style="color: #FF4500;">₹{full_months_interest:.2f}</strong></p>
                    <p style="font-size: 18px;">Remaining Days: <strong style="color: #FF4500;">{remaining_days}</strong></p>
                    <p style="font-size: 18px;">Remaining Days Interest: <strong style="color: #FF4500;">₹{partial_month_interest}</strong></p>
                    <p style="font-size: 18px;">Total Interest: <strong style="color: #FF4500;">₹{total_interest}</strong></p>
                </div>
                """,
                unsafe_allow_html=True
            )
    except ValueError:
        st.error("Please enter dates in the correct format: dd/mm/YYYY.")

# Footer
st.markdown(
    f"""
    <div class="{mode_class}">
        <hr style="border: 1px solid #FFD700;">
        <p style="text-align: center; font-size: 14px; color: {'#CCC' if mode == 'Dark' else '#888'};">
            &copy; 2024 Gold Business Finance Calculator
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
