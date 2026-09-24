import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

# Enhanced training data with more careers and features
data = {
    'math_score': [85,92,78,95,88,76,89,94,82,91,87,93,79,96,84],
    'programming_score': [90,88,85,92,87,80,93,96,84,90,91,89,86,97,83],
    'project_score': [88,90,82,94,86,78,91,95,83,92,89,94,80,98,85],
    'communication': ['Good','Excellent','Average','Excellent','Good','Average','Excellent','Excellent','Good','Excellent','Good','Excellent','Average','Excellent','Good'],
    'teamwork': ['Good','Good','Average','Excellent','Good','Good','Excellent','Excellent','Average','Good','Excellent','Good','Good','Excellent','Average'],
    'leadership': ['Average','Good','Average','Excellent','Good','Average','Good','Excellent','Average','Good','Good','Excellent','Average','Excellent','Good'],
    'interest_ml': ['High','Medium','Low','High','High','Medium','High','High','Low','High','High','Medium','Low','High','Medium'],
    'interest_web': ['Medium','High','High','Medium','High','High','Low','Medium','High','Medium','Low','High','High','Medium','High'],
    'interest_embedded': ['Low','Low','Medium','Low','Low','High','Low','Low','Medium','Low','Medium','Low','High','Low','Medium'],
    'interest_mobile': ['Medium','High','Low','Medium','High','Medium','Low','Medium','High','Medium','Low','High','Medium','High','Low'],
    'career': ['Data Scientist','Full Stack Developer','Embedded Engineer','Data Scientist','Full Stack Developer','Embedded Engineer','Data Scientist','AI Engineer','Web Developer','Data Scientist','Mobile App Developer','Full Stack Developer','Embedded Engineer','AI Engineer','DevOps Engineer']
}

def train_model():
    df = pd.DataFrame(data)
    
    # Encode all categorical variables
    encoders = {}
    categorical_cols = ['communication', 'teamwork', 'leadership', 'interest_ml', 'interest_web', 'interest_embedded', 'interest_mobile']
    
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
    
    X = df.drop('career', axis=1)
    y = df['career']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    
    # Save everything
    joblib.dump(model, 'static/model.pkl')
    joblib.dump(scaler, 'static/scaler.pkl')
    joblib.dump(encoders, 'static/encoders.pkl')
    
    print("✅ Enhanced ML Model trained and saved!")
    return model, scaler, encoders

if __name__ == "__main__":
    train_model()