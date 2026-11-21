<div align="center">

# 🏦 Bank Customer Churn — Prediction & Analysis

**Predicting which bank customers are about to leave — and why.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Railway](https://img.shields.io/badge/Deployed%20on-Railway-0B0D0E?logo=railway&logoColor=white)](https://railway.app/)

</div>

---

## 📌 Overview

Customer churn — when a customer closes their account or stops using bank services — is one of the costliest challenges in the banking sector, as acquiring a new client is significantly more expensive than retaining an existing one.

This project provides an end-to-end machine learning pipeline on the **Bank Customer Churn** dataset (`Bank.csv`), deploying the trained model as a high-performance **FastAPI REST API** on **Railway**, paired with an interactive, custom-themed **Streamlit Web Application** deployed on **Streamlit Community Cloud**.

---

## 🗂️ Project Structure

```text
Bank-Customer-Churn-Prediction/
│
├── main.py                           # FastAPI backend application
├── app.py                            # Streamlit frontend web application
├── Project_F.ipynb                   # Exploratory Data Analysis (EDA) & model training notebook
│
├── best_churn_model.pkl              # Serialized best-performing ML classifier
├── model_scaler.pkl                  # Fitted feature scaler
├── preprocessor.pkl                  # Preprocessing & encoding pipeline
│
├── Bank.csv                          # Bank customer dataset
├── activity_credit_churn.png         # EDA visualization: Activity & Credit Score vs Churn
├── churn_distribution.png            # EDA visualization: Target class distribution
├── demographics_churn.png            # EDA visualization: Demographics vs Churn
├── numeric_features_churn.png        # EDA visualization: Numerical features distribution
├── tenure_products_churn.png         # EDA visualization: Tenure & Products vs Churn
│
├── Procfile                          # Railway deployment start command
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
└── README.md                         # Project documentation
```
---

## 🚀✅ Getting Started (Local Development)

### 1. Clone the repository

```bash
git clone [https://github.com/abdallahsayedabdallah74/Bank-Customer-Churn-Prediction.git](https://github.com/abdallahsayedabdallah74/Bank-Customer-Churn-Prediction.git)
cd Bank-Customer-Churn-Prediction
```

### 2. 🔃Set up the environment

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the FastAPI Backend locally

```bash
uvicorn main:app --reload
```
The API will be available at http://localhost:8000.
Swagger UI Docs: http://localhost:8000/docs
Health Check: http://localhost:8000/

### 4. Test the /predict endpoint
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "CreditScore": 650,
    "Age": 35,
    "Tenure": 3,
    "Balance": 50000.0,
    "NumOfProducts": 1,
    "HasCrCard": 0,
    "IsActiveMember": 0,
    "EstimatedSalary": 60000.0,
    "Geography": "France",
    "Gender": "Male"
  }'
```
### Example response:
```bash
JSON
{
  "status": "Churning",
  "churn_probability": "54.23%"
}
```
### 5. Run the Streamlit Frontend locally
Open a second terminal (while FastAPI is running) and execute:
```bash 
streamlit run app.py
Then open http://localhost:8501 in your browser.
```
🌐 Live Deployment Architecture
```bash
Deploy the API to Railway
Push the repository to GitHub.
Go to railway.app → New Project → Deploy from GitHub.
```
Railway will auto-detect the Procfile:
```bash
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```
Deploy and copy the live Railway URL (e.g., https://web-production-927c0f79.up.railway.app).


Backend — FastAPI on Railway
Connected the GitHub repository (abdallahsayedabdallah74/Bank-Customer-Churn-Prediction) to Railway.
Railway automatically detects the Procfile:
```bash
web: uvicorn main:app --host 0.0.0.0 --port \$PORT
```
Live API Endpoint: https://web-production-927c0f79.up.railway.app/predict

Frontend — Streamlit Community Cloud
Connected app.py from the same GitHub repository to Streamlit Community Cloud.

Configured API_URL in app.py to communicate directly with the live Railway FastAPI service.

Styled with a custom light-mode palette (#FFF8EA background & #815B5B typography/accents) for clean readability and responsive UX.


## 📊 Model & Input Features 

### Input Features

| Feature | Type | Description / Values |
| :--- | :--- | :--- |
| `CreditScore` | `int` | Customer's credit score (`300` – `850`) |
| `Geography` | `str` | Customer's country (`France`, `Spain`, `Germany`) |
| `Gender` | `str` | Customer's gender (`Male`, `Female`) |
| `Age` | `int` | Customer's age (`18` – `100`) |
| `Tenure` | `int` | Number of years with the bank (`0` – `10`) |
| `Balance` | `float` | Current account balance |
| `NumOfProducts` | `int` | Number of bank products held (`1` – `4`) |
| `HasCrCard` | `int` | Credit card ownership (`1` = Yes, `0` = No) |
| `IsActiveMember` | `int` | Active membership status (`1` = Yes, `0` = No) |
| `EstimatedSalary` | `float` | Customer's estimated annual salary |

---

## 🛠️ Tech Stack

`Python` · `pandas` · `NumPy` · `scikit-learn` · `imbalanced-learn` · `FastAPI` · `Uvicorn` · `HTML/CSS/JS`

---

## 📁 Dataset

[Bank Customer Churn] — 165,034 rows × 14 columns.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
