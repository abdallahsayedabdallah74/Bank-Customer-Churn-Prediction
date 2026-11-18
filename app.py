import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Bank Customer Churn Prediction", page_icon="🏦", layout="centered"
)

# Custom CSS
st.markdown(
    """
    <style>
    /* ---------- Layout ---------- */
    .stApp {
        background-color: #FFF8EA;
    }
    .block-container {
        max-width: 780px !important;
        padding-top: 2.5rem;
    }

    /* ---------- Title ---------- */
    h1 {
        color: #815B5B !important;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        font-size: 2.1rem !important;
        white-space: nowrap;
    }

    /* ---------- Text ---------- */
    p, .stMarkdown p {
        color: #815B5B !important;
        font-size: 16px;
        font-weight: 500;
    }
    h2, h3 {
        color: #815B5B !important;
    }

    /* ---------- Form container ---------- */
    [data-testid="stForm"] {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 6px 24px rgba(129, 91, 91, 0.12);
        border: 2px solid #815B5B;
    }

    /* ---------- Labels ---------- */
    label, label p, .stNumberInput label, .stSelectbox label {
        color: #815B5B !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* ---------- Inputs (light style instead of dark) ---------- */
    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    div[data-baseweb="select"] > div {
        background-color: #FFF8EA !important;
        border: 1.5px solid #C9A9A6 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: #815B5B !important;
        box-shadow: 0 0 0 2px rgba(129, 91, 91, 0.2) !important;
    }
    input, textarea,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] span {
        color: #4a3333 !important;
        -webkit-text-fill-color: #4a3333 !important;
        font-weight: 500;
    }
    div[data-baseweb="select"] svg {
        fill: #815B5B !important;
    }

    /* +/- buttons of number input */
    .stNumberInput button {
        background-color: #F3E3D3 !important;
        color: #815B5B !important;
        border: none !important;
    }
    .stNumberInput button:hover {
        background-color: #815B5B !important;
        color: #FFF8EA !important;
    }
    .stNumberInput button svg {
        fill: currentColor !important;
    }

    /* Dropdown menu list */
    ul[role="listbox"],
    div[data-baseweb="popover"] > div {
        background-color: #ffffff !important;
    }
    li[role="option"] {
        color: #815B5B !important;
        background-color: #ffffff !important;
    }
    li[role="option"]:hover,
    li[aria-selected="true"] {
        background-color: #F3E3D3 !important;
    }

    /* ---------- Submit button ---------- */
    .stFormSubmitButton button {
        background-color: #815B5B !important;
        width: 100%;
        border-radius: 8px;
        padding: 12px;
        border: none;
        transition: 0.3s;
    }
    .stFormSubmitButton button p,
    .stFormSubmitButton button span,
    .stFormSubmitButton button div {
        color: #FFF8EA !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    .stFormSubmitButton button:hover {
        background-color: #6a4a4a !important;
    }

    /* ---------- Error / notification boxes ---------- */
    div[data-baseweb="notification"] {
        background-color: #ffffff !important;
        border: 2px solid #815B5B !important;
    }
    div[data-baseweb="notification"] p {
        color: #815B5B !important;
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
        bg_c = "#FDECEA"
        border_c = "#D93025"
        text_c = "#A50E0E"
        icon = "⚠️"
      else:
        bg_c = "#E6F4EA"
        border_c = "#1E8E3E"
        text_c = "#137333"
        icon = "✅"

      st.markdown(
          f"""
<div style="background-color: {bg_c}; border-left: 6px solid {border_c}; padding: 18px 20px; border-radius: 8px; margin-top: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.05);">
  <div style="color: {text_c} !important; margin: 0 0 8px 0; font-size: 20px; font-weight: 700;">
    {icon} Status: {status}
  </div>
  <div style="color: #333333 !important; margin: 0; font-size: 16px; font-weight: 600;">
    Churn Probability: <span style="color: {text_c} !important; font-weight: 700;">{probability}</span>
  </div>
</div>
""",
          unsafe_allow_html=True,
      )
    else:
      st.error(f"Error from API: {response.text}")

  except Exception as e:
    st.error(f"Could not connect to the API server. Error: {e}")