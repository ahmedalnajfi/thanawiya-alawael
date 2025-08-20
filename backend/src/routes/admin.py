from flask import Blueprint, request, jsonify, session
from src.models.user import db, User, Student, Teacher, Parent
from src.routes.auth import require_auth, require_role
import json
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@require_auth
@require_role('admin')
def get_all_users():
    """Get all users with pagination and filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        role_filter = request.args.get('role')
        search = request.args.get('search', '')
        
        query = User.query
        
        # Apply role filter
        if role_filter:
            query = query.filter(User.role == role_filter)
        
        # Apply search filter
        if search:
            query = query.filter(
                db.or_(
                    User.name.contains(search),
                    User.username.contains(search),
                    User.email.contains(search)
                )
            )
        
        # Paginate results
        users = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@admin_bp.route('/users', methods=['POST'])
@require_auth
@require_role('admin')
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'role', 'name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} مطلوب'}), 400
        
        # Validate role
        valid_roles = ['admin', 'teacher', 'parent', 'student']
        if data['role'] not in valid_roles:
            return jsonify({'error': 'نوع المستخدم غير صحيح'}), 400
        
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
            phone=data.get('phone'),
            is_active=data.get('is_active', True)
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.flush()  # Get user ID
        
        # Create role-specific profile
        profile = None
        if data['role'] == 'student':
            profile = Student(
                user_id=user.id,
                student_id=data.get('student_id', f'S{user.id:06d}'),
                class_name=data.get('class_name', ''),
                address=data.get('address'),
                emergency_contact=data.get('emergency_contact')
            )
            if data.get('date_of_birth'):
                try:
                    profile.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                except ValueError:
                    pass
            db.session.add(profile)
            
        elif data['role'] == 'teacher':
            profile = Teacher(
                user_id=user.id,
                teacher_id=data.get('teacher_id', f'T{user.id:06d}'),
                subjects=json.dumps(data.get('subjects', [])),
                classes=json.dumps(data.get('classes', [])),
                qualification=data.get('qualification')
            )
            if data.get('hire_date'):
                try:
                    profile.hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
                except ValueError:
                    pass
            db.session.add(profile)
            
        elif data['role'] == 'parent':
            profile = Parent(
                user_id=user.id,
                occupation=data.get('occupation'),
                relationship=data.get('relationship', 'parent')
            )
            db.session.add(profile)
        
        db.session.commit()
        
        return jsonify({
            'message': 'تم إنشاء المستخدم بنجاح',
            'user': user.to_dict(),
            'profile': profile.to_dict() if profile else None
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@require_auth
@require_role('admin')
def get_user(user_id):
    """Get a specific user by ID"""
    try:
        user = User.query.get_or_404(user_id)
        
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

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@require_auth
@require_role('admin')
def update_user(user_id):
    """Update a user"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        # Update user fields
        if 'username' in data:
            # Check if username is already taken by another user
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user and existing_user.id != user.id:
                return jsonify({'error': 'اسم المستخدم موجود بالفعل'}), 400
            user.username = data['username']
        
        if 'email' in data:
            # Check if email is already taken by another user
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != user.id:
                return jsonify({'error': 'البريد الإلكتروني موجود بالفعل'}), 400
            user.email = data['email']
        
        if 'name' in data:
            user.name = data['name']
        
        if 'phone' in data:
            user.phone = data['phone']
        
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        # Update role-specific profile
        if user.role == 'student':
            profile = Student.query.filter_by(user_id=user.id).first()
            if profile:
                if 'student_id' in data:
                    profile.student_id = data['student_id']
                if 'class_name' in data:
                    profile.class_name = data['class_name']
                if 'address' in data:
                    profile.address = data['address']
                if 'emergency_contact' in data:
                    profile.emergency_contact = data['emergency_contact']
                if 'date_of_birth' in data:
                    try:
                        profile.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                    except ValueError:
                        pass
        
        elif user.role == 'teacher':
            profile = Teacher.query.filter_by(user_id=user.id).first()
            if profile:
                if 'teacher_id' in data:
                    profile.teacher_id = data['teacher_id']
                if 'subjects' in data:
                    profile.subjects = json.dumps(data['subjects'])
                if 'classes' in data:
                    profile.classes = json.dumps(data['classes'])
                if 'qualification' in data:
                    profile.qualification = data['qualification']
                if 'hire_date' in data:
                    try:
                        profile.hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
                    except ValueError:
                        pass
        
        elif user.role == 'parent':
            profile = Parent.query.filter_by(user_id=user.id).first()
            if profile:
                if 'occupation' in data:
                    profile.occupation = data['occupation']
                if 'relationship' in data:
                    profile.relationship = data['relationship']
        
        db.session.commit()
        
        return jsonify({
            'message': 'تم تحديث المستخدم بنجاح',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@require_auth
@require_role('admin')
def delete_user(user_id):
    """Delete a user (soft delete by setting is_active to False)"""
    try:
        user = User.query.get_or_404(user_id)
        
        # Prevent admin from deleting themselves
        if user.id == session['user_id']:
            return jsonify({'error': 'لا يمكن حذف حسابك الخاص'}), 400
        
        # Soft delete by setting is_active to False
        user.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'تم حذف المستخدم بنجاح'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@admin_bp.route('/users/<int:user_id>/activate', methods=['POST'])
@require_auth
@require_role('admin')
def activate_user(user_id):
    """Activate a user"""
    try:
        user = User.query.get_or_404(user_id)
        user.is_active = True
        db.session.commit()
        
        return jsonify({'message': 'تم تفعيل المستخدم بنجاح'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@admin_bp.route('/stats', methods=['GET'])
@require_auth
@require_role('admin')
def get_stats():
    """Get system statistics"""
    try:
        stats = {
            'total_users': User.query.count(),
            'active_users': User.query.filter_by(is_active=True).count(),
            'students': User.query.filter_by(role='student').count(),
            'teachers': User.query.filter_by(role='teacher').count(),
            'parents': User.query.filter_by(role='parent').count(),
            'admins': User.query.filter_by(role='admin').count()
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

