"""Add extended models for enhanced student management system

Revision ID: 001
Revises: 
Create Date: 2025-01-17 08:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create user_credentials table
    op.create_table('user_credentials',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('generated_username', sa.String(length=50), nullable=False),
        sa.Column('generated_password', sa.String(length=20), nullable=False),
        sa.Column('password_changed', sa.Boolean(), default=False, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('viewed_by_admin', sa.Boolean(), default=False, nullable=True),
        sa.Column('viewed_at', sa.DateTime(), nullable=True),
        sa.Column('delivered_to_user', sa.Boolean(), default=False, nullable=True),
        sa.Column('delivered_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    
    # Create academic_years table
    op.create_table('academic_years',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('year', sa.String(length=10), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('is_current', sa.Boolean(), default=False, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('year')
    )
    
    # Create subjects table
    op.create_table('subjects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('name_en', sa.String(length=100), nullable=True),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('department', sa.String(length=50), nullable=True),
        sa.Column('is_mandatory', sa.Boolean(), default=True, nullable=True),
        sa.Column('grade_levels', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    
    # Create classrooms table
    op.create_table('classrooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('grade_level', sa.String(length=10), nullable=False),
        sa.Column('section', sa.String(length=20), nullable=True),
        sa.Column('academic_year_id', sa.Integer(), nullable=False),
        sa.Column('homeroom_teacher_id', sa.Integer(), nullable=True),
        sa.Column('capacity', sa.Integer(), default=30, nullable=True),
        sa.Column('building', sa.String(length=50), nullable=True),
        sa.Column('floor', sa.String(length=10), nullable=True),
        sa.Column('room_number', sa.String(length=10), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['academic_year_id'], ['academic_years.id'], ),
        sa.ForeignKeyConstraint(['homeroom_teacher_id'], ['teacher.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create courses table
    op.create_table('courses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('classroom_id', sa.Integer(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.Column('teacher_id', sa.Integer(), nullable=False),
        sa.Column('schedule_json', sa.Text(), nullable=True),
        sa.Column('credit_hours', sa.Integer(), default=1, nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['classroom_id'], ['classrooms.id'], ),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
        sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create enrollments table
    op.create_table('enrollments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('classroom_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('enrollment_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=20), default='active', nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['classroom_id'], ['classrooms.id'], ),
        sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('classroom_id', 'student_id', name='unique_enrollment')
    )
    
    # Create assignments table
    op.create_table('assignments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('assignment_type', sa.String(length=30), nullable=False),
        sa.Column('max_score', sa.Float(), default=100.0, nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('assigned_date', sa.DateTime(), nullable=True),
        sa.Column('attachments_json', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create grade_systems table
    op.create_table('grade_systems',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('grade_type', sa.String(length=20), nullable=False),
        sa.Column('frequency', sa.String(length=20), nullable=True),
        sa.Column('weight_percentage', sa.Float(), default=10.0, nullable=True),
        sa.Column('max_score', sa.Float(), default=100.0, nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('notify_parents', sa.Boolean(), default=True, nullable=True),
        sa.Column('auto_publish', sa.Boolean(), default=False, nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
        sa.ForeignKeyConstraint(['created_by'], ['teacher.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create student_grades table
    op.create_table('student_grades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('grade_system_id', sa.Integer(), nullable=False),
        sa.Column('assignment_id', sa.Integer(), nullable=True),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('max_score', sa.Float(), nullable=False),
        sa.Column('percentage', sa.Float(), nullable=True),
        sa.Column('grade_letter', sa.String(length=5), nullable=True),
        sa.Column('recorded_date', sa.Date(), nullable=True),
        sa.Column('recorded_by', sa.Integer(), nullable=False),
        sa.Column('recorded_at', sa.DateTime(), nullable=True),
        sa.Column('is_published', sa.Boolean(), default=False, nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('parent_notified', sa.Boolean(), default=False, nullable=True),
        sa.Column('parent_notified_at', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['assignment_id'], ['assignments.id'], ),
        sa.ForeignKeyConstraint(['grade_system_id'], ['grade_systems.id'], ),
        sa.ForeignKeyConstraint(['recorded_by'], ['teacher.id'], ),
        sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create attendance_records table
    op.create_table('attendance_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('classroom_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.Column('attendance_date', sa.Date(), nullable=False),
        sa.Column('period', sa.String(length=20), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('arrival_time', sa.Time(), nullable=True),
        sa.Column('departure_time', sa.Time(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('recorded_by', sa.Integer(), nullable=False),
        sa.Column('recorded_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['classroom_id'], ['classrooms.id'], ),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
        sa.ForeignKeyConstraint(['recorded_by'], ['teacher.id'], ),
        sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create notifications table
    op.create_table('notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('data_json', sa.Text(), nullable=True),
        sa.Column('priority', sa.String(length=20), default='normal', nullable=True),
        sa.Column('is_read', sa.Boolean(), default=False, nullable=True),
        sa.Column('read_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for better performance
    op.create_index('idx_user_credentials_user_id', 'user_credentials', ['user_id'])
    op.create_index('idx_classrooms_academic_year', 'classrooms', ['academic_year_id'])
    op.create_index('idx_classrooms_teacher', 'classrooms', ['homeroom_teacher_id'])
    op.create_index('idx_courses_classroom', 'courses', ['classroom_id'])
    op.create_index('idx_courses_subject', 'courses', ['subject_id'])
    op.create_index('idx_courses_teacher', 'courses', ['teacher_id'])
    op.create_index('idx_enrollments_classroom', 'enrollments', ['classroom_id'])
    op.create_index('idx_enrollments_student', 'enrollments', ['student_id'])
    op.create_index('idx_student_grades_student', 'student_grades', ['student_id'])
    op.create_index('idx_student_grades_grade_system', 'student_grades', ['grade_system_id'])
    op.create_index('idx_student_grades_published', 'student_grades', ['is_published'])
    op.create_index('idx_attendance_date', 'attendance_records', ['attendance_date'])
    op.create_index('idx_attendance_student', 'attendance_records', ['student_id'])
    op.create_index('idx_notifications_user', 'notifications', ['user_id'])
    op.create_index('idx_notifications_unread', 'notifications', ['user_id', 'is_read'])
    op.create_index('idx_notifications_created', 'notifications', ['created_at'])


def downgrade() -> None:
    # Drop indexes first
    op.drop_index('idx_notifications_created')
    op.drop_index('idx_notifications_unread')
    op.drop_index('idx_notifications_user')
    op.drop_index('idx_attendance_student')
    op.drop_index('idx_attendance_date')
    op.drop_index('idx_student_grades_published')
    op.drop_index('idx_student_grades_grade_system')
    op.drop_index('idx_student_grades_student')
    op.drop_index('idx_enrollments_student')
    op.drop_index('idx_enrollments_classroom')
    op.drop_index('idx_courses_teacher')
    op.drop_index('idx_courses_subject')
    op.drop_index('idx_courses_classroom')
    op.drop_index('idx_classrooms_teacher')
    op.drop_index('idx_classrooms_academic_year')
    op.drop_index('idx_user_credentials_user_id')
    
    # Drop tables in reverse order of creation (considering foreign key dependencies)
    op.drop_table('notifications')
    op.drop_table('attendance_records')
    op.drop_table('student_grades')
    op.drop_table('grade_systems')
    op.drop_table('assignments')
    op.drop_table('enrollments')
    op.drop_table('courses')
    op.drop_table('classrooms')
    op.drop_table('subjects')
    op.drop_table('academic_years')
    op.drop_table('user_credentials')
