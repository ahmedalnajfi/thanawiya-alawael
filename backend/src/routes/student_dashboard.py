"""
API endpoints for student dashboard functionality
Student Dashboard Routes - مسارات لوحة تحكم الطالب
"""
import json
from flask import Blueprint, request, jsonify, session
from sqlalchemy.orm import joinedload
from sqlalchemy import and_, or_, func
from datetime import datetime, date, timedelta
from src import db
from src.models.user import User, Student, Teacher
from src.models.extended_models import (
    Course, Assignment, AttendanceRecord, StudentGrade, 
    AcademicYear, Classroom, Subject, Enrollment
)
from src.models.student_dashboard import (
    Exam, ClassSchedule, SchoolDay, AssignmentSubmission, 
    StudentDashboardSettings
)

student_dashboard = Blueprint('student_dashboard', __name__)

def require_student_auth():
    """التحقق من أن المستخدم طالب مسجل دخول"""
    if 'user_id' not in session or session.get('user_role') != 'student':
        return {'error': 'Authentication required'}, 401
    return None

def get_current_student():
    """الحصول على بيانات الطالب الحالي"""
    auth_error = require_student_auth()
    if auth_error:
        return None, auth_error
    
    student = db.session.query(Student).filter(
        Student.user_id == session['user_id']
    ).first()
    
    if not student:
        return None, ({'error': 'Student profile not found'}, 404)
    
    return student, None

@student_dashboard.route('/dashboard/overview', methods=['GET'])
def get_dashboard_overview():
    """الحصول على نظرة عامة للوحة تحكم الطالب"""
    student, error = get_current_student()
    if error:
        return jsonify(error[0]), error[1]
    
    # الحصول على الفصل المسجل فيه الطالب
    enrollment = db.session.query(Enrollment).filter(
        and_(
            Enrollment.student_id == student.id,
            Enrollment.status == 'active'
        )
    ).first()
    
    if not enrollment:
        return jsonify({'error': 'Student not enrolled in any class'}), 404
    
    classroom = enrollment.classroom
    
    # إحصائيات سريعة
    today = date.today()
    
    # الامتحانات القادمة
    upcoming_exams_count = db.session.query(func.count(Exam.id)).filter(
        and_(
            Exam.classroom_id == classroom.id,
            Exam.exam_date >= today,
            Exam.is_published == True,
            Exam.is_active == True
        )
    ).scalar()
    
    # الواجبات المعلقة
    pending_assignments = db.session.query(Assignment).join(Course).filter(
        and_(
            Course.classroom_id == classroom.id,
            Assignment.is_active == True,
            Assignment.due_date >= datetime.now(),
            ~Assignment.id.in_(
                db.session.query(AssignmentSubmission.assignment_id).filter(
                    AssignmentSubmission.student_id == student.id
                )
            )
        )
    ).count()
    
    # نسبة الحضور (آخر شهر)
    last_month = today - timedelta(days=30)
    total_attendance = db.session.query(func.count(AttendanceRecord.id)).filter(
        and_(
            AttendanceRecord.student_id == student.id,
            AttendanceRecord.attendance_date >= last_month
        )
    ).scalar()
    
    present_count = db.session.query(func.count(AttendanceRecord.id)).filter(
        and_(
            AttendanceRecord.student_id == student.id,
            AttendanceRecord.attendance_date >= last_month,
            AttendanceRecord.status == 'present'
        )
    ).scalar()
    
    attendance_rate = (present_count / total_attendance * 100) if total_attendance > 0 else 0
    
    # آخر الدرجات
    recent_grades = db.session.query(StudentGrade).filter(
        and_(
            StudentGrade.student_id == student.id,
            StudentGrade.is_published == True
        )
    ).order_by(StudentGrade.recorded_at.desc()).limit(5).all()
    
    return jsonify({
        'student_info': student.to_dict(),
        'classroom': classroom.to_dict(),
        'overview': {
            'upcoming_exams_count': upcoming_exams_count,
            'pending_assignments_count': pending_assignments,
            'attendance_rate': round(attendance_rate, 1),
            'recent_grades_count': len(recent_grades)
        },
        'recent_grades': [grade.to_dict() for grade in recent_grades]
    })

@student_dashboard.route('/dashboard/assignments', methods=['GET'])
def get_student_assignments():
    """الحصول على قائمة الواجبات للطالب"""
    student, error = get_current_student()
    if error:
        return jsonify(error[0]), error[1]
    
    # الحصول على الفصل
    enrollment = db.session.query(Enrollment).filter(
        and_(
            Enrollment.student_id == student.id,
            Enrollment.status == 'active'
        )
    ).first()
    
    if not enrollment:
        return jsonify({'error': 'Student not enrolled in any class'}), 404
    
    # الحصول على الواجبات مع حالة التسليم
    assignments_query = db.session.query(Assignment).join(Course).filter(
        and_(
            Course.classroom_id == enrollment.classroom_id,
            Assignment.is_active == True
        )
    ).order_by(Assignment.due_date.desc())
    
    status_filter = request.args.get('status', 'all')
    
    if status_filter == 'pending':
        # الواجبات المعلقة
        submitted_assignment_ids = db.session.query(AssignmentSubmission.assignment_id).filter(
            AssignmentSubmission.student_id == student.id
        ).subquery()
        
        assignments_query = assignments_query.filter(
            ~Assignment.id.in_(submitted_assignment_ids)
        )
    elif status_filter == 'submitted':
        # الواجبات المسلمة
        submitted_assignment_ids = db.session.query(AssignmentSubmission.assignment_id).filter(
            AssignmentSubmission.student_id == student.id
        ).subquery()
        
        assignments_query = assignments_query.filter(
            Assignment.id.in_(submitted_assignment_ids)
        )
    
    assignments = assignments_query.all()
    
    # إضافة معلومات التسليم لكل واجب
    assignments_data = []
    for assignment in assignments:
        assignment_dict = assignment.to_dict()
        
        # البحث عن التسليم
        submission = db.session.query(AssignmentSubmission).filter(
            and_(
                AssignmentSubmission.assignment_id == assignment.id,
                AssignmentSubmission.student_id == student.id
            )
        ).first()
        
        assignment_dict['submission'] = submission.to_dict() if submission else None
        assignment_dict['is_submitted'] = submission is not None
        assignment_dict['is_overdue'] = (
            assignment.due_date < datetime.now() if assignment.due_date else False
        )
        
        assignments_data.append(assignment_dict)
    
    return jsonify({
        'assignments': assignments_data,
        'total_count': len(assignments_data)
    })

@student_dashboard.route('/dashboard/exams', methods=['GET'])
def get_student_exams():
    """الحصول على قائمة الامتحانات للطالب"""
    student, error = get_current_student()
    if error:
        return jsonify(error[0]), error[1]
    
    # الحصول على الفصل
    enrollment = db.session.query(Enrollment).filter(
        and_(
            Enrollment.student_id == student.id,
            Enrollment.status == 'active'
        )
    ).first()
    
    if not enrollment:
        return jsonify({'error': 'Student not enrolled in any class'}), 404
    
    # تصفية الامتحانات
    exams_query = db.session.query(Exam).filter(
        and_(
            Exam.classroom_id == enrollment.classroom_id,
            Exam.is_published == True,
            Exam.is_active == True
        )
    )
    
    filter_type = request.args.get('filter', 'all')
    today = date.today()
    
    if filter_type == 'upcoming':
        exams_query = exams_query.filter(Exam.exam_date >= today)
    elif filter_type == 'past':
        exams_query = exams_query.filter(Exam.exam_date < today)
    elif filter_type == 'this_week':
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        exams_query = exams_query.filter(
            and_(
                Exam.exam_date >= week_start,
                Exam.exam_date <= week_end
            )
        )
    
    exams = exams_query.order_by(Exam.exam_date.asc(), Exam.start_time.asc()).all()
    
    return jsonify({
        'exams': [exam.to_dict() for exam in exams],
        'total_count': len(exams)
    })

@student_dashboard.route('/dashboard/schedule', methods=['GET'])
def get_student_schedule():
    """الحصول على جدول الحصص للطالب"""
    student, error = get_current_student()
    if error:
        return jsonify(error[0]), error[1]
    
    # الحصول على الفصل
    enrollment = db.session.query(Enrollment).filter(
        and_(
            Enrollment.student_id == student.id,
            Enrollment.status == 'active'
        )
    ).first()
    
    if not enrollment:
        return jsonify({'error': 'Student not enrolled in any class'}), 404
    
    # الحصول على جدول الحصص
    schedule = db.session.query(ClassSchedule).filter(
        and_(
            ClassSchedule.classroom_id == enrollment.classroom_id,
            ClassSchedule.is_active == True
        )
    ).order_by(
        ClassSchedule.day_of_week.asc(),
        ClassSchedule.period_number.asc()
    ).all()
    
    # تنظيم الجدول حسب الأيام
    schedule_by_day = {}
    for item in schedule:
        day_name = item.day_name
        if day_name not in schedule_by_day:
            schedule_by_day[day_name] = []
        schedule_by_day[day_name].append(item.to_dict())
    
    # معلومات الدوام المدرسي
    today_info = db.session.query(SchoolDay).filter(
        SchoolDay.date == date.today()
    ).first()
    
    return jsonify({
        'schedule': schedule_by_day,
        'today_info': today_info.to_dict() if today_info else None,
        'total_periods': len(schedule)
    })

@student_dashboard.route('/dashboard/grades', methods=['GET'])
def get_student_grades():
    """الحصول على درجات الطالب"""
    student, error = get_current_student()
    if error:
        return jsonify(error[0]), error[1]
    
    # الحصول على الدرجات المنشورة فقط
    grades_query = db.session.query(StudentGrade).options(
        joinedload(StudentGrade.grade_system).joinedload('course').joinedload('subject')
    ).filter(
        and_(
            StudentGrade.student_id == student.id,
            StudentGrade.is_published == True
        )
    )
    
    # تصفية حسب المادة
    subject_filter = request.args.get('subject')
    if subject_filter:
        grades_query = grades_query.join(
            StudentGrade.grade_system
        ).join(
            'course'
        ).join(
            'subject'
        ).filter(Subject.code == subject_filter)
    
    # تصفية حسب نوع الدرجة
    grade_type = request.args.get('type')
    if grade_type:
        grades_query = grades_query.join(StudentGrade.grade_system).filter(
            'grade_systems.grade_type' == grade_type
        )
    
    grades = grades_query.order_by(
        StudentGrade.recorded_date.desc()
    ).all()
    
    # حساب الإحصائيات
    if grades:
        total_grades = len(grades)
        average_percentage = sum(grade.percentage for grade in grades) / total_grades
        highest_grade = max(grades, key=lambda g: g.percentage)
        lowest_grade = min(grades, key=lambda g: g.percentage)
        
        # تجميع الدرجات حسب المادة
        subjects_stats = {}
        for grade in grades:
            subject_name = grade.grade_system.course.subject.name
            if subject_name not in subjects_stats:
                subjects_stats[subject_name] = {
                    'grades': [],
                    'total': 0,
                    'count': 0
                }
            subjects_stats[subject_name]['grades'].append(grade.to_dict())
            subjects_stats[subject_name]['total'] += grade.percentage
            subjects_stats[subject_name]['count'] += 1
        
        # حساب متوسط كل مادة
        for subject in subjects_stats:
            subjects_stats[subject]['average'] = (
                subjects_stats[subject]['total'] / subjects_stats[subject]['count']
            )
    else:
        total_grades = 0
        average_percentage = 0
        highest_grade = None
        lowest_grade = None
        subjects_stats = {}
    
    return jsonify({
        'grades': [grade.to_dict() for grade in grades],
        'statistics': {
            'total_grades': total_grades,
            'average_percentage': round(average_percentage, 2) if total_grades > 0 else 0,
            'highest_grade': highest_grade.to_dict() if highest_grade else None,
            'lowest_grade': lowest_grade.to_dict() if lowest_grade else None
        },
        'subjects_stats': subjects_stats
    })

@student_dashboard.route('/dashboard/attendance', methods=['GET'])
def get_student_attendance():
    """الحصول على سجل حضور الطالب"""
    student, error = get_current_student()
    if error:
        return jsonify(error[0]), error[1]
    
    # تحديد الفترة الزمنية
    days_back = int(request.args.get('days', 30))
    start_date = date.today() - timedelta(days=days_back)
    
    # الحصول على سجلات الحضور
    attendance_records = db.session.query(AttendanceRecord).filter(
        and_(
            AttendanceRecord.student_id == student.id,
            AttendanceRecord.attendance_date >= start_date
        )
    ).order_by(AttendanceRecord.attendance_date.desc()).all()
    
    # حساب الإحصائيات
    total_days = len(attendance_records)
    if total_days > 0:
        present_days = len([r for r in attendance_records if r.status == 'present'])
        absent_days = len([r for r in attendance_records if r.status == 'absent'])
        late_days = len([r for r in attendance_records if r.status == 'late'])
        excused_days = len([r for r in attendance_records if r.status == 'excused'])
        
        attendance_rate = (present_days / total_days) * 100
        
        # تجميع حسب الأسبوع
        weekly_stats = {}
        for record in attendance_records:
            week = record.attendance_date.strftime('%Y-W%U')
            if week not in weekly_stats:
                weekly_stats[week] = {'present': 0, 'absent': 0, 'late': 0, 'excused': 0}
            weekly_stats[week][record.status] += 1
    else:
        present_days = absent_days = late_days = excused_days = 0
        attendance_rate = 0
        weekly_stats = {}
    
    return jsonify({
        'attendance_records': [record.to_dict() for record in attendance_records],
        'statistics': {
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'late_days': late_days,
            'excused_days': excused_days,
            'attendance_rate': round(attendance_rate, 2)
        },
        'weekly_stats': weekly_stats
    })

@student_dashboard.route('/dashboard/settings', methods=['GET', 'POST'])
def student_dashboard_settings():
    """إدارة إعدادات لوحة تحكم الطالب"""
    student, error = get_current_student()
    if error:
        return jsonify(error[0]), error[1]
    
    if request.method == 'GET':
        # الحصول على الإعدادات الحالية
        settings = db.session.query(StudentDashboardSettings).filter(
            StudentDashboardSettings.student_id == student.id
        ).first()
        
        if not settings:
            # إنشاء إعدادات افتراضية
            settings = StudentDashboardSettings(student_id=student.id)
            db.session.add(settings)
            db.session.commit()
        
        return jsonify(settings.to_dict())
    
    elif request.method == 'POST':
        # تحديث الإعدادات
        data = request.get_json()
        
        settings = db.session.query(StudentDashboardSettings).filter(
            StudentDashboardSettings.student_id == student.id
        ).first()
        
        if not settings:
            settings = StudentDashboardSettings(student_id=student.id)
            db.session.add(settings)
        
        # تحديث الحقول المرسلة
        allowed_fields = [
            'show_upcoming_exams', 'show_assignments', 'show_attendance',
            'show_grades', 'show_schedule', 'theme', 'language',
            'notifications_enabled', 'email_notifications'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(settings, field, data[field])
        
        settings.last_updated = datetime.utcnow()
        
        try:
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'تم حفظ الإعدادات بنجاح',
                'settings': settings.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': 'حدث خطأ أثناء حفظ الإعدادات'
            }), 500

@student_dashboard.route('/dashboard/submit-assignment/<int:assignment_id>', methods=['POST'])
def submit_assignment(assignment_id):
    """تسليم واجب"""
    student, error = get_current_student()
    if error:
        return jsonify(error[0]), error[1]
    
    # التحقق من صحة الواجب
    assignment = db.session.query(Assignment).filter(
        Assignment.id == assignment_id
    ).first()
    
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404
    
    # التحقق من أن الطالب مسجل في الفصل الصحيح
    enrollment = db.session.query(Enrollment).join(Course).filter(
        and_(
            Enrollment.student_id == student.id,
            Course.id == assignment.course_id,
            Enrollment.status == 'active'
        )
    ).first()
    
    if not enrollment:
        return jsonify({'error': 'Student not enrolled in this course'}), 403
    
    # التحقق من عدم وجود تسليم سابق
    existing_submission = db.session.query(AssignmentSubmission).filter(
        and_(
            AssignmentSubmission.assignment_id == assignment_id,
            AssignmentSubmission.student_id == student.id
        )
    ).first()
    
    if existing_submission:
        return jsonify({'error': 'Assignment already submitted'}), 400
    
    # الحصول على بيانات التسليم
    data = request.get_json()
    content = data.get('content', '')
    files = data.get('files', [])
    
    # إنشاء التسليم
    submission = AssignmentSubmission(
        assignment_id=assignment_id,
        student_id=student.id,
        content=content,
        files_json=json.dumps(files) if files else None,
        submission_date=datetime.utcnow()
    )
    
    try:
        db.session.add(submission)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم تسليم الواجب بنجاح',
            'submission': submission.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'حدث خطأ أثناء تسليم الواجب'
        }), 500

# إضافة Blueprint إلى التطبيق
def init_student_dashboard_routes(app):
    app.register_blueprint(student_dashboard, url_prefix='/api/student')
