import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    health_records = db.relationship('HealthRecord', backref='user', lazy=True, cascade='all, delete-orphan')
    gamification = db.relationship('UserGamification', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class HealthRecord(db.Model):
    __tablename__ = 'health_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    glucose = db.Column(db.Float, nullable=False)
    insulin = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bp_systolic = db.Column(db.Float, nullable=False)
    bp_diastolic = db.Column(db.Float, nullable=False)
    family_history = db.Column(db.Boolean, default=False)
    prediction = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<HealthRecord {self.id} - User {self.user_id}>'

class UserGamification(db.Model):
    __tablename__ = 'user_gamification'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    health_points = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_check_date = db.Column(db.Date, nullable=True)
    badges = db.Column(db.String(500), default='')
    total_checks = db.Column(db.Integer, default=0)
    
    def add_badge(self, badge_name):
        badges_list = self.badges.split(',') if self.badges else []
        if badge_name not in badges_list:
            badges_list.append(badge_name)
            self.badges = ','.join(badges_list)
    
    def get_badges(self):
        return [b for b in self.badges.split(',') if b] if self.badges else []
    
    def __repr__(self):
        return f'<UserGamification User {self.user_id} - Points: {self.health_points}>'
