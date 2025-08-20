"""
خدمة إنشاء المستخدمين مع بيانات تسجيل الدخول التلقائية
User Creation Service with automatic login credentials
"""

from datetime import date, datetime
from src import db
from src.models.user import User, Student, Teacher, Parent
from src.models.extended_models import UserCredentials, generate_username, generate_random_password
import json


class UserCreationService:
    """خدمة إنشاء المستخدمين مع بيانات الدخول التلقائية"""
    
    @staticmethod
    def create_teacher_with_credentials(name, email, phone, subjects=None, qualification=None, **kwargs):
        """إنشاء معلم مع بيانات تسجيل الدخول التلقائية"""
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return {
                    'success': False,
                    'error': f'المستخدم موجود مسبقاً بالبريد الإلكتروني {email}'
                }
            
            # Generate username and password
            username = generate_username(name, 'teacher')
            password = generate_random_password()
            
            # Create user
            user = User(
                username=username,
                email=email,
                name=name,
                role='teacher',
                phone=phone,
                is_active=True
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.flush()  # To get user.id
            
            # Generate teacher ID
            teacher_id = f"T{user.id:05d}"
            
            # Create teacher profile
            teacher = Teacher(
                user_id=user.id,
                teacher_id=teacher_id,
                subjects=json.dumps(subjects, ensure_ascii=False) if subjects else None,
                qualification=qualification
            )
            
            db.session.add(teacher)
            db.session.flush()
            
            # Create credentials record
            credentials = UserCredentials(
                user_id=user.id,
                generated_username=username,
                generated_password=password
            )
            
            db.session.add(credentials)
            db.session.commit()
            
            return {
                'success': True,
                'user': user.to_dict(),
                'teacher': teacher.to_dict(),
                'credentials': {
                    'username': username,
                    'password': password
                }
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': f'خطأ في إنشاء المعلم: {str(e)}'
            }
    
    @staticmethod
    def create_student_with_credentials(name, email, phone, class_name, date_of_birth=None, **kwargs):
        """إنشاء طالب مع بيانات تسجيل الدخول التلقائية"""
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return {
                    'success': False,
                    'error': f'المستخدم موجود مسبقاً بالبريد الإلكتروني {email}'
                }
            
            # Generate username and password
            username = generate_username(name, 'student')
            password = generate_random_password()
            
            # Create user
            user = User(
                username=username,
                email=email,
                name=name,
                role='student',
                phone=phone,
                is_active=True
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.flush()  # To get user.id
            
            # Generate student ID
            student_id = f"S{user.id:05d}"
            
            # Create student profile
            student = Student(
                user_id=user.id,
                student_id=student_id,
                class_name=class_name,
                date_of_birth=date_of_birth
            )
            
            db.session.add(student)
            db.session.flush()
            
            # Create credentials record
            credentials = UserCredentials(
                user_id=user.id,
                generated_username=username,
                generated_password=password
            )
            
            db.session.add(credentials)
            db.session.commit()
            
            return {
                'success': True,
                'user': user.to_dict(),
                'student': student.to_dict(),
                'credentials': {
                    'username': username,
                    'password': password
                }
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': f'خطأ في إنشاء الطالب: {str(e)}'
            }
    
    @staticmethod
    def create_parent_with_credentials(name, email, phone, occupation=None, relationship='parent', **kwargs):
        """إنشاء ولي أمر مع بيانات تسجيل الدخول التلقائية"""
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return {
                    'success': False,
                    'error': f'المستخدم موجود مسبقاً بالبريد الإلكتروني {email}'
                }
            
            # Generate username and password
            username = generate_username(name, 'parent')
            password = generate_random_password()
            
            # Create user
            user = User(
                username=username,
                email=email,
                name=name,
                role='parent',
                phone=phone,
                is_active=True
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.flush()  # To get user.id
            
            # Create parent profile
            parent = Parent(
                user_id=user.id,
                occupation=occupation,
                relationship=relationship
            )
            
            db.session.add(parent)
            db.session.flush()
            
            # Create credentials record
            credentials = UserCredentials(
                user_id=user.id,
                generated_username=username,
                generated_password=password
            )
            
            db.session.add(credentials)
            db.session.commit()
            
            return {
                'success': True,
                'user': user.to_dict(),
                'parent': parent.to_dict(),
                'credentials': {
                    'username': username,
                    'password': password
                }
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': f'خطأ في إنشاء ولي الأمر: {str(e)}'
            }
    
    @staticmethod
    def get_pending_credentials():
        """الحصول على بيانات تسجيل الدخول التي لم يطلع عليها المدير بعد"""
        try:
            credentials = UserCredentials.query.filter_by(viewed_by_admin=False).all()
            return {
                'success': True,
                'credentials': [cred.to_dict() for cred in credentials]
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'خطأ في جلب بيانات تسجيل الدخول: {str(e)}'
            }
    
    @staticmethod
    def mark_credentials_viewed(credential_ids):
        """تمييز بيانات تسجيل الدخول كمطلع عليها"""
        try:
            credentials = UserCredentials.query.filter(UserCredentials.id.in_(credential_ids)).all()
            for cred in credentials:
                cred.viewed_by_admin = True
                cred.viewed_at = datetime.utcnow()
            
            db.session.commit()
            return {
                'success': True,
                'message': f'تم تمييز {len(credentials)} سجل كمطلع عليه'
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': f'خطأ في تمييز بيانات تسجيل الدخول: {str(e)}'
            }
    
    @staticmethod
    def mark_credentials_delivered(credential_ids):
        """تمييز بيانات تسجيل الدخول كمسلمة للمستخدم"""
        try:
            credentials = UserCredentials.query.filter(UserCredentials.id.in_(credential_ids)).all()
            for cred in credentials:
                cred.delivered_to_user = True
                cred.delivered_at = datetime.utcnow()
            
            db.session.commit()
            return {
                'success': True,
                'message': f'تم تمييز {len(credentials)} سجل كمسلم للمستخدم'
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': f'خطأ في تمييز بيانات تسجيل الدخول: {str(e)}'
            }
