import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Bank Customer Churn Prediction", page_icon="🏦", layout="centered"
)

# Custom CSS for perfect contrast and custom color palette
st.markdown(
    """
    <style>
    /* Main Background */
    .stApp {
        background-color: #FFF8EA;
    }
    
    /* Main Title */
    h1 {
        color: #815B5B !important;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
    
    /* Subtitle & general text */
    p, .stMarkdown p {
        color: #815B5B !important;
        font-size: 16px;
        font-weight: 500;
    }

    /* Subheaders like Prediction Results */
    h2, h3 {
        color: #815B5B !important;
    }

    /* Form Container */
    [data-testid="stForm"] {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 6px 24px rgba(129, 91, 91, 0.12);
        border: 2px solid #815B5B;
    }

    /* Form Labels */
    label, .stNumberInput label, .stSelectbox label {
        color: #815B5B !important;
        font-weight: 600 !important;
    }

    /* Submit Button */
    .stFormSubmitButton button {
        background-color: #815B5B !important;
        color: #FFF8EA !important;
        font-weight: bold;
        width: 100%;
        border-radius: 8px;
        padding: 12px;
        border: none;
        font-size: 16px;
        transition: 0.3s;
    }
    .stFormSubmitButton button:hover {
        background-color: #6a4a4a !important;
        color: #FFF8EA !important;
    }

    /* Fix Streamlit error/success boxes text contrast */
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
      
      # تعديل تصميم الكارد الخاص بالنتيجة عشان يظهر بشكل شيك وواضح مع الألوان
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
            <div style="
                background-color: {bg_c};
                border-left: 6px solid {border_c};
                padding: 18px;
                border-radius: 8px;
                margin-top: 10px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            ">
                <h4 style="color: {text_c} !important; margin: 0 0 6px 0; font-size: 18px; font-weight: bold;">
                    {icon} Status: {status}
                </h4>
                <p style="color: #333333 !important; margin: 0; font-size: 16px; font-weight: 600;">
                    Churn Probability: <span style="color: {text_c};">{probability}</span>
                </p>
            </div>
        """,
          unsafe_allow_html=True,
      )
    else:
      st.error(f"Error from API: {response.text}")

  except Exception as e:
    st.error(f"Could not connect to the API server. Error: {e}")