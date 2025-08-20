from flask import Blueprint, request, jsonify, session
from src.models.user import db, Parent, Student, ParentStudent, Grade, Attendance, BehaviorNote, Tuition, Payment, AIInsight
from src.routes.auth import require_auth, require_role
from datetime import datetime, date
from sqlalchemy import func, and_

parent_bp = Blueprint('parent', __name__)

@parent_bp.route('/dashboard', methods=['GET'])
@require_auth
def get_parent_dashboard():
    try:
        user_id = session['user_id']
        parent = Parent.query.filter_by(user_id=user_id).first()
        
        if not parent:
            return jsonify({'error': 'ملف ولي الأمر غير موجود'}), 404
        
        # Get children
        children_relations = ParentStudent.query.filter_by(parent_id=parent.id).all()
        children_data = []
        
        for relation in children_relations:
            student = relation.student
            
            # Get latest grades
            recent_grades = Grade.query.filter_by(student_id=student.id).order_by(Grade.date_recorded.desc()).limit(5).all()
            
            # Calculate average grade
            all_grades = Grade.query.filter_by(student_id=student.id).all()
            avg_grade = sum(grade.grade for grade in all_grades) / len(all_grades) if all_grades else 0
            
            # Get attendance statistics
            attendance_records = Attendance.query.filter_by(student_id=student.id).all()
            total_days = len(attendance_records)
            present_days = len([a for a in attendance_records if a.status == 'present'])
            attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
            
            # Get recent behavior notes
            recent_behavior = BehaviorNote.query.filter_by(student_id=student.id).order_by(BehaviorNote.date_recorded.desc()).limit(3).all()
            
            # Get tuition information
            current_tuition = Tuition.query.filter_by(student_id=student.id).order_by(Tuition.created_at.desc()).first()
            
            # Get AI insights
            ai_insights = AIInsight.query.filter_by(student_id=student.id, is_active=True).order_by(AIInsight.generated_at.desc()).limit(3).all()
            
            child_data = {
                'student': student.to_dict(),
                'recent_grades': [grade.to_dict() for grade in recent_grades],
                'average_grade': round(avg_grade, 2),
                'attendance': {
                    'total_days': total_days,
                    'present_days': present_days,
                    'percentage': round(attendance_percentage, 2)
                },
                'recent_behavior': [note.to_dict() for note in recent_behavior],
                'tuition': current_tuition.to_dict() if current_tuition else None,
                'ai_insights': [insight.to_dict() for insight in ai_insights]
            }
            children_data.append(child_data)
        
        dashboard_data = {
            'parent': parent.to_dict(),
            'children': children_data,
            'summary': {
                'total_children': len(children_data),
                'children_with_good_attendance': len([c for c in children_data if c['attendance']['percentage'] >= 90]),
                'children_with_high_grades': len([c for c in children_data if c['average_grade'] >= 85])
            }
        }
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@parent_bp.route('/children', methods=['GET'])
@require_auth
def get_children():
    try:
        user_id = session['user_id']
        parent = Parent.query.filter_by(user_id=user_id).first()
        
        if not parent:
            return jsonify({'error': 'ملف ولي الأمر غير موجود'}), 404
        
        children_relations = ParentStudent.query.filter_by(parent_id=parent.id).all()
        children_data = []
        
        for relation in children_relations:
            student = relation.student
            children_data.append(student.to_dict())
        
        return jsonify({'children': children_data}), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@parent_bp.route('/child/<int:student_id>/grades', methods=['GET'])
@require_auth
def get_child_grades(student_id):
    try:
        user_id = session['user_id']
        parent = Parent.query.filter_by(user_id=user_id).first()
        
        if not parent:
            return jsonify({'error': 'ملف ولي الأمر غير موجود'}), 404
        
        # Verify parent has access to this student
        relation = ParentStudent.query.filter_by(parent_id=parent.id, student_id=student_id).first()
        if not relation:
            return jsonify({'error': 'غير مصرح للوصول لبيانات هذا الطالب'}), 403
        
        # Get query parameters
        subject = request.args.get('subject')
        semester = request.args.get('semester')
        grade_type = request.args.get('grade_type')
        
        # Build query
        query = Grade.query.filter_by(student_id=student_id)
        
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
                'trend': 'improving' if len(grade_list) >= 2 and grade_list[0] > grade_list[-1] else 'stable'
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

@parent_bp.route('/child/<int:student_id>/attendance', methods=['GET'])
@require_auth
def get_child_attendance(student_id):
    try:
        user_id = session['user_id']
        parent = Parent.query.filter_by(user_id=user_id).first()
        
        if not parent:
            return jsonify({'error': 'ملف ولي الأمر غير موجود'}), 404
        
        # Verify parent has access to this student
        relation = ParentStudent.query.filter_by(parent_id=parent.id, student_id=student_id).first()
        if not relation:
            return jsonify({'error': 'غير مصرح للوصول لبيانات هذا الطالب'}), 403
        
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build query
        query = Attendance.query.filter_by(student_id=student_id)
        
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
        
        # Get recent absences with details
        recent_absences = [a for a in attendance_records if a.status in ['absent', 'late'] and a.date >= (date.today() - datetime.timedelta(days=30))]
        
        return jsonify({
            'attendance': attendance_data,
            'statistics': {
                'total_days': total_days,
                'present_days': present_days,
                'absent_days': absent_days,
                'late_days': late_days,
                'excused_days': excused_days,
                'attendance_percentage': round(attendance_percentage, 2)
            },
            'recent_absences': [record.to_dict() for record in recent_absences]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@parent_bp.route('/child/<int:student_id>/behavior', methods=['GET'])
@require_auth
def get_child_behavior(student_id):
    try:
        user_id = session['user_id']
        parent = Parent.query.filter_by(user_id=user_id).first()
        
        if not parent:
            return jsonify({'error': 'ملف ولي الأمر غير موجود'}), 404
        
        # Verify parent has access to this student
        relation = ParentStudent.query.filter_by(parent_id=parent.id, student_id=student_id).first()
        if not relation:
            return jsonify({'error': 'غير مصرح للوصول لبيانات هذا الطالب'}), 403
        
        # Get query parameters
        note_type = request.args.get('note_type')
        limit = request.args.get('limit', 50, type=int)
        
        # Build query
        query = BehaviorNote.query.filter_by(student_id=student_id)
        
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
                'neutral_count': neutral_count,
                'positive_ratio': round((positive_count / len(behavior_notes) * 100), 2) if behavior_notes else 0
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@parent_bp.route('/child/<int:student_id>/tuition', methods=['GET'])
@require_auth
def get_child_tuition(student_id):
    try:
        user_id = session['user_id']
        parent = Parent.query.filter_by(user_id=user_id).first()
        
        if not parent:
            return jsonify({'error': 'ملف ولي الأمر غير موجود'}), 404
        
        # Verify parent has access to this student
        relation = ParentStudent.query.filter_by(parent_id=parent.id, student_id=student_id).first()
        if not relation:
            return jsonify({'error': 'غير مصرح للوصول لبيانات هذا الطالب'}), 403
        
        # Get tuition records
        tuition_records = Tuition.query.filter_by(student_id=student_id).order_by(Tuition.created_at.desc()).all()
        tuition_data = [record.to_dict() for record in tuition_records]
        
        # Get payment history
        payments = []
        for tuition in tuition_records:
            tuition_payments = Payment.query.filter_by(tuition_id=tuition.id).order_by(Payment.payment_date.desc()).all()
            for payment in tuition_payments:
                payment_dict = payment.to_dict()
                payment_dict['academic_year'] = tuition.academic_year
                payments.append(payment_dict)
        
        # Calculate totals
        total_amount = sum(record.total_amount for record in tuition_records)
        total_paid = sum(record.paid_amount for record in tuition_records)
        total_remaining = total_amount - total_paid
        
        return jsonify({
            'tuition_records': tuition_data,
            'payment_history': payments,
            'summary': {
                'total_amount': total_amount,
                'total_paid': total_paid,
                'total_remaining': total_remaining,
                'payment_percentage': round((total_paid / total_amount * 100), 2) if total_amount > 0 else 0
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@parent_bp.route('/child/<int:student_id>/ai-report', methods=['GET'])
@require_auth
def generate_ai_report(student_id):
    try:
        user_id = session['user_id']
        parent = Parent.query.filter_by(user_id=user_id).first()
        
        if not parent:
            return jsonify({'error': 'ملف ولي الأمر غير موجود'}), 404
        
        # Verify parent has access to this student
        relation = ParentStudent.query.filter_by(parent_id=parent.id, student_id=student_id).first()
        if not relation:
            return jsonify({'error': 'غير مصرح للوصول لبيانات هذا الطالب'}), 403
        
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'الطالب غير موجود'}), 404
        
        # Get comprehensive data for AI analysis
        grades = Grade.query.filter_by(student_id=student_id).all()
        attendance_records = Attendance.query.filter_by(student_id=student_id).all()
        behavior_notes = BehaviorNote.query.filter_by(student_id=student_id).all()
        
        # Calculate statistics
        avg_grade = sum(grade.grade for grade in grades) / len(grades) if grades else 0
        attendance_percentage = len([a for a in attendance_records if a.status == 'present']) / len(attendance_records) * 100 if attendance_records else 0
        positive_behavior_ratio = len([n for n in behavior_notes if n.note_type == 'positive']) / len(behavior_notes) * 100 if behavior_notes else 0
        
        # Generate AI report (mock implementation)
        ai_report = {
            'student_name': student.user.name,
            'student_id': student.student_id,
            'class_name': student.class_name,
            'report_date': datetime.now().isoformat(),
            'overall_score': round((avg_grade + attendance_percentage + positive_behavior_ratio) / 3, 2),
            'academic_performance': {
                'average_grade': round(avg_grade, 2),
                'trend': 'improving' if avg_grade > 75 else 'needs_attention',
                'strengths': ['الرياضيات', 'الكيمياء'] if avg_grade > 80 else ['يحتاج تحسين'],
                'recommendations': [
                    'زيادة التركيز على المواد الضعيفة',
                    'تطوير مهارات الدراسة',
                    'المشاركة أكثر في الأنشطة'
                ]
            },
            'attendance_analysis': {
                'percentage': round(attendance_percentage, 2),
                'status': 'excellent' if attendance_percentage >= 95 else 'good' if attendance_percentage >= 85 else 'needs_improvement',
                'recommendations': [
                    'الحفاظ على الانتظام' if attendance_percentage >= 90 else 'تحسين الحضور',
                    'تجنب الغياب غير المبرر'
                ]
            },
            'behavior_analysis': {
                'positive_ratio': round(positive_behavior_ratio, 2),
                'emotional_state': 'stable',
                'social_skills': 'good',
                'recommendations': [
                    'تشجيع السلوك الإيجابي',
                    'تطوير المهارات الاجتماعية'
                ]
            },
            'risk_assessment': {
                'level': 'low' if avg_grade > 70 and attendance_percentage > 85 else 'medium',
                'factors': [],
                'interventions': []
            },
            'action_plan': [
                'متابعة دورية مع المعلمين',
                'وضع جدول دراسي منظم',
                'تشجيع الأنشطة اللاصفية'
            ]
        }
        
        return jsonify({'ai_report': ai_report}), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@parent_bp.route('/notifications', methods=['GET'])
@require_auth
def get_parent_notifications():
    try:
        user_id = session['user_id']
        parent = Parent.query.filter_by(user_id=user_id).first()
        
        if not parent:
            return jsonify({'error': 'ملف ولي الأمر غير موجود'}), 404
        
        # Mock notifications - in real implementation, this would come from a notifications table
        notifications = [
            {
                'id': 1,
                'type': 'grade',
                'title': 'درجة جديدة',
                'message': 'تم رفع درجة امتحان الرياضيات',
                'date': datetime.now().isoformat(),
                'read': False,
                'student_id': None  # Will be filled with actual student data
            },
            {
                'id': 2,
                'type': 'attendance',
                'title': 'تنبيه حضور',
                'message': 'غياب اليوم بدون عذر',
                'date': datetime.now().isoformat(),
                'read': False,
                'student_id': None
            },
            {
                'id': 3,
                'type': 'payment',
                'title': 'تذكير دفع',
                'message': 'موعد دفع الرسوم قريب',
                'date': datetime.now().isoformat(),
                'read': True,
                'student_id': None
            }
        ]
        
        return jsonify({'notifications': notifications}), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

