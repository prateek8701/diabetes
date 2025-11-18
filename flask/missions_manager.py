from datetime import datetime, date, timedelta
from models import db, WeeklyMission, UserMissionProgress

def get_current_week_start():
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    return week_start

def get_current_week_end():
    return get_current_week_start() + timedelta(days=6)

def create_weekly_missions():
    week_start = get_current_week_start()
    week_end = get_current_week_end()
    
    existing = WeeklyMission.query.filter_by(week_start=week_start).first()
    if existing:
        return
    
    missions_data = [
        {
            'title': 'Health Check Streak',
            'description': 'Complete 3 health checks this week',
            'mission_type': 'health_checks',
            'target_value': 3,
            'xp_reward': 150,
            'points_reward': 50
        },
        {
            'title': 'Consistency Master',
            'description': 'Log health data 5 days in a row',
            'mission_type': 'streak',
            'target_value': 5,
            'xp_reward': 200,
            'points_reward': 75
        },
        {
            'title': 'Health Explorer',
            'description': 'Ask the health assistant 5 questions',
            'mission_type': 'assistant_queries',
            'target_value': 5,
            'xp_reward': 100,
            'points_reward': 30
        }
    ]
    
    for mission_data in missions_data:
        mission = WeeklyMission(
            title=mission_data['title'],
            description=mission_data['description'],
            mission_type=mission_data['mission_type'],
            target_value=mission_data['target_value'],
            xp_reward=mission_data['xp_reward'],
            points_reward=mission_data['points_reward'],
            week_start=week_start,
            week_end=week_end
        )
        db.session.add(mission)
    
    db.session.commit()

def get_active_missions():
    week_start = get_current_week_start()
    week_end = get_current_week_end()
    return WeeklyMission.query.filter(
        WeeklyMission.week_start == week_start,
        WeeklyMission.week_end == week_end,
        WeeklyMission.is_active == True
    ).all()

def get_user_mission_progress(user_id):
    active_missions = get_active_missions()
    progress_list = []
    
    for mission in active_missions:
        progress = UserMissionProgress.query.filter_by(
            user_id=user_id,
            mission_id=mission.id
        ).first()
        
        if not progress:
            progress = UserMissionProgress(
                user_id=user_id,
                mission_id=mission.id,
                current_progress=0
            )
            db.session.add(progress)
            db.session.commit()
        
        progress_list.append({
            'mission': mission,
            'progress': progress,
            'percentage': min(100, int((progress.current_progress / mission.target_value) * 100))
        })
    
    return progress_list

def update_mission_progress(user_id, mission_type, increment=1):
    active_missions = WeeklyMission.query.filter_by(
        mission_type=mission_type,
        week_start=get_current_week_start(),
        is_active=True
    ).all()
    
    completed_missions = []
    
    for mission in active_missions:
        progress = UserMissionProgress.query.filter_by(
            user_id=user_id,
            mission_id=mission.id
        ).first()
        
        if not progress:
            progress = UserMissionProgress(
                user_id=user_id,
                mission_id=mission.id,
                current_progress=0
            )
            db.session.add(progress)
        
        if not progress.completed:
            progress.current_progress += increment
            
            if progress.current_progress >= mission.target_value:
                progress.completed = True
                progress.completed_at = datetime.utcnow()
                completed_missions.append(mission)
    
    db.session.commit()
    return completed_missions
