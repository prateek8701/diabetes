from datetime import datetime, date, timedelta
from models import db, SeasonalChallenge, UserChallengeProgress

def get_current_season():
    month = date.today().month
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'fall'

def create_seasonal_challenges(season, start_date, end_date):
    existing = SeasonalChallenge.query.filter_by(season=season, start_date=start_date).first()
    if existing:
        return
    
    challenges_data = {
        'winter': [
            {
                'title': 'Winter Wellness Warrior',
                'description': 'Complete 20 health checks during winter',
                'challenge_type': 'health_checks',
                'target_value': 20,
                'xp_reward': 1000,
                'points_reward': 500,
                'badge_reward': 'Winter Warrior'
            },
            {
                'title': 'New Year Health Champion',
                'description': 'Maintain a 30-day streak',
                'challenge_type': 'streak',
                'target_value': 30,
                'xp_reward': 2000,
                'points_reward': 1000,
                'badge_reward': 'New Year Champion'
            }
        ],
        'spring': [
            {
                'title': 'Spring Renewal',
                'description': 'Complete 25 health checks this spring',
                'challenge_type': 'health_checks',
                'target_value': 25,
                'xp_reward': 1200,
                'points_reward': 600,
                'badge_reward': 'Spring Renewal'
            }
        ],
        'summer': [
            {
                'title': 'Summer Fitness Challenge',
                'description': 'Complete 30 health checks this summer',
                'challenge_type': 'health_checks',
                'target_value': 30,
                'xp_reward': 1500,
                'points_reward': 750,
                'badge_reward': 'Summer Star'
            }
        ],
        'fall': [
            {
                'title': 'Fall Harvest Health',
                'description': 'Complete 25 health checks this fall',
                'challenge_type': 'health_checks',
                'target_value': 25,
                'xp_reward': 1200,
                'points_reward': 600,
                'badge_reward': 'Harvest Hero'
            }
        ]
    }
    
    for challenge_data in challenges_data.get(season, []):
        challenge = SeasonalChallenge(
            title=challenge_data['title'],
            description=challenge_data['description'],
            season=season,
            challenge_type=challenge_data['challenge_type'],
            target_value=challenge_data['target_value'],
            xp_reward=challenge_data['xp_reward'],
            points_reward=challenge_data['points_reward'],
            badge_reward=challenge_data.get('badge_reward'),
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(challenge)
    
    db.session.commit()

def get_active_challenges():
    today = date.today()
    return SeasonalChallenge.query.filter(
        SeasonalChallenge.start_date <= today,
        SeasonalChallenge.end_date >= today,
        SeasonalChallenge.is_active == True
    ).all()

def get_user_challenge_progress(user_id):
    active_challenges = get_active_challenges()
    progress_list = []
    
    for challenge in active_challenges:
        progress = UserChallengeProgress.query.filter_by(
            user_id=user_id,
            challenge_id=challenge.id
        ).first()
        
        if not progress:
            progress = UserChallengeProgress(
                user_id=user_id,
                challenge_id=challenge.id,
                current_progress=0
            )
            db.session.add(progress)
            db.session.commit()
        
        progress_list.append({
            'challenge': challenge,
            'progress': progress,
            'percentage': min(100, int((progress.current_progress / challenge.target_value) * 100))
        })
    
    return progress_list

def update_challenge_progress(user_id, challenge_type, increment=1):
    active_challenges = SeasonalChallenge.query.filter_by(
        challenge_type=challenge_type,
        is_active=True
    ).filter(
        SeasonalChallenge.start_date <= date.today(),
        SeasonalChallenge.end_date >= date.today()
    ).all()
    
    completed_challenges = []
    
    for challenge in active_challenges:
        progress = UserChallengeProgress.query.filter_by(
            user_id=user_id,
            challenge_id=challenge.id
        ).first()
        
        if not progress:
            progress = UserChallengeProgress(
                user_id=user_id,
                challenge_id=challenge.id,
                current_progress=0
            )
            db.session.add(progress)
        
        if not progress.completed:
            progress.current_progress += increment
            
            if progress.current_progress >= challenge.target_value:
                progress.completed = True
                progress.completed_at = datetime.utcnow()
                completed_challenges.append(challenge)
    
    db.session.commit()
    return completed_challenges
