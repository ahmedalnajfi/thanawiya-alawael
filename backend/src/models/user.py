from src import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Import extended models to ensure they are registered
try:
    from src.models.extended_models import (
        UserCredentials, AcademicYear, Classroom, Subject, Course, 
        Enrollment, Assignment, GradeSystem, StudentGrade, 
        AttendanceRecord, Notification
    )
except ImportError:
    pass  # Will be imported after first migration

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student, parent, teacher, admin
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'name': self.name,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    class_name = db.Column(db.String(10), nullable=False)
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.Text)
    emergency_contact = db.Column(db.String(20))
    
    user = db.relationship('User', backref=db.backref('student_profile', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'student_id': self.student_id,
            'class_name': self.class_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'address': self.address,
            'emergency_contact': self.emergency_contact,
            'user': self.user.to_dict() if self.user else None
        }

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teacher_id = db.Column(db.String(20), unique=True, nullable=False)
    subjects = db.Column(db.Text)  # JSON string of subjects
    classes = db.Column(db.Text)   # JSON string of classes
    qualification = db.Column(db.String(100))
    hire_date = db.Column(db.Date)
    
    user = db.relationship('User', backref=db.backref('teacher_profile', uselist=False))
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'user_id': self.user_id,
            'teacher_id': self.teacher_id,
            'subjects': json.loads(self.subjects) if self.subjects else [],
            'classes': json.loads(self.classes) if self.classes else [],
            'qualification': self.qualification,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'user': self.user.to_dict() if self.user else None
        }

class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    occupation = db.Column(db.String(100))
    relationship = db.Column(db.String(20))  # father, mother, guardian
    
    user = db.relationship('User', backref=db.backref('parent_profile', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'occupation': self.occupation,
            'relationship': self.relationship,
            'user': self.user.to_dict() if self.user else None
        }

class ParentStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    
    parent = db.relationship('Parent', backref='children')
    student = db.relationship('Student', backref='parents')

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    total_marks = db.Column(db.Float, default=100)
    grade_type = db.Column(db.String(20), nullable=False)  # exam, assignment, quiz, project
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)
    semester = db.Column(db.String(20))
    notes = db.Column(db.Text)
    
    student = db.relationship('Student', backref='grades')
    teacher = db.relationship('Teacher', backref='grades_given')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'teacher_id': self.teacher_id,
            'subject': self.subject,
            'grade': self.grade,
            'total_marks': self.total_marks,
            'grade_type': self.grade_type,
            'date_recorded': self.date_recorded.isoformat() if self.date_recorded else None,
            'semester': self.semester,
            'notes': self.notes,
            'percentage': round((self.grade / self.total_marks) * 100, 2) if self.total_marks > 0 else 0
        }

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # present, absent, late, excused
    period = db.Column(db.String(20))  # morning, afternoon, specific period
    notes = db.Column(db.Text)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('Student', backref='attendance_records')
    teacher = db.relationship('Teacher', backref='attendance_taken')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'teacher_id': self.teacher_id,
            'date': self.date.isoformat() if self.date else None,
            'status': self.status,
            'period': self.period,
            'notes': self.notes,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None
        }

class BehaviorNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    note_type = db.Column(db.String(20), nullable=False)  # positive, negative, neutral
    note = db.Column(db.Text, nullable=False)
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)
    severity = db.Column(db.String(20))  # low, medium, high
    action_taken = db.Column(db.Text)
    
    student = db.relationship('Student', backref='behavior_notes')
    teacher = db.relationship('Teacher', backref='behavior_notes_given')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'teacher_id': self.teacher_id,
            'note_type': self.note_type,
            'note': self.note,
            'date_recorded': self.date_recorded.isoformat() if self.date_recorded else None,
            'severity': self.severity,
            'action_taken': self.action_taken
        }

class Tuition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    paid_amount = db.Column(db.Float, default=0)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, partial, paid, overdue
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('Student', backref='tuition_records')
    
    @property
    def remaining_amount(self):
        return self.total_amount - self.paid_amount
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'academic_year': self.academic_year,
            'total_amount': self.total_amount,
            'paid_amount': self.paid_amount,
            'remaining_amount': self.remaining_amount,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tuition_id = db.Column(db.Integer, db.ForeignKey('tuition.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # cash, bank_transfer, online
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    reference_number = db.Column(db.String(50))
    notes = db.Column(db.Text)
    
    tuition = db.relationship('Tuition', backref='payments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'tuition_id': self.tuition_id,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'reference_number': self.reference_number,
            'notes': self.notes
        }

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    target_audience = db.Column(db.String(20), nullable=False)  # all, students, parents, teachers
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    
    creator = db.relationship('User', backref='announcements')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'target_audience': self.target_audience,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'priority': self.priority,
            'creator': self.creator.to_dict() if self.creator else None
        }

class AIInsight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    insight_type = db.Column(db.String(50), nullable=False)  # performance, behavior, risk_assessment
    content = db.Column(db.Text, nullable=False)
    confidence_score = db.Column(db.Float)  # 0-1 confidence level
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    student = db.relationship('Student', backref='ai_insights')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'insight_type': self.insight_type,
            'content': self.content,
            'confidence_score': self.confidence_score,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'is_active': self.is_active
        }

