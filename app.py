import requests
import streamlit as st

# Page Configuration - تم تغيير الـ layout إلى wide عشان يحل مشكلة الطول والعرض
st.set_page_config(
    page_title="Bank Customer Churn Prediction",
    page_icon="🏦",
    layout="wide",
)

# Custom CSS for perfect layout, wide view, and custom colors
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
        margin-bottom: 0px;
    }
    
    /* Subtitle & general text */
    p, .stMarkdown p {
        color: #815B5B !important;
        font-size: 16px;
        font-weight: 500;
        text-align: center;
    }

    /* Subheaders like Prediction Results */
    h2, h3 {
        color: #815B5B !important;
    }

    /* Form Container - جعل الفورم تأخذ عرض متناسق وغير مبالغ في طوله */
    [data-testid="stForm"] {
        background-color: #ffffff;
        padding: 25px 35px;
        border-radius: 16px;
        box-shadow: 0 6px 24px rgba(129, 91, 91, 0.12);
        border: 2px solid #815B5B;
        max-width: 850px;
        margin: 0 auto;
    }

    /* Form Labels */
    label, .stNumberInput label, .stSelectbox label {
        color: #815B5B !important;
        font-weight: 600 !important;
    }

    /* Submit Button Styling */
    div.stFormSubmitButton > button {
        background-color: #815B5B !important;
        color: #FFFFFF !important;
        font-weight: bold;
        width: 100%;
        border-radius: 8px;
        padding: 12px;
        border: none;
        font-size: 16px;
        transition: 0.3s;
    }
    
    div.stFormSubmitButton > button * {
        color: #FFFFFF !important;
    }

    div.stFormSubmitButton > button:hover {
        background-color: #6a4a4a !important;
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🏦 Bank Customer Churn Prediction")
st.markdown(
    "<p>Enter customer details below to check if they are at risk of"
    " churning.</p>",
    unsafe_allow_html=True,
)

# Your live FastAPI URL on Railway
API_URL = "https://web-production-927c0f79.up.railway.app/predict"

# وضع الفورم في المنتصف بعرض منسق ومريح للعين
col_spacer1, col_form, col_spacer2 = st.columns([1, 2.5, 1])

with col_form:
  with st.form("churn_form"):
    c1, c2 = st.columns(2)

    with c1:
      credit_score = st.number_input(
          "Credit Score", min_value=300, max_value=850, value=650
      )
      age = st.number_input("Age", min_value=18, max_value=100, value=35)
      tenure = st.number_input(
          "Tenure (Years)", min_value=0, max_value=10, value=3
      )
      balance = st.number_input("Balance", min_value=0.0, value=50000.0)

    with c2:
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
    gender = st.selectbox("Gender", options=[address := "Male", "Female"])

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

        # كارد النتيجة جوه الفورم مباشرة تحت الزرار
        st.markdown(
            f"""
                <div style="
                    background-color: {bg_c};
                    border-left: 6px solid {border_c};
                    padding: 16px;
                    border-radius: 8px;
                    margin-top: 15px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
                ">
                    <p style="color: {text_c} !important; font-size: 17px; font-weight: bold; margin: 0 0 6px 0; text-align: left !important;">
                        {icon} Status: {status}
                    </p>
                    <p style="color: #333333 !important; font-size: 15px; font-weight: 600; margin: 0; text-align: left !important;">
                        Churn Probability: <span style="color: {text_c} !important;">{probability}</span>
                    </p>
                </div>
            """,
            unsafe_allow_html=True,
        )
      else:
        st.error(f"Error from API: {response.text}")

    except Exception as e:
      st.error(f"Could not connect to the API server. Error: {e}")
