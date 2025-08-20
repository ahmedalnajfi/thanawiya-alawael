#!/usr/bin/env python3
"""
سكريبت تهيئة البيانات الأساسية لنظام إدارة الطلاب
Basic data seeding script for the Student Management System
"""

import os
import sys
from datetime import date, datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db, User
from src.models.extended_models import AcademicYear, Subject
from src.services.user_creation import UserCreationService
from src import create_app


def create_admin_user():
    """إنشاء مستخدم المدير الأساسي"""
    try:
        # Check if admin exists
        admin = User.query.filter_by(role='admin', username='admin').first()
        if admin:
            print("✅ مستخدم المدير موجود مسبقاً")
            return admin
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@thanawiya-school.com',
            name='مدير النظام',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')  # يجب تغييرها في الإنتاج
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ تم إنشاء مستخدم المدير بنجاح")
        print(f"   اسم المستخدم: admin")
        print(f"   كلمة المرور: admin123")
        print(f"   ⚠️  يرجى تغيير كلمة المرور في الإنتاج")
        
        return admin
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء مستخدم المدير: {e}")
        db.session.rollback()
        return None


def create_academic_year():
    """إنشاء السنة الأكاديمية الحالية"""
    try:
        current_year = AcademicYear.query.filter_by(is_current=True).first()
        if current_year:
            print(f"✅ السنة الأكاديمية الحالية موجودة: {current_year.year}")
            return current_year
        
        # Create current academic year
        academic_year = AcademicYear(
            year='2024-2025',
            start_date=date(2024, 9, 1),
            end_date=date(2025, 6, 30),
            is_current=True
        )
        
        db.session.add(academic_year)
        db.session.commit()
        
        print("✅ تم إنشاء السنة الأكاديمية 2024-2025")
        return academic_year
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء السنة الأكاديمية: {e}")
        db.session.rollback()
        return None


def create_basic_subjects():
    """إنشاء المواد الدراسية الأساسية"""
    subjects_data = [
        {
            'name': 'الرياضيات',
            'name_en': 'Mathematics',
            'code': 'MATH',
            'description': 'مادة الرياضيات للمرحلة الثانوية',
            'department': 'العلوم',
            'grade_levels': ['10', '11', '12']
        },
        {
            'name': 'اللغة العربية',
            'name_en': 'Arabic Language',
            'code': 'ARAB',
            'description': 'مادة اللغة العربية وآدابها',
            'department': 'اللغات',
            'grade_levels': ['10', '11', '12']
        },
        {
            'name': 'اللغة الإنجليزية',
            'name_en': 'English Language',
            'code': 'ENG',
            'description': 'مادة اللغة الإنجليزية',
            'department': 'اللغات',
            'grade_levels': ['10', '11', '12']
        },
        {
            'name': 'اللغة الفرنسية',
            'name_en': 'French Language',
            'code': 'FRE',
            'description': 'مادة اللغة الفرنسية (اختيارية)',
            'department': 'اللغات',
            'is_mandatory': False,
            'grade_levels': ['10', '11', '12']
        },
        {
            'name': 'الفيزياء',
            'name_en': 'Physics',
            'code': 'PHY',
            'description': 'مادة الفيزياء - القسم العلمي',
            'department': 'العلوم',
            'grade_levels': ['11', '12']
        },
        {
            'name': 'الكيمياء',
            'name_en': 'Chemistry',
            'code': 'CHEM',
            'description': 'مادة الكيمياء - القسم العلمي',
            'department': 'العلوم',
            'grade_levels': ['11', '12']
        },
        {
            'name': 'الأحياء',
            'name_en': 'Biology',
            'code': 'BIO',
            'description': 'مادة الأحياء - القسم العلمي',
            'department': 'العلوم',
            'grade_levels': ['11', '12']
        },
        {
            'name': 'التاريخ',
            'name_en': 'History',
            'code': 'HIST',
            'description': 'مادة التاريخ - القسم الأدبي',
            'department': 'الاجتماعيات',
            'grade_levels': ['10', '11', '12']
        },
        {
            'name': 'الجغرافيا',
            'name_en': 'Geography',
            'code': 'GEO',
            'description': 'مادة الجغرافيا - القسم الأدبي',
            'department': 'الاجتماعيات',
            'grade_levels': ['10', '11', '12']
        },
        {
            'name': 'التربية الإسلامية',
            'name_en': 'Islamic Education',
            'code': 'ISLAM',
            'description': 'مادة التربية الإسلامية',
            'department': 'الديانة',
            'grade_levels': ['10', '11', '12']
        }
    ]
    
    created_count = 0
    for subject_data in subjects_data:
        try:
            # Check if subject exists
            existing = Subject.query.filter_by(code=subject_data['code']).first()
            if existing:
                continue
            
            import json
            subject = Subject(
                name=subject_data['name'],
                name_en=subject_data['name_en'],
                code=subject_data['code'],
                description=subject_data['description'],
                department=subject_data['department'],
                is_mandatory=subject_data.get('is_mandatory', True),
                grade_levels=json.dumps(subject_data['grade_levels'], ensure_ascii=False),
                is_active=True
            )
            
            db.session.add(subject)
            created_count += 1
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء مادة {subject_data['name']}: {e}")
            continue
    
    try:
        db.session.commit()
        if created_count > 0:
            print(f"✅ تم إنشاء {created_count} مادة دراسية")
        else:
            print("✅ المواد الدراسية موجودة مسبقاً")
    except Exception as e:
        print(f"❌ خطأ في حفظ المواد الدراسية: {e}")
        db.session.rollback()


def create_sample_users():
    """إنشاء مستخدمين تجريبيين للاختبار"""
    print("\n🔧 إنشاء مستخدمين تجريبيين...")
    
    # Create sample teachers
    teachers_data = [
        {
            'name': 'أحمد محمد الأستاذ',
            'email': 'ahmed.teacher@thanawiya-school.com',
            'phone': '07701234567',
            'subjects': ['الرياضيات', 'الفيزياء'],
            'qualification': 'ماجستير في الرياضيات'
        },
        {
            'name': 'فاطمة علي المدرسة',
            'email': 'fatima.teacher@thanawiya-school.com',
            'phone': '07701234568',
            'subjects': ['اللغة العربية', 'التاريخ'],
            'qualification': 'بكالوريوس في اللغة العربية'
        }
    ]
    
    for teacher_data in teachers_data:
        result = UserCreationService.create_teacher_with_credentials(**teacher_data)
        if result['success']:
            creds = result['credentials']
            print(f"✅ معلم: {teacher_data['name']}")
            print(f"   اسم المستخدم: {creds['username']}")
            print(f"   كلمة المرور: {creds['password']}")
        else:
            print(f"❌ فشل في إنشاء المعلم {teacher_data['name']}: {result['error']}")
    
    # Create sample students
    students_data = [
        {
            'name': 'محمد أحمد الطالب',
            'email': 'mohammed.student@thanawiya-school.com',
            'phone': '07801234567',
            'class_name': '3أ',
            'date_of_birth': date(2006, 5, 15)
        },
        {
            'name': 'سارة علي الطالبة',
            'email': 'sara.student@thanawiya-school.com',
            'phone': '07801234568',
            'class_name': '3أ',
            'date_of_birth': date(2006, 8, 22)
        }
    ]
    
    for student_data in students_data:
        result = UserCreationService.create_student_with_credentials(**student_data)
        if result['success']:
            creds = result['credentials']
            print(f"✅ طالب: {student_data['name']}")
            print(f"   اسم المستخدم: {creds['username']}")
            print(f"   كلمة المرور: {creds['password']}")
        else:
            print(f"❌ فشل في إنشاء الطالب {student_data['name']}: {result['error']}")
    
    # Create sample parents
    parents_data = [
        {
            'name': 'أحمد الطالب والد محمد',
            'email': 'ahmed.parent@thanawiya-school.com',
            'phone': '07901234567',
            'occupation': 'مهندس',
            'relationship': 'father'
        }
    ]
    
    for parent_data in parents_data:
        result = UserCreationService.create_parent_with_credentials(**parent_data)
        if result['success']:
            creds = result['credentials']
            print(f"✅ ولي أمر: {parent_data['name']}")
            print(f"   اسم المستخدم: {creds['username']}")
            print(f"   كلمة المرور: {creds['password']}")
        else:
            print(f"❌ فشل في إنشاء ولي الأمر {parent_data['name']}: {result['error']}")


def main():
    """تشغيل سكريبت التهيئة"""
    print("🚀 بدء تهيئة البيانات الأساسية لنظام إدارة الطلاب...")
    print("=" * 60)
    
    # Create Flask app context
    app = create_app()
    with app.app_context():
        try:
            # Create all tables
            print("📊 إنشاء جداول قاعدة البيانات...")
            db.create_all()
            print("✅ تم إنشاء جداول قاعدة البيانات بنجاح")
            
            # Create admin user
            print("\n👤 إنشاء مستخدم المدير...")
            admin = create_admin_user()
            if not admin:
                return
            
            # Create academic year
            print("\n📅 إنشاء السنة الأكاديمية...")
            academic_year = create_academic_year()
            if not academic_year:
                return
            
            # Create subjects
            print("\n📚 إنشاء المواد الدراسية...")
            create_basic_subjects()
            
            # Create sample users
            create_sample_users()
            
            print("\n" + "=" * 60)
            print("🎉 تم إكمال تهيئة البيانات الأساسية بنجاح!")
            print("\n📋 ملخص بيانات تسجيل الدخول:")
            print("   المدير:")
            print("   - اسم المستخدم: admin")
            print("   - كلمة المرور: admin123")
            print("\n   للمستخدمين الآخرين، راجع المخرجات أعلاه أو")
            print("   استخدم واجهة المدير لعرض بيانات تسجيل الدخول المُنشأة تلقائياً")
            
        except Exception as e:
            print(f"❌ خطأ عام في تهيئة البيانات: {e}")
            return 1
    
    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
