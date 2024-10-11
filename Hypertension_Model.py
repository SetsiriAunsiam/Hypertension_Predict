import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

# โหลดชุดข้อมูล
file_path = 'Hypertension-risk-model-main.csv'
data = pd.read_csv(file_path)

# ลบแถวที่มีค่า NaN
data_cleaned = data.dropna()

# เตรียมข้อมูลที่ล้างแล้ว
X_cleaned = data_cleaned.drop(columns='Risk')  # ข้อมูลฟีเจอร์
y_cleaned = data_cleaned['Risk']  # ข้อมูลเป้าหมาย (Target)

# แบ่งข้อมูลเป็นชุดฝึกและชุดทดสอบ
X_train_cleaned, X_test_cleaned, y_train_cleaned, y_test_cleaned = train_test_split(X_cleaned, 
                                                                                    y_cleaned, 
                                                                                    test_size=0.2, 
                                                                                    random_state=42)

# สร้างและฝึกโมเดล Gradient Boosting
model_cleaned = GradientBoostingClassifier()
model_cleaned.fit(X_train_cleaned, y_train_cleaned)

# ทดสอบโมเดล
y_pred_cleaned = model_cleaned.predict(X_test_cleaned)
accuracy_cleaned = accuracy_score(y_test_cleaned, y_pred_cleaned)
classification_rep_cleaned = classification_report(y_test_cleaned, y_pred_cleaned)

# แสดงผลประสิทธิภาพของโมเดล
print(f"ความแม่นยำของโมเดล: {accuracy_cleaned}")
print(classification_rep_cleaned)

# บันทึกโมเดลที่ฝึกแล้วลงไฟล์สำหรับใช้งาน
with open('hypertension_model.pkl', 'wb') as model_file:
    pickle.dump(model_cleaned, model_file)
