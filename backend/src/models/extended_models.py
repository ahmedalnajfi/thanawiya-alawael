from datetime import datetime, date
import secrets
import string
from sqlalchemy import func
from src import db
from src.models.user import User, Student, Teacher, Parent


def generate_random_password(length=8):
    """Generate a random password with letters and numbers."""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def generate_username(base_name, role):
    """Generate unique username based on name and role."""
    # Clean and format base name
    cleaned_name = ''.join(e for e in base_name if e.isalnum())[:10]
    
    # Add role prefix
    role_prefix = {
        'student': 'st',
        'teacher': 'tr', 
        'parent': 'pr',
        'admin': 'ad'
    }.get(role, 'us')
    
    # Generate random suffix
    suffix = ''.join(secrets.choice(string.digits) for _ in range(4))
    
    username = f"{role_prefix}_{cleaned_name}_{suffix}".lower()
    
    # Ensure uniqueness
    from src.models.user import User
    counter = 1
    original_username = username
    while User.query.filter_by(username=username).first():
        username = f"{original_username}_{counter}"
        counter += 1
    
    return username


class UserCredentials(db.Model):
    """جدول لحفظ بيانات تسجيل الدخول المُنشأة تلقائياً"""
    __tablename__ = 'user_credentials'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    generated_username = db.Column(db.String(50), nullable=False)
    generated_password = db.Column(db.String(20), nullable=False)  # Store plain text for admin
    password_changed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    viewed_by_admin = db.Column(db.Boolean, default=False)
    viewed_at = db.Column(db.DateTime)
    delivered_to_user = db.Column(db.Boolean, default=False)
    delivered_at = db.Column(db.DateTime)
    
    user = db.relationship('User', backref=db.backref('credentials', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'generated_username': self.generated_username,
            'generated_password': self.generated_password,
            'password_changed': self.password_changed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'viewed_by_admin': self.viewed_by_admin,
            'viewed_at': self.viewed_at.isoformat() if self.viewed_at else None,
            'delivered_to_user': self.delivered_to_user,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'user': self.user.to_dict() if self.user else None
        }


class AcademicYear(db.Model):
    """السنوات الأكاديمية"""
    __tablename__ = 'academic_years'
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(10), nullable=False, unique=True)  # e.g., "2024-2025"
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_current = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'year': self.year,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_current': self.is_current,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Classroom(db.Model):
    """الفصول الدراسية"""
    __tablename__ = 'classrooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # e.g., "3أ"
    grade_level = db.Column(db.String(10), nullable=False)  # e.g., "10", "11", "12"
    section = db.Column(db.String(20))  # e.g., "علمي", "أدبي", "فرنسي"
    academic_year_id = db.Column(db.Integer, db.ForeignKey('academic_years.id'), nullable=False)
    homeroom_teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    capacity = db.Column(db.Integer, default=30)
    building = db.Column(db.String(50))  # e.g., "بناية البنين"
    floor = db.Column(db.String(10))
    room_number = db.Column(db.String(10))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    academic_year = db.relationship('AcademicYear', backref='classrooms')
    homeroom_teacher = db.relationship('Teacher', backref='homeroom_classes')
    
    @property
    def enrolled_count(self):
        return len(self.enrollments)
    
    @property
    def available_spots(self):
        return self.capacity - self.enrolled_count
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'grade_level': self.grade_level,
            'section': self.section,
            'academic_year_id': self.academic_year_id,
            'homeroom_teacher_id': self.homeroom_teacher_id,
            'capacity': self.capacity,
            'enrolled_count': self.enrolled_count,
            'available_spots': self.available_spots,
            'building': self.building,
            'floor': self.floor,
            'room_number': self.room_number,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'academic_year': self.academic_year.to_dict() if self.academic_year else None,
            'homeroom_teacher': self.homeroom_teacher.to_dict() if self.homeroom_teacher else None
        }


class Subject(db.Model):
    """المواد الدراسية"""
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100))
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    department = db.Column(db.String(50))  # قسم المادة
    is_mandatory = db.Column(db.Boolean, default=True)
    grade_levels = db.Column(db.Text)  # JSON array of applicable grade levels
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'name': self.name,
            'name_en': self.name_en,
            'code': self.code,
            'description': self.description,
            'department': self.department,
            'is_mandatory': self.is_mandatory,
            'grade_levels': json.loads(self.grade_levels) if self.grade_levels else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }


class Course(db.Model):
    """ربط المادة بالفصل والمعلم"""
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    schedule_json = db.Column(db.Text)  # JSON schedule data
    credit_hours = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    classroom = db.relationship('Classroom', backref='courses')
    subject = db.relationship('Subject', backref='courses')
    teacher = db.relationship('Teacher', backref='courses')
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'classroom_id': self.classroom_id,
            'subject_id': self.subject_id,
            'teacher_id': self.teacher_id,
            'schedule': json.loads(self.schedule_json) if self.schedule_json else {},
            'credit_hours': self.credit_hours,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'classroom': self.classroom.to_dict() if self.classroom else None,
            'subject': self.subject.to_dict() if self.subject else None,
            'teacher': self.teacher.to_dict() if self.teacher else None
        }


class Enrollment(db.Model):
    """تسجيل الطلاب في الفصول"""
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    enrollment_date = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(20), default='active')  # active, transferred, graduated, dropped
    notes = db.Column(db.Text)
    
    classroom = db.relationship('Classroom', backref='enrollments')
    student = db.relationship('Student', backref='enrollments')
    
    # Unique constraint to prevent duplicate enrollments
    __table_args__ = (db.UniqueConstraint('classroom_id', 'student_id', name='unique_enrollment'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'classroom_id': self.classroom_id,
            'student_id': self.student_id,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'status': self.status,
            'notes': self.notes,
            'classroom': self.classroom.to_dict() if self.classroom else None,
            'student': self.student.to_dict() if self.student else None
        }


class Assignment(db.Model):
    """الواجبات"""
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    assignment_type = db.Column(db.String(30), nullable=False)  # homework, project, quiz, exam
    max_score = db.Column(db.Float, default=100.0)
    due_date = db.Column(db.DateTime)
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    attachments_json = db.Column(db.Text)  # JSON array of file paths
    is_active = db.Column(db.Boolean, default=True)
    
    course = db.relationship('Course', backref='assignments')
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'assignment_type': self.assignment_type,
            'max_score': self.max_score,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'assigned_date': self.assigned_date.isoformat() if self.assigned_date else None,
            'attachments': json.loads(self.attachments_json) if self.attachments_json else [],
            'is_active': self.is_active,
            'course': self.course.to_dict() if self.course else None
        }


class GradeSystem(db.Model):
    """نظام الدرجات المرن - يومي، أسبوعي، شهري"""
    __tablename__ = 'grade_systems'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # e.g., "اختبار الأسبوع الأول"
    grade_type = db.Column(db.String(20), nullable=False)  # daily, weekly, monthly, midterm, final
    frequency = db.Column(db.String(20))  # once, weekly, monthly, quarterly
    weight_percentage = db.Column(db.Float, default=10.0)  # وزن الدرجة في التقييم الكامل
    max_score = db.Column(db.Float, default=100.0)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # إعدادات تلقائية للإشعارات
    notify_parents = db.Column(db.Boolean, default=True)
    auto_publish = db.Column(db.Boolean, default=False)  # نشر تلقائي أم يحتاج موافقة
    
    course = db.relationship('Course', backref='grade_systems')
    creator = db.relationship('Teacher', backref='created_grade_systems')
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'name': self.name,
            'grade_type': self.grade_type,
            'frequency': self.frequency,
            'weight_percentage': self.weight_percentage,
            'max_score': self.max_score,
            'is_active': self.is_active,
            'notify_parents': self.notify_parents,
            'auto_publish': self.auto_publish,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'course': self.course.to_dict() if self.course else None,
            'creator': self.creator.to_dict() if self.creator else None
        }


class StudentGrade(db.Model):
    """درجات الطلاب المحسنة"""
    __tablename__ = 'student_grades'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    grade_system_id = db.Column(db.Integer, db.ForeignKey('grade_systems.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))  # اختياري للواجبات
    score = db.Column(db.Float, nullable=False)
    max_score = db.Column(db.Float, nullable=False)
    percentage = db.Column(db.Float)  # محسوبة تلقائياً
    grade_letter = db.Column(db.String(5))  # A, B, C, D, F
    recorded_date = db.Column(db.Date, default=date.today)
    recorded_by = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # حالة النشر والإشعارات
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    parent_notified = db.Column(db.Boolean, default=False)
    parent_notified_at = db.Column(db.DateTime)
    
    notes = db.Column(db.Text)
    
    student = db.relationship('Student', backref='student_grades')
    grade_system = db.relationship('GradeSystem', backref='student_grades')
    assignment = db.relationship('Assignment', backref='student_grades')
    recorder = db.relationship('Teacher', backref='grades_recorded')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # حساب النسبة المئوية وتحديد الدرجة الحرفية تلقائياً
        if self.score is not None and self.max_score is not None and self.max_score > 0:
            self.percentage = round((self.score / self.max_score) * 100, 2)
            self.grade_letter = self.calculate_grade_letter()
    
    def calculate_grade_letter(self):
        """حساب الدرجة الحرفية بناءً على النسبة المئوية"""
        if self.percentage >= 90:
            return 'A+'
        elif self.percentage >= 85:
            return 'A'
        elif self.percentage >= 80:
            return 'B+'
        elif self.percentage >= 75:
            return 'B'
        elif self.percentage >= 70:
            return 'C+'
        elif self.percentage >= 65:
            return 'C'
        elif self.percentage >= 60:
            return 'D+'
        elif self.percentage >= 55:
            return 'D'
        else:
            return 'F'
    
    def publish_grade(self):
        """نشر الدرجة وإرسال إشعار لولي الأمر"""
        self.is_published = True
        self.published_at = datetime.utcnow()
        
        # إنشاء إشعار لولي الأمر
        if self.grade_system.notify_parents:
            self.create_parent_notification()
    
    def create_parent_notification(self):
        """إنشاء إشعار لولي الأمر عن الدرجة الجديدة"""
        # سيتم تنفيذ هذا في نظام الإشعارات لاحقاً
        pass
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'grade_system_id': self.grade_system_id,
            'assignment_id': self.assignment_id,
            'score': self.score,
            'max_score': self.max_score,
            'percentage': self.percentage,
            'grade_letter': self.grade_letter,
            'recorded_date': self.recorded_date.isoformat() if self.recorded_date else None,
            'recorded_by': self.recorded_by,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None,
            'is_published': self.is_published,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'parent_notified': self.parent_notified,
            'parent_notified_at': self.parent_notified_at.isoformat() if self.parent_notified_at else None,
            'notes': self.notes,
            'student': self.student.to_dict() if self.student else None,
            'grade_system': self.grade_system.to_dict() if self.grade_system else None,
            'assignment': self.assignment.to_dict() if self.assignment else None,
            'recorder': self.recorder.to_dict() if self.recorder else None
        }


class AttendanceRecord(db.Model):
    """سجل الحضور المحسن"""
    __tablename__ = 'attendance_records'
    
    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))  # اختياري - لحصة معينة
    attendance_date = db.Column(db.Date, nullable=False, default=date.today)
    period = db.Column(db.String(20))  # morning, afternoon, period_1, period_2, etc.
    status = db.Column(db.String(20), nullable=False)  # present, absent, late, excused, sick
    arrival_time = db.Column(db.Time)
    departure_time = db.Column(db.Time)
    notes = db.Column(db.Text)
    recorded_by = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    classroom = db.relationship('Classroom', backref='attendance_records')
    student = db.relationship('Student', backref='extended_attendance_records')
    course = db.relationship('Course', backref='attendance_records')
    recorder = db.relationship('Teacher', backref='attendance_records')
    
    def to_dict(self):
        return {
            'id': self.id,
            'classroom_id': self.classroom_id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'attendance_date': self.attendance_date.isoformat() if self.attendance_date else None,
            'period': self.period,
            'status': self.status,
            'arrival_time': self.arrival_time.isoformat() if self.arrival_time else None,
            'departure_time': self.departure_time.isoformat() if self.departure_time else None,
            'notes': self.notes,
            'recorded_by': self.recorded_by,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None,
            'classroom': self.classroom.to_dict() if self.classroom else None,
            'student': self.student.to_dict() if self.student else None,
            'course': self.course.to_dict() if self.course else None,
            'recorder': self.recorder.to_dict() if self.recorder else None
        }


class Notification(db.Model):
    """نظام الإشعارات"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # grade, attendance, announcement, behavior
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    data_json = db.Column(db.Text)  # Additional data as JSON
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    user = db.relationship('User', backref='notifications')
    
    def mark_as_read(self):
        self.is_read = True
        self.read_at = datetime.utcnow()
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'title': self.title,
            'body': self.body,
            'data': json.loads(self.data_json) if self.data_json else {},
            'priority': self.priority,
            'is_read': self.is_read,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'user': self.user.to_dict() if self.user else None
        }
