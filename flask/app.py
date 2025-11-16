import os
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
import pickle
from datetime import datetime, date
from diet_planner import generate_diet_plan
from health_checkup import generate_health_checkup_plan
from health_assistant import get_health_advice
from models import db, User, HealthRecord, UserGamification

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "dev-secret-key-change-in-production"

database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url or "sqlite:///health_tracker.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

model = pickle.load(open('model.pkl', 'rb'))

dataset = pd.read_csv('diabetes.csv')

dataset_X = dataset.iloc[:,[1, 2, 5, 7]].values

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0,1))
dataset_scaled = sc.fit_transform(dataset_X)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Validate inputs
        if not username or len(username) < 3:
            flash('Username must be at least 3 characters long', 'error')
            return render_template('register.html')
        
        if not email or '@' not in email:
            flash('Please enter a valid email address', 'error')
            return render_template('register.html')
        
        if not password or len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        
        gamification = UserGamification(user=user)
        db.session.add(gamification)
        
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    records_query = HealthRecord.query.filter_by(user_id=current_user.id).order_by(HealthRecord.created_at.desc()).all()
    
    # Convert SQLAlchemy objects to dictionaries for JSON serialization
    records = []
    for record in records_query:
        records.append({
            'id': record.id,
            'glucose': record.glucose,
            'insulin': record.insulin,
            'bmi': record.bmi,
            'age': record.age,
            'bp_systolic': record.bp_systolic,
            'bp_diastolic': record.bp_diastolic,
            'family_history': record.family_history,
            'prediction': record.prediction,
            'created_at': record.created_at.isoformat()
        })
    
    gamification = current_user.gamification
    if not gamification:
        gamification = UserGamification(user=current_user)
        db.session.add(gamification)
        db.session.commit()
    
    return render_template('dashboard.html', records=records, gamification=gamification)

@app.route('/health-assistant', methods=['POST'])
def health_assistant():
    question = request.json.get('question', '')
    advice = get_health_advice(question)
    return jsonify(advice)

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    # Extract form values
    glucose = float(request.form.get('Glucose Level'))
    insulin = float(request.form.get('Insulin'))
    bmi = float(request.form.get('BMI'))
    age = float(request.form.get('Age'))
    bp_systolic = float(request.form.get('Blood Pressure Systolic'))
    bp_diastolic = float(request.form.get('Blood Pressure Diastolic'))
    family_history = request.form.get('Family History') == 'yes'
    
    # Prepare features for ML model (original 4 features)
    float_features = [glucose, insulin, bmi, age]
    final_features = [np.array(float_features)]
    prediction = model.predict( sc.transform(final_features) )
    
    pred_value = int(prediction[0])
    
    if pred_value == 1:
        pred = "You have Diabetes, please consult a Doctor."
    else:
        pred = "You don't have Diabetes."
    output = pred
    
    # Save health record if user is logged in
    if current_user.is_authenticated:
        record = HealthRecord(
            user_id=current_user.id,
            glucose=glucose,
            insulin=insulin,
            bmi=bmi,
            age=int(age),
            bp_systolic=bp_systolic,
            bp_diastolic=bp_diastolic,
            family_history=family_history,
            prediction=pred_value
        )
        db.session.add(record)
        
        # Update gamification
        gamification = current_user.gamification
        if not gamification:
            gamification = UserGamification(user=current_user)
            db.session.add(gamification)
        
        # Update health points
        gamification.health_points += 10
        gamification.total_checks += 1
        
        # Update streak
        today = date.today()
        if gamification.last_check_date == today:
            pass
        elif gamification.last_check_date == date.fromordinal(today.toordinal() - 1):
            gamification.current_streak += 1
            if gamification.current_streak > gamification.longest_streak:
                gamification.longest_streak = gamification.current_streak
        else:
            gamification.current_streak = 1
        
        gamification.last_check_date = today
        
        # Award badges
        if gamification.total_checks == 1:
            gamification.add_badge('First Check')
        if gamification.total_checks == 5:
            gamification.add_badge('Health Enthusiast')
        if gamification.total_checks == 10:
            gamification.add_badge('Committed')
        if gamification.current_streak >= 7:
            gamification.add_badge('Week Warrior')
        if gamification.current_streak >= 30:
            gamification.add_badge('Monthly Master')
        
        db.session.commit()
        flash('Health record saved successfully!', 'success')
    
    # Generate diet plan
    diet_plan = generate_diet_plan(glucose, insulin, bmi, age, pred_value)
    
    # Generate health checkup plan
    checkup_plan = generate_health_checkup_plan(
        age, bmi, glucose, bp_systolic, bp_diastolic, 
        pred_value, family_history
    )
    
    # Prepare chart data for visualizations
    chart_data = {
        'bmi': bmi,
        'glucose': glucose,
        'risk': pred_value,
        'nutrition': {
            'carbs': 45,
            'protein': 30,
            'fats': 25
        }
    }

    return render_template('index.html', 
                         prediction_text='{}'.format(output), 
                         diet_plan=diet_plan,
                         checkup_plan=checkup_plan,
                         chart_data=chart_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
