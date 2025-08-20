from datetime import datetime, date, time
from sqlalchemy import func
from src import db
from src.models.user import User, Student, Teacher
from src.models.extended_models import Course, Assignment, AttendanceRecord, StudentGrade

class Exam(db.Model):
    """نموذج الامتحانات والاختبارات"""
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    exam_type = db.Column(db.String(50), nullable=False)  # يومي، أسبوعي، شهري، نصف فصلي، نهائي
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    
    exam_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100))  # رقم القاعة أو المكان
    
    total_marks = db.Column(db.Float, nullable=False, default=100.0)
    passing_score = db.Column(db.Float, default=50.0)
    weight_percentage = db.Column(db.Float, default=20.0)  # الوزن النسبي من الدرجة النهائية
    
    is_published = db.Column(db.Boolean, default=False)  # هل تم نشر الاختبار للطلاب؟
    published_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    subject = db.relationship('Subject', backref='exams')
    classroom = db.relationship('Classroom', backref='exams')
    teacher = db.relationship('Teacher', backref='exams')
    
    @property
    def duration_minutes(self):
        """حساب مدة الامتحان بالدقائق"""
        if self.start_time and self.end_time:
            start_seconds = self.start_time.hour * 3600 + self.start_time.minute * 60
            end_seconds = self.end_time.hour * 3600 + self.end_time.minute * 60
            return (end_seconds - start_seconds) // 60
        return 0
    
    @property
    def is_upcoming(self):
        """التحقق مما إذا كان الامتحان قادماً"""
        return self.exam_date >= date.today()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'exam_type': self.exam_type,
            'subject_id': self.subject_id,
            'classroom_id': self.classroom_id,
            'teacher_id': self.teacher_id,
            'exam_date': self.exam_date.isoformat() if self.exam_date else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'location': self.location,
            'duration_minutes': self.duration_minutes,
            'total_marks': self.total_marks,
            'passing_score': self.passing_score,
            'weight_percentage': self.weight_percentage,
            'is_published': self.is_published,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_upcoming': self.is_upcoming,
            'subject': self.subject.to_dict() if self.subject else None,
            'classroom': self.classroom.to_dict() if self.classroom else None,
            'teacher': self.teacher.to_dict() if self.teacher else None
        }

class ClassSchedule(db.Model):
    """نموذج جدول الحصص اليومي"""
    __tablename__ = 'class_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Sunday, 1=Monday, ..., 6=Saturday
    period_number = db.Column(db.Integer, nullable=False)  # ترتيب الحصة في اليوم
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100))  # الفصل أو المختبر
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    classroom = db.relationship('Classroom', backref='schedule')
    course = db.relationship('Course', backref='schedule')
    teacher = db.relationship('Teacher', backref='schedule')
    
    @property
    def day_name(self):
        """اسم اليوم بالعربية"""
        days = ['الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']
        return days[self.day_of_week]
    
    @property
    def day_name_en(self):
        """اسم اليوم بالإنجليزية"""
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        return days[self.day_of_week]
    
    @property
    def duration_minutes(self):
        """حساب مدة الحصة بالدقائق"""
        if self.start_time and self.end_time:
            start_seconds = self.start_time.hour * 3600 + self.start_time.minute * 60
            end_seconds = self.end_time.hour * 3600 + self.end_time.minute * 60
            return (end_seconds - start_seconds) // 60
        return 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'classroom_id': self.classroom_id,
            'day_of_week': self.day_of_week,
            'day_name': self.day_name,
            'day_name_en': self.day_name_en,
            'period_number': self.period_number,
            'course_id': self.course_id,
            'teacher_id': self.teacher_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_minutes': self.duration_minutes,
            'location': self.location,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'classroom': self.classroom.to_dict() if self.classroom else None,
            'course': self.course.to_dict() if self.course else None,
            'teacher': self.teacher.to_dict() if self.teacher else None
        }

class SchoolDay(db.Model):
    """نموذج معلومات الدوام المدرسي"""
    __tablename__ = 'school_days'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    day_type = db.Column(db.String(20), nullable=False, default='regular')  # regular, holiday, exam, special
    is_school_day = db.Column(db.Boolean, default=True)
    
    start_time = db.Column(db.Time)  # وقت بدء الدوام
    end_time = db.Column(db.Time)  # وقت انتهاء الدوام
    
    note = db.Column(db.Text)  # ملاحظات خاصة بهذا اليوم
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'day_type': self.day_type,
            'is_school_day': self.is_school_day,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'note': self.note,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AssignmentSubmission(db.Model):
    """نموذج تسليم الواجبات"""
    __tablename__ = 'assignment_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text)  # المحتوى النصي للتسليم
    files_json = db.Column(db.Text)  # مسارات الملفات المرفقة بتنسيق JSON
    
    status = db.Column(db.String(20), default='submitted')  # submitted, reviewed, returned, accepted
    grade = db.Column(db.Float)  # درجة الواجب
    feedback = db.Column(db.Text)  # ملاحظات المعلم
    
    graded_by = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    graded_at = db.Column(db.DateTime)
    
    # Relations
    assignment = db.relationship('Assignment', backref='submissions')
    student = db.relationship('Student', backref='assignment_submissions')
    teacher = db.relationship('Teacher', foreign_keys=[graded_by], backref='graded_submissions')
    
    @property
    def is_late(self):
        """التحقق مما إذا كان التسليم متأخراً"""
        if self.submission_date and self.assignment.due_date:
            return self.submission_date > self.assignment.due_date
        return False
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'assignment_id': self.assignment_id,
            'student_id': self.student_id,
            'submission_date': self.submission_date.isoformat() if self.submission_date else None,
            'content': self.content,
            'files': json.loads(self.files_json) if self.files_json else [],
            'status': self.status,
            'grade': self.grade,
            'feedback': self.feedback,
            'graded_by': self.graded_by,
            'graded_at': self.graded_at.isoformat() if self.graded_at else None,
            'is_late': self.is_late,
            'assignment': self.assignment.to_dict() if self.assignment else None,
            'student': self.student.to_dict() if self.student else None,
            'teacher': self.teacher.to_dict() if self.teacher else None
        }

class StudentDashboardSettings(db.Model):
    """إعدادات لوحة تحكم الطالب"""
    __tablename__ = 'student_dashboard_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False, unique=True)
    
    show_upcoming_exams = db.Column(db.Boolean, default=True)
    show_assignments = db.Column(db.Boolean, default=True)
    show_attendance = db.Column(db.Boolean, default=True)
    show_grades = db.Column(db.Boolean, default=True)
    show_schedule = db.Column(db.Boolean, default=True)
    
    theme = db.Column(db.String(20), default='light')  # light, dark, system
    language = db.Column(db.String(10), default='ar')  # ar, en
    
    notifications_enabled = db.Column(db.Boolean, default=True)
    email_notifications = db.Column(db.Boolean, default=True)
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    student = db.relationship('Student', backref=db.backref('dashboard_settings', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'show_upcoming_exams': self.show_upcoming_exams,
            'show_assignments': self.show_assignments,
            'show_attendance': self.show_attendance,
            'show_grades': self.show_grades,
            'show_schedule': self.show_schedule,
            'theme': self.theme,
            'language': self.language,
            'notifications_enabled': self.notifications_enabled,
            'email_notifications': self.email_notifications,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'student': self.student.to_dict() if self.student else None
        }
