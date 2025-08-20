from datetime import datetime
from src.models.user import db, User, Student, Teacher, Parent
from src.models.extended_models import UserCredentials, generate_random_password, generate_username


class UserCreationService:
    """خدمة إنشاء المستخدمين مع إنشاء بيانات تسجيل الدخول تلقائياً"""
    
    @staticmethod
    def create_student_with_credentials(name, email, phone=None, student_id=None, 
                                       class_name=None, date_of_birth=None, 
                                       address=None, emergency_contact=None):
        """إنشاء طالب مع بيانات تسجيل الدخول التلقائية"""
        try:
            # إنشاء اسم مستخدم وكلمة مرور
            username = generate_username(name, 'student')
            password = generate_random_password()
            
            # إنشاء المستخدم الأساسي
            user = User(
                username=username,
                email=email,
                name=name,
                phone=phone,
                role='student',
                is_active=True
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.flush()  # للحصول على user.id
            
            # إنشاء ملف الطالب
            student = Student(
                user_id=user.id,
                student_id=student_id or f"ST{user.id:06d}",
                class_name=class_name,
                date_of_birth=date_of_birth,
                address=address,
                emergency_contact=emergency_contact
            )
            
            db.session.add(student)
            
            # حفظ بيانات تسجيل الدخول للمدير
            credentials = UserCredentials(
                user_id=user.id,
                generated_username=username,
                generated_password=password,  # حفظ كلمة المرور للمدير
                password_changed=False,
                created_at=datetime.utcnow()
            )
            
            db.session.add(credentials)
            db.session.commit()
            
            return {
                'success': True,
                'user': user.to_dict(),
                'student': student.to_dict(),
                'credentials': {
                    'username': username,
                    'password': password,
                    'message': 'تم إنشاء بيانات تسجيل الدخول تلقائياً'
                }
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def create_teacher_with_credentials(name, email, phone=None, teacher_id=None,
                                       subjects=None, classes=None, qualification=None,
                                       hire_date=None):
        """إنشاء معلم مع بيانات تسجيل الدخول التلقائية"""
        try:
            # إنشاء اسم مستخدم وكلمة مرور
            username = generate_username(name, 'teacher')
            password = generate_random_password()
            
            # إنشاء المستخدم الأساسي
            user = User(
                username=username,
                email=email,
                name=name,
                phone=phone,
                role='teacher',
                is_active=True
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.flush()  # للحصول على user.id
            
            # إنشاء ملف المعلم
            import json
            teacher = Teacher(
                user_id=user.id,
                teacher_id=teacher_id or f"TR{user.id:06d}",
                subjects=json.dumps(subjects or [], ensure_ascii=False),
                classes=json.dumps(classes or [], ensure_ascii=False),
                qualification=qualification,
                hire_date=hire_date
            )
            
            db.session.add(teacher)
            
            # حفظ بيانات تسجيل الدخول للمدير
            credentials = UserCredentials(
                user_id=user.id,
                generated_username=username,
                generated_password=password,  # حفظ كلمة المرور للمدير
                password_changed=False,
                created_at=datetime.utcnow()
            )
            
            db.session.add(credentials)
            db.session.commit()
            
            return {
                'success': True,
                'user': user.to_dict(),
                'teacher': teacher.to_dict(),
                'credentials': {
                    'username': username,
                    'password': password,
                    'message': 'تم إنشاء بيانات تسجيل الدخول تلقائياً'
                }
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def create_parent_with_credentials(name, email, phone=None, occupation=None,
                                      relationship='father'):
        """إنشاء ولي أمر مع بيانات تسجيل الدخول التلقائية"""
        try:
            # إنشاء اسم مستخدم وكلمة مرور
            username = generate_username(name, 'parent')
            password = generate_random_password()
            
            # إنشاء المستخدم الأساسي
            user = User(
                username=username,
                email=email,
                name=name,
                phone=phone,
                role='parent',
                is_active=True
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.flush()  # للحصول على user.id
            
            # إنشاء ملف ولي الأمر
            parent = Parent(
                user_id=user.id,
                occupation=occupation,
                relationship=relationship
            )
            
            db.session.add(parent)
            
            # حفظ بيانات تسجيل الدخول للمدير
            credentials = UserCredentials(
                user_id=user.id,
                generated_username=username,
                generated_password=password,  # حفظ كلمة المرور للمدير
                password_changed=False,
                created_at=datetime.utcnow()
            )
            
            db.session.add(credentials)
            db.session.commit()
            
            return {
                'success': True,
                'user': user.to_dict(),
                'parent': parent.to_dict(),
                'credentials': {
                    'username': username,
                    'password': password,
                    'message': 'تم إنشاء بيانات تسجيل الدخول تلقائياً'
                }
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_pending_credentials_for_admin():
        """استرجاع بيانات تسجيل الدخول التي لم يراها المدير بعد"""
        credentials = UserCredentials.query.filter_by(
            viewed_by_admin=False
        ).order_by(UserCredentials.created_at.desc()).all()
        
        return [cred.to_dict() for cred in credentials]
    
    @staticmethod
    def mark_credentials_viewed(credential_ids, admin_id):
        """تحديد بيانات تسجيل الدخول كمشاهدة من قبل المدير"""
        try:
            credentials = UserCredentials.query.filter(
                UserCredentials.id.in_(credential_ids)
            ).all()
            
            for cred in credentials:
                cred.viewed_by_admin = True
                cred.viewed_at = datetime.utcnow()
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
    
    @staticmethod
    def mark_credentials_delivered(credential_ids, admin_id):
        """تحديد بيانات تسجيل الدخول كمُسلَّمة للمستخدمين"""
        try:
            credentials = UserCredentials.query.filter(
                UserCredentials.id.in_(credential_ids)
            ).all()
            
            for cred in credentials:
                cred.delivered_to_user = True
                cred.delivered_at = datetime.utcnow()
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False


class GradeSystemService:
    """خدمة إدارة نظام الدرجات المرن"""
    
    @staticmethod
    def create_grade_system(course_id, teacher_id, name, grade_type,
                           weight_percentage=10.0, max_score=100.0,
                           notify_parents=True, auto_publish=False):
        """إنشاء نظام درجات جديد للمعلم"""
        try:
            from src.models.extended_models import GradeSystem
            
            grade_system = GradeSystem(
                course_id=course_id,
                name=name,
                grade_type=grade_type,
                weight_percentage=weight_percentage,
                max_score=max_score,
                notify_parents=notify_parents,
                auto_publish=auto_publish,
                created_by=teacher_id,
                is_active=True
            )
            
            db.session.add(grade_system)
            db.session.commit()
            
            return {
                'success': True,
                'grade_system': grade_system.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def record_student_grade(student_id, grade_system_id, score, teacher_id,
                           assignment_id=None, notes=None):
        """تسجيل درجة طالب مع إشعار ولي الأمر تلقائياً"""
        try:
            from src.models.extended_models import StudentGrade, GradeSystem
            
            # التأكد من صحة نظام الدرجات
            grade_system = GradeSystem.query.get(grade_system_id)
            if not grade_system:
                return {
                    'success': False,
                    'error': 'نظام الدرجات غير موجود'
                }
            
            # إنشاء درجة الطالب
            student_grade = StudentGrade(
                student_id=student_id,
                grade_system_id=grade_system_id,
                assignment_id=assignment_id,
                score=score,
                max_score=grade_system.max_score,
                recorded_by=teacher_id,
                notes=notes
            )
            
            db.session.add(student_grade)
            
            # نشر تلقائي إذا كان مُفعل
            if grade_system.auto_publish:
                student_grade.publish_grade()
            
            db.session.commit()
            
            return {
                'success': True,
                'student_grade': student_grade.to_dict(),
                'auto_published': grade_system.auto_publish
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_unpublished_grades_for_teacher(teacher_id):
        """استرجاع الدرجات غير المنشورة للمعلم"""
        from src.models.extended_models import StudentGrade, GradeSystem, Course
        
        unpublished_grades = db.session.query(StudentGrade).join(
            GradeSystem
        ).join(Course).filter(
            Course.teacher_id == teacher_id,
            StudentGrade.is_published == False
        ).all()
        
        return [grade.to_dict() for grade in unpublished_grades]
    
    @staticmethod
    def publish_grades(grade_ids, teacher_id):
        """نشر درجات متعددة وإرسال إشعارات لأولياء الأمور"""
        try:
            from src.models.extended_models import StudentGrade
            
            grades = StudentGrade.query.filter(
                StudentGrade.id.in_(grade_ids)
            ).all()
            
            published_count = 0
            for grade in grades:
                # التأكد من صلاحية المعلم
                if grade.recorder.user_id == teacher_id:
                    grade.publish_grade()
                    published_count += 1
            
            db.session.commit()
            
            return {
                'success': True,
                'published_count': published_count,
                'message': f'تم نشر {published_count} درجة وإرسال إشعارات لأولياء الأمور'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
