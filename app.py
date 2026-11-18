
import requests
import streamlit as st
import textwrap

# ==========================================
# 1. Page Configuration
# ==========================================

st.set_page_config(
    page_title="Bank Customer Churn Prediction",
    page_icon="🏦",
    layout="centered"
)

# ==========================================
# 2. Custom CSS - Modern Banking Theme
# ==========================================

st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #F1F5F9;
}

/* Main Container */
.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main Title */
h1 {
    color: #183B56 !important;
    text-align: center;
    font-weight: 800 !important;
    font-size: 2.3rem !important;
}

/* Subtitle */
.stApp p {
    color: #64748B;
}

/* Section Titles */
h2, h3 {
    color: #183B56 !important;
    font-weight: 700 !important;
}

/* Form Container */
[data-testid="stForm"] {
    background-color: #FFFFFF;
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 8px 25px rgba(24, 59, 86, 0.07);
}

/* Labels */
[data-testid="stForm"] label {
    color: #334155 !important;
    font-weight: 600 !important;
}

/* Number Input Container */
[data-testid="stNumberInput"] div[data-baseweb="input"] {
    background-color: #F8FAFC !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 9px !important;
    overflow: hidden;
}

/* Number Input Text */
[data-testid="stNumberInput"] input {
    background-color: #F8FAFC !important;
    color: #183B56 !important;
    border: none !important;
}

/* Number Input Buttons */
[data-testid="stNumberInput"] button {
    background-color: #E2E8F0 !important;
    color: #183B56 !important;
    border: none !important;
}

/* Select Box */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #F8FAFC !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 9px !important;
    color: #183B56 !important;
}

/* Select Box Text */
[data-testid="stSelectbox"] div[data-baseweb="select"] span {
    color: #183B56 !important;
}

/* Select Dropdown Menu */
[data-baseweb="popover"] {
    background-color: #FFFFFF !important;
}

[data-baseweb="menu"] {
    background-color: #FFFFFF !important;
}

[data-baseweb="menu"] * {
    color: #183B56 !important;
}

/* Input Focus */
[data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within,
[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
    border-color: #0D9488 !important;
    box-shadow: 0 0 0 1px #0D9488 !important;
}

/* Predict Button */
.stFormSubmitButton button {
    background-color: #183B56 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    width: 100%;
    min-height: 48px;
    font-size: 16px !important;
    font-weight: 700 !important;
    transition: 0.3s ease;
}

.stFormSubmitButton button:hover {
    background-color: #0D9488 !important;
    color: #FFFFFF !important;
    transform: translateY(-2px);
}

/* Prediction Result Card */
.prediction-card {
    padding: 25px;
    border-radius: 14px;
    margin-top: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.04);
}

/* Result Title */
.prediction-title {
    font-size: 21px;
    font-weight: 800;
    margin-bottom: 12px;
}

/* Result Description */
.prediction-message {
    color: #475569;
    font-size: 15px;
    margin-bottom: 20px;
}

/* Probability Label */
.probability-label {
    color: #64748B;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
}

/* Probability Value */
.probability-value {
    font-size: 36px;
    font-weight: 800;
    margin-top: 5px;
}

/* Footer */
.footer {
    text-align: center;
    color: #94A3B8;
    font-size: 13px;
    margin-top: 35px;
}

/* Responsive */
@media (max-width: 640px) {
    h1 {
        font-size: 1.7rem !important;
    }

    [data-testid="stForm"] {
        padding: 18px;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. Page Header
# ==========================================

st.title("🏦 Bank Customer Churn Prediction")

st.markdown(
    """
    <p style="
        text-align: center;
        font-size: 16px;
        margin-bottom: 30px;
    ">
        Enter customer details below to check if they are at risk of churning.
    </p>
    """,
    unsafe_allow_html=True
)


# ==========================================
# 4. API Configuration
# ==========================================

API_URL = "https://web-production-927c0f79.up.railway.app/predict"


# ==========================================
# 5. Customer Input Form
# ==========================================

with st.form("churn_form"):

    col1, col2 = st.columns(2)

    with col1:

        credit_score = st.number_input(
            "Credit Score",
            min_value=300,
            max_value=850,
            value=650
        )

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=35
        )

        tenure = st.number_input(
            "Tenure (Years)",
            min_value=0,
            max_value=10,
            value=3
        )

        balance = st.number_input(
            "Balance",
            min_value=0.0,
            value=50000.0
        )

    with col2:

        num_of_products = st.number_input(
            "Number of Products",
            min_value=1,
            max_value=4,
            value=1
        )

        has_cr_card = st.selectbox(
            "Has Credit Card",
            options=[0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        is_active_member = st.selectbox(
            "Is Active Member",
            options=[0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        estimated_salary = st.number_input(
            "Estimated Salary",
            min_value=0.0,
            value=60000.0
        )

    geography = st.selectbox(
        "Geography",
        options=["France", "Spain", "Germany"]
    )

    gender = st.selectbox(
        "Gender",
        options=["Male", "Female"]
    )

    st.markdown("<br>", unsafe_allow_html=True)

    submit_button = st.form_submit_button(
        "🔍 Predict Churn",
        use_container_width=True
    )


# ==========================================
# 6. Prediction Process
# ==========================================

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
        "Gender": gender
    }

    try:

        with st.spinner("Connecting to API and predicting..."):

            response = requests.post(
                API_URL,
                json=input_data,
                timeout=30
            )

        if response.status_code == 200:

            result = response.json()

            status = result.get("status")
            probability = result.get("churn_probability")

            # ==================================
            # 7. Prediction Results
            # ==================================

            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader("📊 Prediction Results")

            if status == "Churning":

                bg_c = "#FEF2F2"
                border_c = "#DC2626"
                text_c = "#B91C1C"
                icon = "⚠️"

                message = (
                    "This customer is at risk of leaving the bank."
                )

            else:

                bg_c = "#ECFDF5"
                border_c = "#059669"
                text_c = "#047857"
                icon = "✅"

                message = (
                    "This customer is likely to stay with the bank."
                )

            # Format probability if it is numeric
            if isinstance(probability, (int, float)):
                probability_display = f"{probability:.2f}%"
            else:
                probability_display = str(probability)

            # Build Result Card
            result_card = f"""
<div class="prediction-card" style="
    background-color: {bg_c};
    border-left: 6px solid {border_c};
">

    <div class="prediction-title" style="color: {text_c};">
        {icon} Prediction: {status}
    </div>

    <div class="prediction-message">
        {message}
    </div>

    <div class="probability-label">
        CHURN PROBABILITY
    </div>

    <div class="probability-value" style="color: {text_c};">
        {probability_display}
    </div>

</div>
"""

            # Display HTML correctly
            st.markdown(
                textwrap.dedent(result_card),
                unsafe_allow_html=True
            )

        else:

            st.error(
                f"Error from API: {response.text}"
            )

    except requests.exceptions.Timeout:

        st.error(
            "The API request timed out. Please try again."
        )

    except requests.exceptions.RequestException as e:

        st.error(
            f"Could not connect to the API server: {e}"
        )

    except ValueError:

        st.error(
            "The API returned an invalid response."
        )


# ==========================================
# 8. Footer
# ==========================================

st.markdown(
    """
    <div class="footer">
        Bank Customer Churn Prediction
        <br>
        Powered by Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)
