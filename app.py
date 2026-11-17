import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Bank Customer Churn Prediction", page_icon="🏦", layout="centered"
)

# Custom CSS for clean, readable, bright styling
st.markdown(
    """
    <style>
    /* Main background */
    .stApp {
        background-color: #f4f6f9;
    }
    
    /* Main Title Styling - Dark & Clear */
    h1 {
        color: #0f172a !important;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
    
    /* Subtitle Styling */
    p {
        color: #475569 !important;
        font-size: 16px;
    }

    /* Form Container */
    [data-testid="stForm"] {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
    }

    /* Labels inside form - Make them dark and clear */
    label, .stNumberInput label, .stSelectbox label {
        color: #1e293b !important;
        font-weight: 600 !important;
    }

    /* Submit Button Styling */
    .stFormSubmitButton button {
        background-color: #2563eb !important;
        color: white !important;
        font-weight: bold;
        width: 100%;
        border-radius: 8px;
        padding: 12px;
        border: none;
        font-size: 16px;
    }
    .stFormSubmitButton button:hover {
        background-color: #1d4ed8 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🏦 Bank Customer Churn Prediction")
st.markdown(
    "<p style='text-align: center;'>Enter customer details below to check if"
    " they are at risk of churning.</p>",
    unsafe_allow_html=True,
)

# Your live FastAPI URL on Railway
API_URL = "https://web-production-927c0f79.up.railway.app/predict"

with st.form("churn_form"):
  col1, col2 = st.columns(2)

  with col1:
    credit_score = st.number_input(
        "Credit Score", min_value=300, max_value=850, value=650
    )
    age = st.number_input("Age", min_value=18, max_value=100, value=35)
    tenure = st.number_input("Tenure (Years)", min_value=0, max_value=10, value=3)
    balance = st.number_input("Balance", min_value=0.0, value=50000.0)

  with col2:
    num_of_products = st.number_input(
        "Number of Products", min_value=1, max_value=4, value=1
    )
    has_cr_card = st.selectbox(
        "Has Credit Card",
        options=[0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No",
    )
    is_active_member = st.selectbox(
        "Is Active Member",
        options=[0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No",
    )
    estimated_salary = st.number_input(
        "Estimated Salary", min_value=0.0, value=60000.0
    )

  geography = st.selectbox("Geography", options=["France", "Spain", "Germany"])
  gender = st.selectbox("Gender", options=["Male", "Female"])

  submit_button = st.form_submit_button(label="Predict Churn")

if submit_button:
  input_data = {
      "CreditScore": credit_score,
      "Age": age,
      "Tenure": tenure,
      "Balance": balance,
      "NumOfProducts": num_of_products,
      "HasCrCard": has_cr_card,
      "IsActiveMember": is_active_member,
      "EstimatedSalary": estimated_salary,
      "Geography": geography,
      "Gender": gender,
  }

  try:
    with st.spinner("Connecting to API and predicting..."):
      response = requests.post(API_URL, json=input_data)

    if response.status_code == 200:
      result = response.json()
      status = result.get("status")
      probability = result.get("churn_probability")

      st.subheader("Prediction Results:")
      if status == "Churning":
        st.error(f"⚠️ **Status:** {status} (Probability: {probability})")
      else:
        st.success(f"✅ **Status:** {status} (Probability: {probability})")
    else:
      st.error(f"Error from API: {response.text}")

  except Exception as e:
    st.error(f"Could not connect to the API server. Error: {e}")