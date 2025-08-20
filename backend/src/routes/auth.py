from flask import Blueprint, request, jsonify, session
from src.models.user import db, User, Student, Teacher, Parent
import json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'اسم المستخدم وكلمة المرور مطلوبان'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'الحساب غير نشط'}), 401
        
        # Store user session
        session['user_id'] = user.id
        session['user_role'] = user.role
        
        # Get role-specific profile
        profile = None
        if user.role == 'student':
            profile = Student.query.filter_by(user_id=user.id).first()
        elif user.role == 'teacher':
            profile = Teacher.query.filter_by(user_id=user.id).first()
        elif user.role == 'parent':
            profile = Parent.query.filter_by(user_id=user.id).first()
        
        response_data = {
            'user': user.to_dict(),
            'profile': profile.to_dict() if profile else None,
            'message': 'تم تسجيل الدخول بنجاح'
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        session.clear()
        return jsonify({'message': 'تم تسجيل الخروج بنجاح'}), 200
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'role', 'name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} مطلوب'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'اسم المستخدم موجود بالفعل'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'البريد الإلكتروني موجود بالفعل'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            role=data['role'],
            name=data['name'],
            phone=data.get('phone')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.flush()  # Get user ID
        
        # Create role-specific profile
        if data['role'] == 'student':
            student = Student(
                user_id=user.id,
                student_id=data.get('student_id', f'S{user.id:03d}'),
                class_name=data.get('class_name', ''),
                date_of_birth=data.get('date_of_birth'),
                address=data.get('address'),
                emergency_contact=data.get('emergency_contact')
            )
            db.session.add(student)
            
        elif data['role'] == 'teacher':
            teacher = Teacher(
                user_id=user.id,
                teacher_id=data.get('teacher_id', f'T{user.id:03d}'),
                subjects=json.dumps(data.get('subjects', [])),
                classes=json.dumps(data.get('classes', [])),
                qualification=data.get('qualification'),
                hire_date=data.get('hire_date')
            )
            db.session.add(teacher)
            
        elif data['role'] == 'parent':
            parent = Parent(
                user_id=user.id,
                occupation=data.get('occupation'),
                relationship=data.get('relationship', 'parent')
            )
            db.session.add(parent)
        
        db.session.commit()
        
        return jsonify({
            'message': 'تم إنشاء الحساب بنجاح',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'غير مصرح'}), 401
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'المستخدم غير موجود'}), 404
        
        # Get role-specific profile
        profile = None
        if user.role == 'student':
            profile = Student.query.filter_by(user_id=user.id).first()
        elif user.role == 'teacher':
            profile = Teacher.query.filter_by(user_id=user.id).first()
        elif user.role == 'parent':
            profile = Parent.query.filter_by(user_id=user.id).first()
        
        return jsonify({
            'user': user.to_dict(),
            'profile': profile.to_dict() if profile else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

def require_auth(f):
    """Decorator to require authentication"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'غير مصرح'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def require_role(role):
    """Decorator to require specific role"""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'غير مصرح'}), 401
            if session.get('user_role') != role:
                return jsonify({'error': 'غير مصرح للوصول'}), 403
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

