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
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_check_date = db.Column(db.Date, nullable=True)
    badges = db.Column(db.String(500), default='')
    total_checks = db.Column(db.Integer, default=0)
    selected_theme = db.Column(db.String(50), default='default')
    
    def add_badge(self, badge_name):
        badges_list = self.badges.split(',') if self.badges else []
        if badge_name not in badges_list:
            badges_list.append(badge_name)
            self.badges = ','.join(badges_list)
    
    def get_badges(self):
        return [b for b in self.badges.split(',') if b] if self.badges else []
    
    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_for_next_level():
            self.xp -= self.xp_for_next_level()
            self.level += 1
    
    def xp_for_next_level(self):
        return 100 * self.level
    
    def xp_progress_percent(self):
        return int((self.xp / self.xp_for_next_level()) * 100)
    
    def __repr__(self):
        return f'<UserGamification User {self.user_id} - Points: {self.health_points}>'

class WeeklyMission(db.Model):
    __tablename__ = 'weekly_missions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    mission_type = db.Column(db.String(50), nullable=False)
    target_value = db.Column(db.Integer, nullable=False)
    xp_reward = db.Column(db.Integer, nullable=False)
    points_reward = db.Column(db.Integer, nullable=False)
    week_start = db.Column(db.Date, nullable=False)
    week_end = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<WeeklyMission {self.title}>'

class UserMissionProgress(db.Model):
    __tablename__ = 'user_mission_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mission_id = db.Column(db.Integer, db.ForeignKey('weekly_missions.id'), nullable=False)
    current_progress = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    mission = db.relationship('WeeklyMission', backref='user_progress')
    
    def __repr__(self):
        return f'<UserMissionProgress User {self.user_id} Mission {self.mission_id}>'

class SeasonalChallenge(db.Model):
    __tablename__ = 'seasonal_challenges'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    season = db.Column(db.String(50), nullable=False)
    challenge_type = db.Column(db.String(50), nullable=False)
    target_value = db.Column(db.Integer, nullable=False)
    xp_reward = db.Column(db.Integer, nullable=False)
    points_reward = db.Column(db.Integer, nullable=False)
    badge_reward = db.Column(db.String(100), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<SeasonalChallenge {self.title}>'

class UserChallengeProgress(db.Model):
    __tablename__ = 'user_challenge_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('seasonal_challenges.id'), nullable=False)
    current_progress = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    challenge = db.relationship('SeasonalChallenge', backref='user_progress')
    
    def __repr__(self):
        return f'<UserChallengeProgress User {self.user_id} Challenge {self.challenge_id}>'

class MarketplaceItem(db.Model):
    __tablename__ = 'marketplace_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    item_type = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    theme_data = db.Column(db.String(1000), nullable=True)
    icon = db.Column(db.String(100), nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    required_level = db.Column(db.Integer, default=1)
    
    def __repr__(self):
        return f'<MarketplaceItem {self.name}>'

class UserPurchase(db.Model):
    __tablename__ = 'user_purchases'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('marketplace_items.id'), nullable=False)
    purchased_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    item = db.relationship('MarketplaceItem', backref='purchases')
    
    def __repr__(self):
        return f'<UserPurchase User {self.user_id} Item {self.item_id}>'

class Friendship(db.Model):
    __tablename__ = 'friendships'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_at = db.Column(db.DateTime, nullable=True)
    
    user = db.relationship('User', foreign_keys=[user_id], backref='friendships_sent')
    friend = db.relationship('User', foreign_keys=[friend_id], backref='friendships_received')
    
    def __repr__(self):
        return f'<Friendship {self.user_id} -> {self.friend_id} ({self.status})>'

class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    dark_mode = db.Column(db.Boolean, default=False)
    email_notifications = db.Column(db.Boolean, default=True)
    share_profile_public = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref='preferences', uselist=False)
    
    def __repr__(self):
        return f'<UserPreferences User {self.user_id}>'
