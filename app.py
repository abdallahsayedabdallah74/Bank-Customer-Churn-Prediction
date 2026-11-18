import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Bank Customer Churn Prediction", page_icon="🏦", layout="centered"
)

# Custom CSS - Modern Indigo + Slate palette
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, .stApp, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #F4F6FB; }
    .block-container { max-width: 780px !important; padding-top: 2.5rem; }

    /* Title */
    h1 {
        color: #0F172A !important;
        text-align: center;
        font-weight: 800;
        font-size: 2rem !important;
        letter-spacing: -0.5px;
        white-space: nowrap;
    }
    h2, h3 { color: #0F172A !important; font-weight: 700; }
    .stMarkdown p { color: #64748B !important; font-weight: 500; }

    /* Form card */
    [data-testid="stForm"] {
        background-color: #FFFFFF;
        padding: 32px;
        border-radius: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 40px rgba(15, 23, 42, 0.06);
    }

    /* Labels */
    [data-testid="stWidgetLabel"] p {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    /* Inputs: light background on all layers */
    [data-baseweb="input"],
    [data-baseweb="input"] > div,
    [data-baseweb="base-input"],
    [data-baseweb="select"] > div,
    [data-baseweb="select"] > div > div {
        background-color: #F8FAFC !important;
    }
    [data-baseweb="input"],
    [data-baseweb="select"] > div {
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 10px !important;
        transition: all 0.2s;
    }
    [data-baseweb="input"]:focus-within,
    [data-baseweb="select"] > div:focus-within {
        border-color: #4F46E5 !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
    }

    /* Text inside inputs */
    [data-baseweb="input"] input,
    [data-baseweb="select"] div,
    [data-baseweb="select"] span {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        background-color: transparent !important;
        font-weight: 500 !important;
    }
    [data-baseweb="select"] svg { fill: #64748B !important; }

    /* +/- buttons */
    .stNumberInput button {
        background-color: #EEF2FF !important;
        color: #4F46E5 !important;
        border: none !important;
    }
    .stNumberInput button:hover {
        background-color: #4F46E5 !important;
        color: #FFFFFF !important;
    }

    /* Dropdown list */
    [data-baseweb="popover"] ul,
    [data-baseweb="menu"] { background-color: #FFFFFF !important; }
    [data-baseweb="popover"] li,
    [data-baseweb="menu"] li {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    [data-baseweb="popover"] li:hover,
    [data-baseweb="menu"] li:hover { background-color: #EEF2FF !important; }

    /* Submit button */
    .stFormSubmitButton button {
        background: linear-gradient(135deg, #4F46E5, #7C3AED) !important;
        width: 100%;
        border-radius: 10px;
        padding: 14px;
        border: none;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.35);
        transition: all 0.2s;
    }
    .stFormSubmitButton button * {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    .stFormSubmitButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 28px rgba(79, 70, 229, 0.45);
    }

    /* Error boxes */
    [data-testid="stAlert"] {
        background-color: #FEF2F2 !important;
        border: 1px solid #FECACA !important;
        border-radius: 12px;
    }
    [data-testid="stAlert"] * { color: #991B1B !important; }
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
        bg_c, border_c, text_c, icon = "#FEF2F2", "#DC2626", "#991B1B", "⚠️"
        label = "High risk of churning"
      else:
        bg_c, border_c, text_c, icon = "#ECFDF5", "#059669", "#065F46", "✅"
        label = "Likely to stay"

      st.markdown(
          f"""
<div style="background-color:{bg_c}; border:1px solid {border_c}33; border-left:6px solid {border_c}; padding:22px 24px; border-radius:14px; margin-top:12px; box-shadow:0 6px 24px rgba(15,23,42,0.06);">
  <div style="color:{text_c} !important; font-size:20px; font-weight:800; margin-bottom:6px;">
    {icon} Status: {status}
  </div>
  <div style="color:{text_c} !important; font-size:14px; font-weight:500; opacity:0.85; margin-bottom:10px;">
    {label}
  </div>
  <div style="color:#0F172A !important; font-size:16px; font-weight:600;">
    Churn Probability: <span style="color:{border_c} !important; font-weight:800; font-size:22px;">{probability}</span>
  </div>
</div>
""",
          unsafe_allow_html=True,
      )
    else:
      st.error(f"Error from API: {response.text}")

  except Exception as e:
    st.error(f"Could not connect to the API server. Error: {e}")