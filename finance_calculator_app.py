import streamlit as st
from datetime import datetime, timedelta

# Function to calculate interest (unchanged)
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
st.set_page_config(page_title="Finance Calculator", page_icon="💰", layout="wide")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    body {
        font-family: 'Poppins', sans-serif;
        color: #333;
        background-color: #f0f2f5;
    }
    
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #FFD700;
        margin: 2rem 0 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
    }
    
    .card {
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 2rem;
        margin-bottom: 2rem;
    }
    
    .input-section h3 {
        color: #2c3e50;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    
    .stNumberInput > div > div > input {
        border-radius: 10px;
    }
    
    .stButton > button {
        background-color: #FFD700;
        color: #333;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #FFC300;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .results-section h2 {
        color: #2ecc71;
        font-size: 2rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .result-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
        font-size: 1.1rem;
        padding: 0.5rem;
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    
    .result-label {
        font-weight: 500;
    }
    
    .result-value {
        font-weight: 600;
        color: #e74c3c;
    }
    
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #FFD700;
        font-size: 0.9rem;
        color: #888;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .sub-header {
            font-size: 1rem;
        }
        
        .card {
            padding: 1.5rem;
        }
        
        .stButton > button {
            padding: 0.6rem 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<h1 class="main-header">Finance Calculator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Calculate your gold business interest with ease</p>', unsafe_allow_html=True)

# Input Section
st.markdown('<div class="card input-section">', unsafe_allow_html=True)
st.markdown('### Enter Details')

col1, col2 = st.columns(2)
with col1:
    start_date = st.text_input("Start Date (dd/mm/YYYY)", value="01/01/2024", key="start_date")
with col2:
    end_date = st.text_input("End Date (dd/mm/YYYY)", value="31/12/2024", key="end_date")

amount = st.number_input("Principal Amount (₹)", value=20000, min_value=0, step=1000, key="amount")
interest_rate = st.number_input("Monthly Interest Rate (%)", value=1.75, min_value=0.0, step=0.01, key="interest_rate")

calculate_button = st.button("Calculate Interest", key="calculate_button")

st.markdown('</div>', unsafe_allow_html=True)

# Calculate and Display Results
if calculate_button:
    try:
        if datetime.strptime(start_date, "%d/%m/%Y") >= datetime.strptime(end_date, "%d/%m/%Y"):
            st.error("Start Date must be before End Date.")
        else:
            years_diff, total_interest, rem_months, rem_days, rem_months_interest, rem_days_interest = calculate_interest(
                start_date, 
                end_date, 
                amount, 
                interest_rate
            )
            
            # Display results
            st.markdown('<div class="card results-section">', unsafe_allow_html=True)
            st.markdown('<h2>Calculation Results</h2>', unsafe_allow_html=True)
            
            results = [
                ("Number of Full Years", f"{years_diff}"),
                ("Number of Remaining Months", f"{rem_months}"),
                ("Interest for Remaining Months", f"₹{rem_months_interest:.2f}"),
                ("Number of Remaining Days", f"{rem_days}"),
                ("Interest for Remaining Days", f"₹{rem_days_interest:.2f}"),
                ("Total Interest", f"₹{total_interest:.2f}")
            ]
            
            for label, value in results:
                st.markdown(f'<div class="result-item"><span class="result-label">{label}:</span> <span class="result-value">{value}</span></div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    except ValueError:
        st.error("Please enter dates in the correct format: dd/mm/YYYY.")

# Footer
st.markdown('<div class="footer">&copy; 2024 Gold Business Finance Calculator</div>', unsafe_allow_html=True)

