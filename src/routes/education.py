from flask import Blueprint, request, jsonify
from src.models.education import db, Subject, Lesson, Exercise, Achievement, UserProgress, UserStats, UserAchievement
from src.models.user import User
from datetime import datetime, timedelta
import json

education_bp = Blueprint('education', __name__)

@education_bp.route('/subjects', methods=['GET'])
def get_subjects():
    """Get all subjects with their lesson counts"""
    subjects = Subject.query.all()
    result = []
    
    for subject in subjects:
        lesson_count = Lesson.query.filter_by(subject_id=subject.id, is_active=True).count()
        result.append({
            'id': subject.id,
            'name': subject.name,
            'name_ar': subject.name_ar,
            'description': subject.description,
            'icon': subject.icon,
            'color': subject.color,
            'lesson_count': lesson_count
        })
    
    return jsonify(result)

@education_bp.route('/subjects/<int:subject_id>/lessons', methods=['GET'])
def get_subject_lessons(subject_id):
    """Get all lessons for a specific subject"""
    lessons = Lesson.query.filter_by(subject_id=subject_id, is_active=True).order_by(Lesson.order_index).all()
    result = []
    
    for lesson in lessons:
        exercise_count = Exercise.query.filter_by(lesson_id=lesson.id).count()
        result.append({
            'id': lesson.id,
            'title': lesson.title,
            'title_ar': lesson.title_ar,
            'description': lesson.description,
            'difficulty_level': lesson.difficulty_level,
            'estimated_duration': lesson.estimated_duration,
            'xp_reward': lesson.xp_reward,
            'exercise_count': exercise_count,
            'order_index': lesson.order_index
        })
    
    return jsonify(result)

@education_bp.route('/lessons/<int:lesson_id>', methods=['GET'])
def get_lesson_details(lesson_id):
    """Get detailed lesson information including exercises"""
    lesson = Lesson.query.get_or_404(lesson_id)
    exercises = Exercise.query.filter_by(lesson_id=lesson_id).order_by(Exercise.order_index).all()
    
    exercise_list = []
    for exercise in exercises:
        exercise_data = {
            'id': exercise.id,
            'question': exercise.question,
            'question_ar': exercise.question_ar,
            'exercise_type': exercise.exercise_type,
            'points': exercise.points,
            'order_index': exercise.order_index
        }
        
        # Include options for multiple choice questions
        if exercise.exercise_type == 'multiple_choice' and exercise.options:
            exercise_data['options'] = exercise.options
        
        exercise_list.append(exercise_data)
    
    return jsonify({
        'id': lesson.id,
        'title': lesson.title,
        'title_ar': lesson.title_ar,
        'description': lesson.description,
        'content': lesson.content,
        'video_url': lesson.video_url,
        'difficulty_level': lesson.difficulty_level,
        'estimated_duration': lesson.estimated_duration,
        'xp_reward': lesson.xp_reward,
        'exercises': exercise_list
    })

@education_bp.route('/user/<int:user_id>/progress', methods=['GET'])
def get_user_progress(user_id):
    """Get user's overall progress across all subjects"""
    user = User.query.get_or_404(user_id)
    user_stats = UserStats.query.filter_by(user_id=user_id).first()
    
    if not user_stats:
        # Create initial stats for new user
        user_stats = UserStats(user_id=user_id)
        db.session.add(user_stats)
        db.session.commit()
    
    # Get progress by subject
    subjects = Subject.query.all()
    subject_progress = []
    
    for subject in subjects:
        lessons = Lesson.query.filter_by(subject_id=subject.id, is_active=True).all()
        total_lessons = len(lessons)
        completed_lessons = 0
        total_progress = 0
        
        for lesson in lessons:
            progress = UserProgress.query.filter_by(user_id=user_id, lesson_id=lesson.id).first()
            if progress:
                if progress.status == 'completed':
                    completed_lessons += 1
                total_progress += progress.progress_percentage
        
        avg_progress = (total_progress / total_lessons) if total_lessons > 0 else 0
        
        subject_progress.append({
            'subject_id': subject.id,
            'name': subject.name,
            'name_ar': subject.name_ar,
            'icon': subject.icon,
            'color': subject.color,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'progress_percentage': round(avg_progress)
        })
    
    # Get recent achievements
    recent_achievements = db.session.query(UserAchievement, Achievement).join(
        Achievement, UserAchievement.achievement_id == Achievement.id
    ).filter(UserAchievement.user_id == user_id).order_by(
        UserAchievement.earned_at.desc()
    ).limit(5).all()
    
    achievement_list = []
    for user_achievement, achievement in recent_achievements:
        achievement_list.append({
            'id': achievement.id,
            'name': achievement.name,
            'name_ar': achievement.name_ar,
            'icon': achievement.icon,
            'earned_at': user_achievement.earned_at.isoformat()
        })
    
    return jsonify({
        'user_stats': {
            'total_xp': user_stats.total_xp,
            'level': user_stats.level,
            'current_streak': user_stats.current_streak,
            'lessons_completed': user_stats.lessons_completed,
            'total_time_spent': user_stats.total_time_spent
        },
        'subject_progress': subject_progress,
        'recent_achievements': achievement_list
    })

@education_bp.route('/user/<int:user_id>/lesson/<int:lesson_id>/progress', methods=['POST'])
def update_lesson_progress(user_id, lesson_id):
    """Update user's progress for a specific lesson"""
    data = request.get_json()
    
    user = User.query.get_or_404(user_id)
    lesson = Lesson.query.get_or_404(lesson_id)
    
    # Get or create progress record
    progress = UserProgress.query.filter_by(user_id=user_id, lesson_id=lesson_id).first()
    if not progress:
        progress = UserProgress(user_id=user_id, lesson_id=lesson_id)
        db.session.add(progress)
    
    # Update progress
    progress.progress_percentage = data.get('progress_percentage', progress.progress_percentage)
    progress.score = data.get('score', progress.score)
    progress.time_spent = data.get('time_spent', progress.time_spent)
    progress.status = data.get('status', progress.status)
    progress.updated_at = datetime.utcnow()
    
    if progress.status == 'completed' and not progress.completed_at:
        progress.completed_at = datetime.utcnow()
        
        # Update user stats
        user_stats = UserStats.query.filter_by(user_id=user_id).first()
        if user_stats:
            user_stats.total_xp += lesson.xp_reward
            user_stats.lessons_completed += 1
            user_stats.level = calculate_level(user_stats.total_xp)
            user_stats.last_activity = datetime.utcnow()
            
            # Update streak
            today = datetime.utcnow().date()
            if user_stats.last_activity and user_stats.last_activity.date() == today - timedelta(days=1):
                user_stats.current_streak += 1
            elif user_stats.last_activity and user_stats.last_activity.date() != today:
                user_stats.current_streak = 1
            else:
                user_stats.current_streak = 1
                
            if user_stats.current_streak > user_stats.longest_streak:
                user_stats.longest_streak = user_stats.current_streak
    
    db.session.commit()
    
    return jsonify({'message': 'Progress updated successfully'})

@education_bp.route('/achievements', methods=['GET'])
def get_achievements():
    """Get all available achievements"""
    achievements = Achievement.query.filter_by(is_active=True).all()
    result = []
    
    for achievement in achievements:
        result.append({
            'id': achievement.id,
            'name': achievement.name,
            'name_ar': achievement.name_ar,
            'description': achievement.description,
            'description_ar': achievement.description_ar,
            'icon': achievement.icon,
            'badge_color': achievement.badge_color,
            'requirement_type': achievement.requirement_type,
            'requirement_value': achievement.requirement_value,
            'xp_reward': achievement.xp_reward
        })
    
    return jsonify(result)

@education_bp.route('/user/<int:user_id>/achievements', methods=['GET'])
def get_user_achievements(user_id):
    """Get user's earned achievements"""
    user_achievements = db.session.query(UserAchievement, Achievement).join(
        Achievement, UserAchievement.achievement_id == Achievement.id
    ).filter(UserAchievement.user_id == user_id).all()
    
    result = []
    for user_achievement, achievement in user_achievements:
        result.append({
            'id': achievement.id,
            'name': achievement.name,
            'name_ar': achievement.name_ar,
            'description': achievement.description,
            'description_ar': achievement.description_ar,
            'icon': achievement.icon,
            'badge_color': achievement.badge_color,
            'earned_at': user_achievement.earned_at.isoformat()
        })
    
    return jsonify(result)

def calculate_level(total_xp):
    """Calculate user level based on total XP"""
    # Simple level calculation: every 100 XP = 1 level
    return max(1, total_xp // 100)

@education_bp.route('/init-sample-data', methods=['POST'])
def init_sample_data():
    """Initialize sample educational data"""
    try:
        # Create subjects
        subjects_data = [
            {'name': 'Reading', 'name_ar': 'القراءة', 'icon': 'BookOpen', 'color': 'bg-blue-500'},
            {'name': 'Mathematics', 'name_ar': 'الرياضيات', 'icon': 'Calculator', 'color': 'bg-green-500'},
            {'name': 'Science', 'name_ar': 'العلوم', 'icon': 'Microscope', 'color': 'bg-purple-500'}
        ]
        
        for subject_data in subjects_data:
            existing = Subject.query.filter_by(name=subject_data['name']).first()
            if not existing:
                subject = Subject(**subject_data)
                db.session.add(subject)
        
        db.session.commit()
        
        # Create sample lessons
        reading_subject = Subject.query.filter_by(name='Reading').first()
        math_subject = Subject.query.filter_by(name='Mathematics').first()
        science_subject = Subject.query.filter_by(name='Science').first()
        
        lessons_data = [
            {
                'title': 'Arabic Letters - Part 1',
                'title_ar': 'الحروف الهجائية - الجزء الأول',
                'description': 'Learn the first set of Arabic letters',
                'subject_id': reading_subject.id,
                'difficulty_level': 1,
                'estimated_duration': 15,
                'xp_reward': 20,
                'order_index': 1
            },
            {
                'title': 'Arabic Letters - Part 2',
                'title_ar': 'الحروف الهجائية - الجزء الثاني',
                'description': 'Learn more Arabic letters',
                'subject_id': reading_subject.id,
                'difficulty_level': 1,
                'estimated_duration': 15,
                'xp_reward': 20,
                'order_index': 2
            },
            {
                'title': 'Numbers 1-10',
                'title_ar': 'الأرقام من 1 إلى 10',
                'description': 'Learn to count from 1 to 10',
                'subject_id': math_subject.id,
                'difficulty_level': 1,
                'estimated_duration': 10,
                'xp_reward': 15,
                'order_index': 1
            },
            {
                'title': 'Basic Addition',
                'title_ar': 'الجمع البسيط',
                'description': 'Learn basic addition',
                'subject_id': math_subject.id,
                'difficulty_level': 2,
                'estimated_duration': 20,
                'xp_reward': 25,
                'order_index': 2
            },
            {
                'title': 'Water Cycle',
                'title_ar': 'دورة الماء في الطبيعة',
                'description': 'Learn about the water cycle',
                'subject_id': science_subject.id,
                'difficulty_level': 2,
                'estimated_duration': 25,
                'xp_reward': 30,
                'order_index': 1
            }
        ]
        
        for lesson_data in lessons_data:
            existing = Lesson.query.filter_by(title=lesson_data['title']).first()
            if not existing:
                lesson = Lesson(**lesson_data)
                db.session.add(lesson)
        
        db.session.commit()
        
        # Create sample achievements
        achievements_data = [
            {
                'name': 'First Steps',
                'name_ar': 'الخطوات الأولى',
                'description': 'Complete your first lesson',
                'description_ar': 'أكمل درسك الأول',
                'icon': '🎯',
                'badge_color': 'yellow',
                'requirement_type': 'lessons_completed',
                'requirement_value': 1,
                'xp_reward': 50
            },
            {
                'name': 'Reading Master',
                'name_ar': 'قارئ ماهر',
                'description': 'Complete 5 reading lessons',
                'description_ar': 'أكمل 5 دروس في القراءة',
                'icon': '📚',
                'badge_color': 'blue',
                'requirement_type': 'subject_lessons',
                'requirement_value': 5,
                'xp_reward': 100
            },
            {
                'name': 'Math Genius',
                'name_ar': 'عبقري الرياضيات',
                'description': 'Complete 5 math lessons',
                'description_ar': 'أكمل 5 دروس في الرياضيات',
                'icon': '🔢',
                'badge_color': 'green',
                'requirement_type': 'subject_lessons',
                'requirement_value': 5,
                'xp_reward': 100
            },
            {
                'name': 'Persistent Learner',
                'name_ar': 'متعلم مثابر',
                'description': 'Maintain a 7-day learning streak',
                'description_ar': 'حافظ على سلسلة تعلم لمدة 7 أيام',
                'icon': '⭐',
                'badge_color': 'purple',
                'requirement_type': 'streak_days',
                'requirement_value': 7,
                'xp_reward': 200
            }
        ]
        
        for achievement_data in achievements_data:
            existing = Achievement.query.filter_by(name=achievement_data['name']).first()
            if not existing:
                achievement = Achievement(**achievement_data)
                db.session.add(achievement)
        
        db.session.commit()
        
        return jsonify({'message': 'Sample data initialized successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
