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
from health_assistant_ai import get_health_advice_ai as get_health_advice
from models import db, User, HealthRecord, UserGamification, UserPreferences, Friendship
from missions_manager import (
    create_weekly_missions, get_user_mission_progress, 
    update_mission_progress
)
from challenges_manager import (
    create_seasonal_challenges, get_user_challenge_progress,
    update_challenge_progress, get_current_season
)
from marketplace_manager import (
    initialize_marketplace, get_available_items,
    get_user_purchases, purchase_item
)

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
    initialize_marketplace()
    create_weekly_missions()
    from datetime import timedelta
    season = get_current_season()
    today = date.today()
    season_starts = {
        'winter': date(today.year if today.month == 12 else today.year - 1, 12, 1),
        'spring': date(today.year, 3, 1),
        'summer': date(today.year, 6, 1),
        'fall': date(today.year, 9, 1)
    }
    season_start = season_starts.get(season, today)
    season_end = season_start + timedelta(days=89)
    create_seasonal_challenges(season, season_start, season_end)

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
@login_required
def health_assistant():
    question = request.json.get('question', '')
    advice = get_health_advice(question)
    
    if current_user.is_authenticated:
        update_mission_progress(current_user.id, 'assistant_queries')
        update_challenge_progress(current_user.id, 'assistant_queries')
    
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
        
        # Update health points and XP
        gamification.health_points += 10
        gamification.add_xp(20)
        gamification.total_checks += 1
        
        # Update streak
        today = date.today()
        if gamification.last_check_date == today:
            pass
        elif gamification.last_check_date == date.fromordinal(today.toordinal() - 1):
            gamification.current_streak += 1
            gamification.add_xp(5)
            if gamification.current_streak > gamification.longest_streak:
                gamification.longest_streak = gamification.current_streak
            
            streak_missions = update_mission_progress(current_user.id, 'streak')
            for mission in streak_missions:
                gamification.add_xp(mission.xp_reward)
                gamification.health_points += mission.points_reward
                flash(f'Streak mission completed: {mission.title}!', 'success')
            
            streak_challenges = update_challenge_progress(current_user.id, 'streak')
            for challenge in streak_challenges:
                gamification.add_xp(challenge.xp_reward)
                gamification.health_points += challenge.points_reward
                if challenge.badge_reward:
                    gamification.add_badge(challenge.badge_reward)
                flash(f'Streak challenge completed: {challenge.title}!', 'success')
        else:
            gamification.current_streak = 1
        
        gamification.last_check_date = today
        
        # Award badges and XP bonuses
        if gamification.total_checks == 1:
            gamification.add_badge('First Check')
            gamification.add_xp(50)
        if gamification.total_checks == 5:
            gamification.add_badge('Health Enthusiast')
            gamification.add_xp(100)
        if gamification.total_checks == 10:
            gamification.add_badge('Committed')
            gamification.add_xp(200)
        if gamification.current_streak >= 7:
            gamification.add_badge('Week Warrior')
            gamification.add_xp(150)
        if gamification.current_streak >= 30:
            gamification.add_badge('Monthly Master')
            gamification.add_xp(500)
        
        db.session.commit()
        
        completed_missions = update_mission_progress(current_user.id, 'health_checks')
        for mission in completed_missions:
            gamification.add_xp(mission.xp_reward)
            gamification.health_points += mission.points_reward
            flash(f'Mission completed: {mission.title}! +{mission.xp_reward} XP, +{mission.points_reward} points', 'success')
        
        completed_challenges = update_challenge_progress(current_user.id, 'health_checks')
        for challenge in completed_challenges:
            gamification.add_xp(challenge.xp_reward)
            gamification.health_points += challenge.points_reward
            if challenge.badge_reward:
                gamification.add_badge(challenge.badge_reward)
            flash(f'Challenge completed: {challenge.title}! +{challenge.xp_reward} XP, +{challenge.points_reward} points', 'success')
        
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

@app.route('/missions')
@login_required
def missions():
    mission_progress = get_user_mission_progress(current_user.id)
    return render_template('missions.html', missions=mission_progress)

@app.route('/challenges')
@login_required
def challenges():
    challenge_progress = get_user_challenge_progress(current_user.id)
    return render_template('challenges.html', challenges=challenge_progress)

@app.route('/marketplace')
@login_required
def marketplace():
    gamification = current_user.gamification
    if not gamification:
        gamification = UserGamification(user=current_user)
        db.session.add(gamification)
        db.session.commit()
    
    available_items = get_available_items(gamification.level)
    user_purchases = get_user_purchases(current_user.id)
    purchased_ids = [p.item_id for p in user_purchases]
    
    return render_template('marketplace.html', 
                         items=available_items,
                         purchased_ids=purchased_ids,
                         gamification=gamification)

@app.route('/marketplace/purchase/<int:item_id>', methods=['POST'])
@login_required
def purchase(item_id):
    gamification = current_user.gamification
    success, message = purchase_item(current_user.id, item_id, gamification)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('marketplace'))

@app.route('/leaderboard')
@login_required
def leaderboard():
    top_points = db.session.query(User, UserGamification).join(
        UserGamification, User.id == UserGamification.user_id
    ).order_by(UserGamification.health_points.desc()).limit(10).all()
    
    top_streaks = db.session.query(User, UserGamification).join(
        UserGamification, User.id == UserGamification.user_id
    ).order_by(UserGamification.current_streak.desc()).limit(10).all()
    
    top_checks = db.session.query(User, UserGamification).join(
        UserGamification, User.id == UserGamification.user_id
    ).order_by(UserGamification.total_checks.desc()).limit(10).all()
    
    return render_template('leaderboard.html',
                         top_points=top_points,
                         top_streaks=top_streaks,
                         top_checks=top_checks)

@app.route('/export/csv')
@login_required
def export_csv():
    import csv
    from io import StringIO
    from flask import make_response
    
    records = HealthRecord.query.filter_by(user_id=current_user.id).order_by(HealthRecord.created_at.desc()).all()
    
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Date', 'Glucose', 'Insulin', 'BMI', 'Age', 'BP Systolic', 'BP Diastolic', 'Family History', 'Prediction'])
    
    for record in records:
        writer.writerow([
            record.created_at.strftime('%Y-%m-%d %H:%M'),
            record.glucose,
            record.insulin,
            record.bmi,
            record.age,
            record.bp_systolic,
            record.bp_diastolic,
            'Yes' if record.family_history else 'No',
            'Diabetes' if record.prediction == 1 else 'No Diabetes'
        ])
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=health_records.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/export/pdf')
@login_required
def export_pdf():
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from io import BytesIO
    from flask import make_response
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    elements.append(Paragraph(f"Health Report for {current_user.username}", styles['Title']))
    elements.append(Spacer(1, 0.3*inch))
    
    gamification = current_user.gamification
    if gamification:
        summary_text = f"""
        <b>Health Journey Summary</b><br/>
        Level: {gamification.level} | XP: {gamification.xp}<br/>
        Health Points: {gamification.health_points}<br/>
        Current Streak: {gamification.current_streak} days<br/>
        Total Health Checks: {gamification.total_checks}
        """
        elements.append(Paragraph(summary_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
    
    records = HealthRecord.query.filter_by(user_id=current_user.id).order_by(HealthRecord.created_at.desc()).limit(20).all()
    
    if records:
        data = [['Date', 'Glucose', 'Insulin', 'BMI', 'BP', 'Result']]
        for record in records:
            data.append([
                record.created_at.strftime('%Y-%m-%d'),
                f"{record.glucose}",
                f"{record.insulin}",
                f"{record.bmi}",
                f"{record.bp_systolic}/{record.bp_diastolic}",
                'Diabetes' if record.prediction == 1 else 'Normal'
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
    
    doc.build(elements)
    pdf_data = buffer.getvalue()
    buffer.close()
    
    response = make_response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=health_report.pdf'
    return response

@app.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    user_prefs = UserPreferences.query.filter_by(user_id=current_user.id).first()
    if not user_prefs:
        user_prefs = UserPreferences(user_id=current_user.id)
        db.session.add(user_prefs)
        db.session.commit()
    
    if request.method == 'POST':
        user_prefs.dark_mode = request.form.get('dark_mode') == 'on'
        user_prefs.email_notifications = request.form.get('email_notifications') == 'on'
        user_prefs.share_profile_public = request.form.get('share_profile_public') == 'on'
        db.session.commit()
        flash('Preferences updated successfully!', 'success')
        return redirect(url_for('preferences'))
    
    return render_template('preferences.html', preferences=user_prefs)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
