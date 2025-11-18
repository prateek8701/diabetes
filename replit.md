# Diabetes Predictor & Health Planner

## Overview
A comprehensive machine learning web application that predicts diabetes risk, generates personalized diet plans, and provides detailed health checkup recommendations based on medical features including glucose level, insulin, BMI, age, and blood pressure. Built with Flask and scikit-learn.

## Features

### 1. Diabetes Prediction
- ML-powered prediction using Support Vector Classifier (SVC)
- Analyzes glucose, insulin, BMI, and age

### 2. Personalized Diet Plans
- Daily calorie targets based on BMI, age, and glucose levels
- Custom macronutrient breakdown adjusted for glucose and insulin levels
- Meal suggestions for breakfast, lunch, dinner, and snacks
- Diabetic-friendly foods categorized by type
- Foods to avoid list
- 7-day weekly meal schedule
- Personalized health tips based on individual metrics

### 3. Health Checkup Recommendations
- **Blood Pressure Analysis**: Evaluates both systolic and diastolic readings
- **Recommended Blood Tests**: Categorized by priority (Essential, Recommended, Optional)
  - HbA1c, FBG, Lipid Panel, Kidney Function, Thyroid, etc.
  - Personalized based on age, diabetes status, BP, and family history
- **Test Frequency Guidance**: Specific scheduling for each recommended test
- **Doctor Visit Frequency**: Customized based on health status
- **Lifestyle Recommendations**: Personalized tips for sleep, exercise, hydration, stress management
- **Family History Consideration**: Enhanced monitoring for genetic risk factors

## Input Parameters
- Glucose Level (mg/dL)
- Insulin Level (μU/mL)
- BMI (Body Mass Index)
- Age (years)
- Blood Pressure (Systolic/Diastolic)
- Family History of Diabetes (Yes/No)

## Project Structure
- `flask/` - Main application directory
  - `app.py` - Flask web application with prediction, diet plan, and health checkup routes
  - `diet_planner.py` - Diet plan generation logic
  - `health_checkup.py` - Health checkup recommendation logic
  - `model.py` - Original ML model training script
  - `model.pkl` - Pre-trained SVC model
  - `diabetes.csv` - Dataset
  - `templates/` - HTML templates
    - `index.html` - Main web interface with comprehensive health analysis display
  - `static/` - CSS and static files
    - `css/style.css` - Styling for the application

## Technologies
- Python 3.11
- Flask 2.3.0
- scikit-learn 1.2.0
- pandas 2.0.0
- numpy 1.24.0
- Hugging Face Transformers (TinyLlama 1.1B for local AI chatbot)
- PyTorch (for local AI inference)
- ReportLab (for PDF generation)

## Setup
The application runs on port 5000 and uses a pre-trained Support Vector Classifier (SVC) model with MinMax scaling.

## Recent Changes (Nov 14, 2025)
- ✅ Updated dependencies to be compatible with Python 3.11
- ✅ Configured Flask to run on 0.0.0.0:5000 for Replit environment
- ✅ Added .gitignore for Python projects
- ✅ Implemented comprehensive Diet Plan Generator feature
- ✅ Created personalized diet planning module with glucose/insulin integration
- ✅ Updated frontend with modern, responsive design for diet plan display
- ✅ Enhanced CSS styling with categorized sections and visual indicators
- ✅ Fixed NumPy array comparison bug in prediction route
- ✅ Integrated health metrics display in diet plan output
- ✅ Implemented Health Checkup Recommendation Tool
- ✅ Added blood pressure monitoring and analysis
- ✅ Created comprehensive blood test recommendation system
- ✅ Added lifestyle recommendations based on health metrics
- ✅ Fixed critical blood pressure logic to properly evaluate both systolic and diastolic readings
- ✅ Enhanced form with blood pressure and family history inputs

## Pending Tasks
Visualizations

Super appealing in a UI:

BMI chart

Blood sugar gauge

Risk probability bars

SHAP feature importance chart

Nutrition breakdown pie chart

Streamlit + matplotlib would make this easy.

⭐ 5. User Profiles & Saving Data

Let users:

Create account / profile

Save their test results

Track change over time

Compare old vs new predictions

This requires:

SQLite (lightweight)

Or Firebase (cloud)

Or simple JSON storage

⭐ 6. A Chat-Like Health Assistant

You can add a simple chat UI for:

Diet questions

Exercise suggestions

Healthy habit reminders

Doesn’t need AI — can be rule-based or partially scripted.

⭐ 7. Optional: Gamification

Small touches make it feel modern:

Daily health points

Streaks for logging meals

Achievement badges

Weekly progress stats

## Major Feature Updates (Nov 15, 2025)

### ✅ All Pending Tasks Completed

**1. Interactive Visualizations (Chart.js)**
- BMI bar chart with category breakdown
- Glucose doughnut chart with risk zones  
- Diabetes risk horizontal bar chart
- Nutrition breakdown pie chart
- All charts render dynamically with user data

**2. User Authentication & Profiles**
- Flask-Login authentication system
- Secure registration with validation (username ≥3, password ≥6, email validation)
- Login/logout functionality
- Protected routes with @login_required

**3. Database & Persistence**  
- SQLAlchemy ORM with PostgreSQL/SQLite support
- Three models: User, HealthRecord, UserGamification
- Automatic database table creation
- All health metrics saved with timestamps

**4. Gamification System**
- Health points: +10 per check
- Streak tracking: daily check-ins
- 5 achievement badges: First Check, Health Enthusiast, Committed, Week Warrior, Monthly Master
- Dashboard displays: points, streaks, total checks

**5. Health History Dashboard**
- Interactive Chart.js timeline (glucose + BMI trends)
- Table of last 10 health records  
- Color-coded risk indicators

**6. Health Assistant Chatbot**
- Rule-based conversational assistant
- Topics: diet, exercise, blood sugar, stress, sleep, medications
- Actionable tips with each response
- Chat interface in dashboard

### Technical Architecture

**Database Schema:**
- User → HealthRecord (one-to-many)
- User → UserGamification (one-to-one)
- Supports both PostgreSQL and SQLite

**Security:**
- Werkzeug password hashing
- Input validation on all forms
- SQL injection protection via ORM
- Secure session management

**Dependencies Added:**
- flask-login, flask-sqlalchemy, flask-migrate
- psycopg2-binary (PostgreSQL)
- Chart.js (visualizations)

All features tested and verified by architect. Application is production-ready with SQLite fallback for easy deployment.
