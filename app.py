import joblib  # أو pickle حسب ما حفظت الموديل
import pandas as pd
import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Bank Customer Churn Prediction", page_icon="🏦", layout="centered"
)

# 2. كود الـ CSS لتظبيط الثيم، الخلفية، الألوان، وزرار الـ Predict
st.markdown(
    """
<style>
/* الخلفية العامة للصفحة (بيج هادي) */
.stApp {
    background-color: #FAF6F0;
    color: #4E342E;
}

/* تظبيط العناوين */
h1, h2, h3, p, label {
    color: #4E342E !important;
}

/* إطار الفورم */
[data-testid="stForm"] {
    background-color: #FFFFFF;
    border: 2px solid #8D6E63;
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 4px 12px rgba(78, 52, 46, 0.08);
}

/* تظبيط زرار الـ Predict */
div.stFormSubmitButton > button {
    background-color: #5D4037 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-size: 16px !important;
    font-weight: bold !important;
    margin-top: 15px;
    transition: all 0.3s ease;
}

div.stFormSubmitButton > button:hover {
    background-color: #3E2723 !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}
</style>
""",
    unsafe_allow_html=True,
)


# 3. تحميل الموديل المحفوظ (عدّل الاسم لاسم ملفك)
@st.cache_resource
def load_model():
    return joblib.load("best_churn_model.pkl")


try:
    model = load_model()
except Exception as e:
    st.error(f"تأكد من وجود ملف الموديل في نفس الفولدر: {e}")
    st.stop()

# 4. واجهة التطبيق وإدخال البيانات
st.title("🏦 Bank Customer Churn Prediction")
st.write("Enter customer details below to check if they are at risk of churning.")

with st.form("churn_form"):
    col1, col2 = st.columns(2)

    with col1:
        credit_score = st.number_input(
            "Credit Score", min_value=300, max_value=850, value=650
        )
        age = st.number_input("Age", min_value=18, max_value=100, value=35)
        tenure = st.number_input(
            "Tenure (Years)", min_value=0, max_value=10, value=3
        )
        balance = st.number_input(
            "Balance", min_value=0.0, value=50000.00, format="%.2f"
        )

    with col2:
        num_of_products = st.number_input(
            "Number of Products", min_value=1, max_value=4, value=1
        )
        has_cr_card = st.selectbox("Has Credit Card", ["No", "Yes"])
        is_active_member = st.selectbox("Is Active Member", ["No", "Yes"])
        estimated_salary = st.number_input(
            "Estimated Salary", min_value=0.0, value=60000.00, format="%.2f"
        )

    geography = st.selectbox("Geography", ["France", "Spain", "Germany"])
    gender = st.selectbox("Gender", ["Male", "Female"])

    # الزرار واخد العرض كامل
    submitted = st.form_submit_button("Predict Churn", use_container_width=True)

# 5. معالجة البيانات والتنبؤ وعرض النتيجة في كارت احترافي
if submitted:
    # تحويل Yes/No إلى 1/0
    has_cr_card_val = 1 if has_cr_card == "Yes" else 0
    is_active_member_val = 1 if is_active_member == "Yes" else 0

    # تجهيز البيانات بنفس أسماء الأعمدة اللي اتدرب عليها الموديل
    input_data = pd.DataFrame({
        "CreditScore": [credit_score],
        "Geography": [geography],
        "Gender": [gender],
        "Age": [age],
        "Tenure": [tenure],
        "Balance": [balance],
        "NumOfProducts": [num_of_products],
        "HasCrCard": [has_cr_card_val],
        "IsActiveMember": [is_active_member_val],
        "EstimatedSalary": [estimated_salary],
    })

    # التنبؤ وحساب الاحتمالية
    prediction = model.predict(input_data)[0]
    prob = model.predict_proba(input_data)[0][1]

    st.markdown("### Prediction Results:")

    if prediction == 1:
        bg_color = "#FDECEA"
        border_color = "#D93025"
        text_color = "#A50E0E"
        status_text = "⚠️ High Risk: Customer is Likely to Churn"
    else:
        bg_color = "#E6F4EA"
        border_color = "#1E8E3E"
        text_color = "#137333"
        status_text = "✅ Low Risk: Customer is Likely to Stay"

    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            border-left: 6px solid {border_color};
            padding: 20px;
            border-radius: 10px;
            margin-top: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        ">
            <h4 style="color: {text_color}; margin: 0 0 8px 0; font-size: 18px;">
                {status_text}
            </h4>
            <p style="color: #333333; margin: 0; font-size: 16px;">
                Churn Probability: <b>{prob * 100:.2f}%</b>
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )