from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib

# إنشاء تطبيق FastAPI
app = FastAPI(
    title="Bank Churn Prediction API",
    description="API للتنبؤ بمغادرة عملاء البنك باستخدام الموديل والـ Preprocessor المحفوظين",
    version="2.0.0"
)

# تحميل الموديل وملف الـ Preprocessing عند بدء التشغيل
try:
    model_artifacts = joblib.load('best_churn_model.pkl')
    preprocessor_artifacts = joblib.load('preprocessor.pkl')

    # استخراج المكونات من الـ Dictionaries بناءً على اللي ظاهر في الصورة
    model = model_artifacts['model']
    scaler = preprocessor_artifacts['scaler']
    feature_names = preprocessor_artifacts['features']
    gender_map = preprocessor_artifacts['gender_map']
    geo_map = preprocessor_artifacts['geo_map']
    threshold = preprocessor_artifacts['threshold']
    
except Exception as e:
    model = None
    print(f"Error loading model artifacts: {e}")

# هيكل بيانات المدخلات من المستخدم
class CustomerData(BaseModel):
    CreditScore: int
    Geography: str  # مثال: "France", "Germany", "Spain"
    Gender: str     # مثال: "Male", "Female"
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float

@app.get("/")
def read_root():
    return {"message": "مرحباً بك! نظام التنبؤ بمغادرة العملاء جاهز، استخدم مسار /predict."}

@app.post("/predict")
def predict_churn(data: CustomerData):
    if model is None:
        raise HTTPException(status_code=500, detail="ملفات الموديل غير محملة.")
    
    try:
        input_dict = data.dict()
        input_df = pd.DataFrame([input_dict])
        
        # 1. تطبيق الـ Mappings لو موجودة
        if 'Gender' in input_df.columns and gender_map:
            input_df['Gender'] = input_df['Gender'].map(gender_map)
            
        if 'Geography' in input_df.columns and geo_map:
            input_df['Geography'] = input_df['Geography'].map(geo_map)
            
        # 2. لو الـ Scaler متوقع 12 عمود، لازم نتأكد إن الـ DataFrame فيها نفس الـ 12 عمود بالترتيب
        # (لو عملت One-Hot Encoding في التدريب، لازم تعمله هنا كمان بنفس الطريقة قبل الـ Scaler)
        # لو الـ feature_names اللي حافظها فيها الـ 12 عمود:
        
        # لو فيه أعمدة ناقصة (بسبب الـ Encoding)، ممكن تظبطها كده:
        for col in feature_names:
            if col not in input_df.columns:
                input_df[col] = 0  # أو القيمة الافتراضية المناسبة
                
        # إعادة ترتيب الأعمدة בדיוק زي ما الـ Scaler متوقعها
        input_df = input_df[feature_names]
        
        # 3. الـ Scaling
        scaled_data = scaler.transform(input_df)
        
        # 4. التنبؤ
        probabilities = model.predict_proba(scaled_data)
        churn_prob = float(probabilities[0][1])
        
        prediction = 1 if churn_prob >= threshold else 0
        
        return {
            "status": "Churning" if prediction == 1 else "Loyal Customer",
            "churn_probability": f"{round(churn_prob * 100, 2)}%"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"حدث خطأ أثناء المعالجة: {str(e)}")