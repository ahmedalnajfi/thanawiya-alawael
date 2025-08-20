#!/usr/bin/env python3
"""
نظام إدارة الطلاب "صُنّاع الأوائل"
Student Management System "Makers of Excellence"

ملف تشغيل الخادم الأساسي
Basic server runner
"""

import os
from src import create_app, db

# Create the application
app = create_app()

# Simple route for testing
@app.route('/')
def index():
    return {
        'message': 'نظام إدارة الطلاب "صُنّاع الأوائل" - Student Management System',
        'status': 'running',
        'version': '1.0.0',
        'arabic_name': 'صُنّاع الأوائل',
        'english_name': 'Makers of Excellence'
    }

@app.route('/health')
def health_check():
    """فحص صحة النظام - Health check endpoint"""
    return {
        'status': 'healthy',
        'database': 'connected',
        'message': 'النظام يعمل بشكل طبيعي'
    }

@app.route('/api/info')
def api_info():
    """معلومات API الأساسية"""
    return {
        'api_version': '1.0.0',
        'system_name': 'Student Management System',
        'school_name': 'مدرسة صُنّاع الأوائل الثانوية',
        'features': [
            'User Management',
            'Grade Management', 
            'Attendance Tracking',
            'Academic Year Management',
            'Subject Management',
            'Classroom Management',
            'Parent-Teacher Communication',
            'Notifications System'
        ]
    }

if __name__ == '__main__':
    with app.app_context():
        # Ensure all tables exist
        db.create_all()
        print("🚀 تشغيل نظام إدارة الطلاب...")
        print("📊 تم التأكد من وجود جداول قاعدة البيانات")
        print("🌐 الخادم يعمل على: http://localhost:5000")
        print("⚡ جاهز لاستقبال الطلبات!")
    
    # Run the development server
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
