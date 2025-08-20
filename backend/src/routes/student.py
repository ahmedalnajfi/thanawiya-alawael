from flask import Blueprint, request, jsonify, session
from src.models.user import db, Student, Grade, Attendance, BehaviorNote, Tuition, AIInsight
from src.routes.auth import require_auth, require_role
from datetime import datetime, date
from sqlalchemy import func, and_

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard', methods=['GET'])
@require_auth
def get_student_dashboard():
    try:
        user_id = session['user_id']
        student = Student.query.filter_by(user_id=user_id).first()
        
        if not student:
            return jsonify({'error': 'ملف الطالب غير موجود'}), 404
        
        # Get grades
        grades = Grade.query.filter_by(student_id=student.id).all()
        grades_data = [grade.to_dict() for grade in grades]
        
        # Calculate average grade
        if grades:
            avg_grade = sum(grade.grade for grade in grades) / len(grades)
        else:
            avg_grade = 0
        
        # Get attendance
        attendance_records = Attendance.query.filter_by(student_id=student.id).all()
        total_days = len(attendance_records)
        present_days = len([a for a in attendance_records if a.status == 'present'])
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        # Get behavior notes
        behavior_notes = BehaviorNote.query.filter_by(student_id=student.id).order_by(BehaviorNote.date_recorded.desc()).limit(10).all()
        behavior_data = [note.to_dict() for note in behavior_notes]
        
        # Get AI insights
        ai_insights = AIInsight.query.filter_by(student_id=student.id, is_active=True).order_by(AIInsight.generated_at.desc()).limit(5).all()
        insights_data = [insight.to_dict() for insight in ai_insights]
        
        dashboard_data = {
            'student': student.to_dict(),
            'grades': grades_data,
            'average_grade': round(avg_grade, 2),
            'attendance': {
                'total_days': total_days,
                'present_days': present_days,
                'absent_days': total_days - present_days,
                'percentage': round(attendance_percentage, 2)
            },
            'behavior_notes': behavior_data,
            'ai_insights': insights_data
        }
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@student_bp.route('/grades', methods=['GET'])
@require_auth
def get_student_grades():
    try:
        user_id = session['user_id']
        student = Student.query.filter_by(user_id=user_id).first()
        
        if not student:
            return jsonify({'error': 'ملف الطالب غير موجود'}), 404
        
        # Get query parameters
        subject = request.args.get('subject')
        semester = request.args.get('semester')
        grade_type = request.args.get('grade_type')
        
        # Build query
        query = Grade.query.filter_by(student_id=student.id)
        
        if subject:
            query = query.filter_by(subject=subject)
        if semester:
            query = query.filter_by(semester=semester)
        if grade_type:
            query = query.filter_by(grade_type=grade_type)
        
        grades = query.order_by(Grade.date_recorded.desc()).all()
        grades_data = [grade.to_dict() for grade in grades]
        
        # Calculate statistics
        if grades:
            avg_grade = sum(grade.grade for grade in grades) / len(grades)
            max_grade = max(grade.grade for grade in grades)
            min_grade = min(grade.grade for grade in grades)
        else:
            avg_grade = max_grade = min_grade = 0
        
        # Group by subject
        subjects_stats = {}
        for grade in grades:
            if grade.subject not in subjects_stats:
                subjects_stats[grade.subject] = []
            subjects_stats[grade.subject].append(grade.grade)
        
        for subject, grade_list in subjects_stats.items():
            subjects_stats[subject] = {
                'average': round(sum(grade_list) / len(grade_list), 2),
                'count': len(grade_list),
                'latest': grade_list[0] if grade_list else 0
            }
        
        return jsonify({
            'grades': grades_data,
            'statistics': {
                'average': round(avg_grade, 2),
                'maximum': max_grade,
                'minimum': min_grade,
                'total_count': len(grades)
            },
            'subjects': subjects_stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@student_bp.route('/attendance', methods=['GET'])
@require_auth
def get_student_attendance():
    try:
        user_id = session['user_id']
        student = Student.query.filter_by(user_id=user_id).first()
        
        if not student:
            return jsonify({'error': 'ملف الطالب غير موجود'}), 404
        
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build query
        query = Attendance.query.filter_by(student_id=student.id)
        
        if start_date:
            query = query.filter(Attendance.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
        if end_date:
            query = query.filter(Attendance.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
        
        attendance_records = query.order_by(Attendance.date.desc()).all()
        attendance_data = [record.to_dict() for record in attendance_records]
        
        # Calculate statistics
        total_days = len(attendance_records)
        present_days = len([a for a in attendance_records if a.status == 'present'])
        absent_days = len([a for a in attendance_records if a.status == 'absent'])
        late_days = len([a for a in attendance_records if a.status == 'late'])
        excused_days = len([a for a in attendance_records if a.status == 'excused'])
        
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        return jsonify({
            'attendance': attendance_data,
            'statistics': {
                'total_days': total_days,
                'present_days': present_days,
                'absent_days': absent_days,
                'late_days': late_days,
                'excused_days': excused_days,
                'attendance_percentage': round(attendance_percentage, 2)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@student_bp.route('/behavior', methods=['GET'])
@require_auth
def get_student_behavior():
    try:
        user_id = session['user_id']
        student = Student.query.filter_by(user_id=user_id).first()
        
        if not student:
            return jsonify({'error': 'ملف الطالب غير موجود'}), 404
        
        # Get query parameters
        note_type = request.args.get('note_type')
        limit = request.args.get('limit', 50, type=int)
        
        # Build query
        query = BehaviorNote.query.filter_by(student_id=student.id)
        
        if note_type:
            query = query.filter_by(note_type=note_type)
        
        behavior_notes = query.order_by(BehaviorNote.date_recorded.desc()).limit(limit).all()
        behavior_data = [note.to_dict() for note in behavior_notes]
        
        # Calculate statistics
        positive_count = len([n for n in behavior_notes if n.note_type == 'positive'])
        negative_count = len([n for n in behavior_notes if n.note_type == 'negative'])
        neutral_count = len([n for n in behavior_notes if n.note_type == 'neutral'])
        
        return jsonify({
            'behavior_notes': behavior_data,
            'statistics': {
                'total_notes': len(behavior_notes),
                'positive_count': positive_count,
                'negative_count': negative_count,
                'neutral_count': neutral_count
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@student_bp.route('/ai-insights', methods=['GET'])
@require_auth
def get_student_ai_insights():
    try:
        user_id = session['user_id']
        student = Student.query.filter_by(user_id=user_id).first()
        
        if not student:
            return jsonify({'error': 'ملف الطالب غير موجود'}), 404
        
        # Get AI insights
        insights = AIInsight.query.filter_by(
            student_id=student.id, 
            is_active=True
        ).order_by(AIInsight.generated_at.desc()).all()
        
        insights_data = [insight.to_dict() for insight in insights]
        
        # Group by insight type
        insights_by_type = {}
        for insight in insights:
            if insight.insight_type not in insights_by_type:
                insights_by_type[insight.insight_type] = []
            insights_by_type[insight.insight_type].append(insight.to_dict())
        
        return jsonify({
            'insights': insights_data,
            'insights_by_type': insights_by_type
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@student_bp.route('/profile', methods=['GET'])
@require_auth
def get_student_profile():
    try:
        user_id = session['user_id']
        student = Student.query.filter_by(user_id=user_id).first()
        
        if not student:
            return jsonify({'error': 'ملف الطالب غير موجود'}), 404
        
        return jsonify({'student': student.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@student_bp.route('/profile', methods=['PUT'])
@require_auth
def update_student_profile():
    try:
        user_id = session['user_id']
        student = Student.query.filter_by(user_id=user_id).first()
        
        if not student:
            return jsonify({'error': 'ملف الطالب غير موجود'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'address' in data:
            student.address = data['address']
        if 'emergency_contact' in data:
            student.emergency_contact = data['emergency_contact']
        
        # Update user information
        if 'phone' in data:
            student.user.phone = data['phone']
        if 'email' in data:
            student.user.email = data['email']
        
        db.session.commit()
        
        return jsonify({
            'message': 'تم تحديث الملف الشخصي بنجاح',
            'student': student.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

