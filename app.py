from flask import Flask, render_template, request, session, redirect, url_for
import joblib
import numpy as np
import os
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'career_guidance_2024_super_secure_key'

# Load ML model and preprocessors
try:
    model = joblib.load('static/model.pkl')
    scaler = joblib.load('static/scaler.pkl')
    encoders = joblib.load('static/encoders.pkl')
    print("✅ ML Model loaded successfully!")
except:
    print("❌ ERROR: Run 'python ml_model.py' first to create model files!")
    exit()

# Complete Career Roadmap Data

CAREER_ROADMAP = {
    # ✅ ALL possible model predictions
    'Data Scientist': {
        'known_skills': ['Python', 'Math', 'Data Structures'],
        'skills_to_learn': ['Pandas', 'NumPy', 'Scikit-learn', 'SQL', 'Tableau'],
        'roadmap': [
            {'topic': 'Step 1: Data Analysis', 'duration': '2 Weeks', 'details': ['Pandas DataFrames & Series', 'Data Cleaning & Preprocessing', 'Visualization with Matplotlib']},
            {'topic': 'Step 2: SQL Mastery', 'duration': '1 Week', 'details': ['Joins, Unions, & Subqueries', 'Window Functions', 'Database Normalization']},
            {'topic': 'Step 3: Machine Learning', 'duration': '4 Weeks', 'details': ['Supervised & Unsupervised Learning', 'Model Evaluation Metrics', 'Scikit-learn Pipelines']},
            {'topic': 'Step 4: Advanced Practice', 'duration': '4 Weeks', 'details': ['Feature Engineering', 'Kaggle Competitions', 'Ensemble Methods']},
            {'topic': 'Step 5: Portfolio', 'duration': '2 Weeks', 'details': ['Streamlit App Deployment', 'Model Serialization', 'Project Documentation']}
        ],
        'suggestions': ['Kaggle', 'Google Cert', '3 ML projects'],
        'preferred_jobs': ['Data Analyst', 'ML Engineer']
    },
    'Full Stack Developer': {
        'known_skills': ['HTML/CSS', 'JavaScript'],
        'skills_to_learn': ['React', 'Node.js', 'MongoDB', 'Docker'],
        'roadmap': [
            {'topic': 'Step 1: Modern JavaScript', 'duration': '2 Weeks', 'details': ['ES6+ Syntax (Arrow functions, Destructuring)', 'Async/Await & Promises', 'DOM Manipulation']},
            {'topic': 'Step 2: React Frontend', 'duration': '3 Weeks', 'details': ['Components, Props, & State', 'React Hooks (useState, useEffect)', 'Context API & Redux']},
            {'topic': 'Step 3: Node.js Backend', 'duration': '3 Weeks', 'details': ['Express.js Server Setup', 'RESTful API Development', 'Middleware & Error Handling']},
            {'topic': 'Step 4: Database & Integration', 'duration': '4 Weeks', 'details': ['MongoDB Schema Design', 'Authentication (JWT)', 'API Integration with Frontend']},
            {'topic': 'Step 5: Deployment', 'duration': '1 Week', 'details': ['Docker Basics', 'CI/CD Pipelines', 'Hosting on Vercel/Heroku']}
        ],
        'suggestions': ['5+ projects', 'FreeCodeCamp', 'GitHub'],
        'preferred_jobs': ['Frontend', 'Backend', 'MERN Dev']
    },
    'AI Engineer': {
        'known_skills': ['Python', 'ML Basics'],
        'skills_to_learn': ['PyTorch', 'Computer Vision', 'NLP'],
        'roadmap': [
            {'topic': 'Step 1: Deep Learning Basics', 'duration': '2 Weeks', 'details': ['Neural Networks Fundamentals', 'Backpropagation & Loss Functions', 'Activation Functions']},
            {'topic': 'Step 2: PyTorch Framework', 'duration': '4 Weeks', 'details': ['Tensors & Autograd', 'Building CNNs', 'Custom DataLoaders']},
            {'topic': 'Step 3: Computer Vision', 'duration': '3 Weeks', 'details': ['OpenCV Basics', 'Object Detection (YOLO)', 'Image Segmentation']},
            {'topic': 'Step 4: NLP Fundamentals', 'duration': '3 Weeks', 'details': ['Text Preprocessing', 'RNNs & LSTMs', 'Transformers (BERT/GPT)']},
            {'topic': 'Step 5: Deployment & MLOps', 'duration': '2 Weeks', 'details': ['Model Optimization (ONNX)', 'FastAPI Model Serving', 'Containerization']}
        ],
        'suggestions': ['fast.ai', 'HuggingFace', 'AI hackathons'],
        'preferred_jobs': ['ML Engineer', 'CV Engineer']
    },
    'Embedded Engineer': {
        'known_skills': ['C Programming'],
        'skills_to_learn': ['Microcontrollers', 'RTOS', 'IoT'],
        'roadmap': [
            {'topic': 'Step 1: Advanced C', 'duration': '2 Weeks', 'details': ['Pointers & Memory Management', 'Bitwise Operations', 'Structs & Unions']},
            {'topic': 'Step 2: Microcontroller Basics', 'duration': '3 Weeks', 'details': ['GPIO & Interrupts', 'Timers & PWM', 'ADC/DAC Interfacing']},
            {'topic': 'Step 3: Communication Protocols', 'duration': '4 Weeks', 'details': ['UART, I2C, SPI', 'Sensor Integration', 'Debugging techniques']},
            {'topic': 'Step 4: IoT Connectivity', 'duration': '3 Weeks', 'details': ['WiFi (ESP32)', 'MQTT Protocol', 'Cloud Data Logging']},
            {'topic': 'Step 5: RTOS & System Design', 'duration': '2 Weeks', 'details': ['FreeRTOS Tasks & Queues', 'PCB Design Basics', 'Power Management']}
        ],
        'suggestions': ['Arduino', 'Embedded Linux'],
        'preferred_jobs': ['Firmware', 'IoT Developer']
    },
    'Web Developer': {
        'known_skills': ['HTML/CSS'],
        'skills_to_learn': ['React', 'APIs', 'Responsive'],
        'roadmap': [
            {'topic': 'Step 1: Advanced CSS', 'duration': '1 Week', 'details': ['Flexbox & Grid Layouts', 'Responsive Design (Media Queries)', 'CSS Animations']},
            {'topic': 'Step 2: JavaScript Logic', 'duration': '2 Weeks', 'details': ['ES6 Features', 'DOM Events & Manipulation', 'Fetch API & JSON']},
            {'topic': 'Step 3: React Essentials', 'duration': '3 Weeks', 'details': ['Functional Components', 'State Management', 'React Router']},
            {'topic': 'Step 4: Real-world Projects', 'duration': '3 Weeks', 'details': ['Portfolio Website', 'Landing Pages', 'Consuming Public APIs']},
            {'topic': 'Step 5: Freelancing Skills', 'duration': '2 Weeks', 'details': ['Git/GitHub Workflow', 'Client Communication', 'Upwork/Fiverr Profiles']}
        ],
        'suggestions': ['Frontend Mentor', 'Freelancing'],
        'preferred_jobs': ['Frontend Dev']
    },
    'Mobile App Developer': {
        'known_skills': ['Java/Kotlin', 'Basic Programming'],
        'skills_to_learn': ['Flutter/React Native', 'Android/iOS', 'APIs'],
        'roadmap': [
            {'topic': 'Step 1: Dart Language', 'duration': '2 Weeks', 'details': ['Dart Syntax & Collections', 'OOP in Dart', 'Asynchronous Programming']},
            {'topic': 'Step 2: Flutter UI', 'duration': '4 Weeks', 'details': ['Widget Tree & Layouts', 'State Management (Provider)', 'Navigation & Routing']},
            {'topic': 'Step 3: Native Features', 'duration': '3 Weeks', 'details': ['Camera & Location Access', 'Local Storage (Hive/SQLite)', 'API Integration']},
            {'topic': 'Step 4: Deployment', 'duration': '2 Weeks', 'details': ['App Icon & Splash Screen', 'Play Store Publishing', 'App Store Guidelines']}
        ],
        'suggestions': ['Build 3 mobile apps', 'Play Store publish'],
        'preferred_jobs': ['Mobile Developer', 'App Developer']
    },
    'DevOps Engineer': {
        'known_skills': ['Linux Basics', 'Networking'],
        'skills_to_learn': ['Docker', 'Kubernetes', 'AWS', 'CI/CD'],
        'roadmap': [
            {'topic': 'Step 1: Linux Administration', 'duration': '2 Weeks', 'details': ['Shell Scripting (Bash)', 'User & Permissions Management', 'Networking Basics']},
            {'topic': 'Step 2: Containerization', 'duration': '2 Weeks', 'details': ['Dockerfiles & Image Creation', 'Docker Compose', 'Container Networking']},
            {'topic': 'Step 3: AWS Cloud', 'duration': '3 Weeks', 'details': ['EC2, S3, & RDS', 'IAM Security Policies', 'VPC Architecture']},
            {'topic': 'Step 4: Orchestration', 'duration': '3 Weeks', 'details': ['Kubernetes Pods & Services', 'Deployments & ReplicaSets', 'Helm Charts']},
            {'topic': 'Step 5: CI/CD Pipelines', 'duration': '2 Weeks', 'details': ['GitHub Actions / Jenkins', 'Automated Testing Integration', 'Infrastructure as Code (Terraform)']}
        ],
        'suggestions': ['AWS certification', 'Build CI/CD pipeline'],
        'preferred_jobs': ['DevOps Engineer', 'Cloud Engineer']
    }
    # ✅ Now covers ALL model predictions!
}

        

@app.route('/', methods=['GET', 'POST'])
def index():
    """✅ Home with data persistence"""
    return render_template('index.html', student_data=session.get('student_data', {}))

@app.route('/profile', methods=['POST'])
def create_profile():
    """✅ Save ALL form data"""
    student_data = request.form.to_dict()
    session['student_data'] = student_data
    
    print("\n📊 COMPLETE STUDENT DATA:")
    for key, value in student_data.items():
        print(f"   {key}: {value}")
    
    return render_template('profile.html', student_data=student_data)
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    # If the user clicks "Back to Results", it sends a GET request
    if request.method == 'GET':
        return render_template('recommendation.html', profile=session.get('profile', {}))

    """✅ FIXED: Correct 100% probabilities"""
    try:
        data = request.form
        
        # Prepare features (same as before)
        features = [
            float(data.get('math_score', 80)),
            float(data.get('programming_score', 80)),
            float(data.get('project_score', 80)),
            encoders['communication'].transform([data.get('communication', 'Average')])[0],
            encoders['teamwork'].transform([data.get('teamwork', 'Good')])[0],
            encoders['leadership'].transform([data.get('leadership', 'Average')])[0],
            encoders['interest_ml'].transform([data.get('interest_ml', 'Medium')])[0],
            encoders['interest_web'].transform([data.get('interest_web', 'Medium')])[0],
            encoders['interest_embedded'].transform([data.get('interest_embedded', 'Low')])[0],
            encoders['interest_mobile'].transform([data.get('interest_mobile', 'Medium')])[0]
        ]
        
        # ML Prediction
        features_scaled = scaler.transform([features])
        prediction = model.predict(features_scaled)[0]
        raw_probs = model.predict_proba(features_scaled)[0]
        
        # ✅ FIXED: Normalize to 100%
        total_prob = raw_probs.sum()
        normalized_probs = (raw_probs / total_prob * 100).round(1)
        
        # Confidence = highest probability
        confidence = float(normalized_probs.max())
        
        student_profile = {
            'name': data.get('name', 'Student'),
            'branch': data.get('branch', 'CSE'),
            'math_score': data.get('math_score', '85'),
            'programming_score': data.get('programming_score', '88'),
            'project_score': data.get('project_score', '90'),
            'predicted_career': prediction,
            'confidence': confidence,
            'probabilities': dict(zip(model.classes_, normalized_probs)),
            'career_details': CAREER_ROADMAP[prediction]
        }
        
        session['profile'] = student_profile
        print(f"\n🎯 {prediction}: {confidence}% (Total: 100%)")
        print("📊 Probabilities:", dict(zip(model.classes_, normalized_probs)))
        
        # ✅ Print Roadmap Step-by-Step
        print("\n🗺️  Learning Roadmap:")
        for step in CAREER_ROADMAP[prediction]['roadmap']:
            print(f"   📍 {step['topic']} ({step['duration']})")
            for detail in step['details']:
                print(f"      • {detail}")
        
        return render_template('recommendation.html', profile=student_profile)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return f"Error: {str(e)}", 500


        

@app.route('/roadmap')
def roadmap():
    return render_template('roadmap.html', profile=session.get('profile', {}))

@app.route('/clear')
def clear_session():
    """✅ Clear all session data"""
    session.clear()
    print("\n🧹 Session cleared!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("🚀 Career Guidance System v2.0")
    print("📱 Open: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)