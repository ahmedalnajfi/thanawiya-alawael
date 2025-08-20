from flask import Blueprint, request, jsonify, session
from src.models.user import db, Student, Parent, ParentStudent, AIInsight
from src.routes.auth import require_auth
from src.services.ai_service import AIService
from datetime import datetime

ai_bp = Blueprint('ai', __name__)
ai_service = AIService()

@ai_bp.route('/analyze-student/<int:student_id>', methods=['POST'])
@require_auth
def analyze_student_performance(student_id):
    """تحليل أداء الطالب باستخدام الذكاء الاصطناعي"""
    try:
        user_id = session['user_id']
        user_role = session['user_role']
        
        # التحقق من الصلاحيات
        if user_role == 'student':
            student = Student.query.filter_by(user_id=user_id, id=student_id).first()
            if not student:
                return jsonify({'error': 'غير مصرح للوصول'}), 403
        elif user_role == 'parent':
            parent = Parent.query.filter_by(user_id=user_id).first()
            if not parent:
                return jsonify({'error': 'ملف ولي الأمر غير موجود'}), 404
            
            relation = ParentStudent.query.filter_by(parent_id=parent.id, student_id=student_id).first()
            if not relation:
                return jsonify({'error': 'غير مصرح للوصول لبيانات هذا الطالب'}), 403
        elif user_role not in ['teacher', 'admin']:
            return jsonify({'error': 'غير مصرح'}), 403
        
        # تحليل أداء الطالب
        analysis_result = ai_service.analyze_student_performance(student_id)
        
        if not analysis_result:
            return jsonify({'error': 'فشل في تحليل أداء الطالب'}), 500
        
        return jsonify({
            'message': 'تم تحليل أداء الطالب بنجاح',
            'analysis': analysis_result['analysis'],
            'student_data': analysis_result['student_data'],
            'insight_id': analysis_result['insight_id']
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@ai_bp.route('/generate-report/<int:student_id>', methods=['POST'])
@require_auth
def generate_comprehensive_report(student_id):
    """إنتاج تقرير شامل للطالب"""
    try:
        user_id = session['user_id']
        user_role = session['user_role']
        
        # التحقق من الصلاحيات
        if user_role == 'student':
            student = Student.query.filter_by(user_id=user_id, id=student_id).first()
            if not student:
                return jsonify({'error': 'غير مصرح للوصول'}), 403
        elif user_role == 'parent':
            parent = Parent.query.filter_by(user_id=user_id).first()
            if not parent:
                return jsonify({'error': 'ملف ولي الأمر غير موجود'}), 404
            
            relation = ParentStudent.query.filter_by(parent_id=parent.id, student_id=student_id).first()
            if not relation:
                return jsonify({'error': 'غير مصرح للوصول لبيانات هذا الطالب'}), 403
        elif user_role not in ['teacher', 'admin']:
            return jsonify({'error': 'غير مصرح'}), 403
        
        # إنتاج التقرير الشامل
        report_result = ai_service.generate_comprehensive_report(student_id)
        
        if not report_result:
            return jsonify({'error': 'فشل في إنتاج التقرير الشامل'}), 500
        
        return jsonify({
            'message': 'تم إنتاج التقرير الشامل بنجاح',
            'report': report_result['report'],
            'statistics': report_result['statistics'],
            'student_info': report_result['student_info'],
            'generated_at': report_result['generated_at']
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@ai_bp.route('/risk-assessment/<int:student_id>', methods=['POST'])
@require_auth
def assess_academic_risk(student_id):
    """تقييم مخاطر الأداء الأكاديمي"""
    try:
        user_id = session['user_id']
        user_role = session['user_role']
        
        # التحقق من الصلاحيات (المعلمين والإدارة فقط)
        if user_role not in ['teacher', 'admin']:
            return jsonify({'error': 'غير مصرح - هذه الخدمة متاحة للمعلمين والإدارة فقط'}), 403
        
        # تقييم المخاطر
        risk_result = ai_service.predict_academic_risk(student_id)
        
        if not risk_result:
            return jsonify({'error': 'فشل في تقييم المخاطر الأكاديمية'}), 500
        
        return jsonify({
            'message': 'تم تقييم المخاطر الأكاديمية بنجاح',
            'risk_level': risk_result['risk_level'],
            'assessment': risk_result['assessment'],
            'risk_factors': risk_result['risk_factors'],
            'recommendations': risk_result['recommendations']
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@ai_bp.route('/recommendations/<int:student_id>', methods=['POST'])
@require_auth
def generate_personalized_recommendations(student_id):
    """إنتاج توصيات شخصية للطالب"""
    try:
        user_id = session['user_id']
        user_role = session['user_role']
        
        # التحقق من الصلاحيات
        if user_role == 'student':
            student = Student.query.filter_by(user_id=user_id, id=student_id).first()
            if not student:
                return jsonify({'error': 'غير مصرح للوصول'}), 403
        elif user_role == 'parent':
            parent = Parent.query.filter_by(user_id=user_id).first()
            if not parent:
                return jsonify({'error': 'ملف ولي الأمر غير موجود'}), 404
            
            relation = ParentStudent.query.filter_by(parent_id=parent.id, student_id=student_id).first()
            if not relation:
                return jsonify({'error': 'غير مصرح للوصول لبيانات هذا الطالب'}), 403
        elif user_role not in ['teacher', 'admin']:
            return jsonify({'error': 'غير مصرح'}), 403
        
        # إنتاج التوصيات الشخصية
        recommendations_result = ai_service.generate_personalized_recommendations(student_id)
        
        if not recommendations_result:
            return jsonify({'error': 'فشل في إنتاج التوصيات الشخصية'}), 500
        
        return jsonify({
            'message': 'تم إنتاج التوصيات الشخصية بنجاح',
            'recommendations': recommendations_result['recommendations'],
            'strengths': recommendations_result['strengths'],
            'weaknesses': recommendations_result['weaknesses'],
            'action_plan': recommendations_result['action_plan']
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@ai_bp.route('/insights/<int:student_id>', methods=['GET'])
@require_auth
def get_ai_insights(student_id):
    """الحصول على رؤى الذكاء الاصطناعي للطالب"""
    try:
        user_id = session['user_id']
        user_role = session['user_role']
        
        # التحقق من الصلاحيات
        if user_role == 'student':
            student = Student.query.filter_by(user_id=user_id, id=student_id).first()
            if not student:
                return jsonify({'error': 'غير مصرح للوصول'}), 403
        elif user_role == 'parent':
            parent = Parent.query.filter_by(user_id=user_id).first()
            if not parent:
                return jsonify({'error': 'ملف ولي الأمر غير موجود'}), 404
            
            relation = ParentStudent.query.filter_by(parent_id=parent.id, student_id=student_id).first()
            if not relation:
                return jsonify({'error': 'غير مصرح للوصول لبيانات هذا الطالب'}), 403
        elif user_role not in ['teacher', 'admin']:
            return jsonify({'error': 'غير مصرح'}), 403
        
        # الحصول على المعاملات
        insight_type = request.args.get('type')
        limit = request.args.get('limit', 10, type=int)
        
        # بناء الاستعلام
        query = AIInsight.query.filter_by(student_id=student_id, is_active=True)
        
        if insight_type:
            query = query.filter_by(insight_type=insight_type)
        
        insights = query.order_by(AIInsight.generated_at.desc()).limit(limit).all()
        insights_data = [insight.to_dict() for insight in insights]
        
        # تجميع حسب النوع
        insights_by_type = {}
        for insight in insights:
            if insight.insight_type not in insights_by_type:
                insights_by_type[insight.insight_type] = []
            insights_by_type[insight.insight_type].append(insight.to_dict())
        
        return jsonify({
            'insights': insights_data,
            'insights_by_type': insights_by_type,
            'total_count': len(insights_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@ai_bp.route('/insights/<int:insight_id>', methods=['DELETE'])
@require_auth
def delete_ai_insight(insight_id):
    """حذف رؤية ذكاء اصطناعي"""
    try:
        user_role = session['user_role']
        
        # فقط المعلمين والإدارة يمكنهم حذف الرؤى
        if user_role not in ['teacher', 'admin']:
            return jsonify({'error': 'غير مصرح'}), 403
        
        insight = AIInsight.query.get(insight_id)
        if not insight:
            return jsonify({'error': 'الرؤية غير موجودة'}), 404
        
        # تعطيل الرؤية بدلاً من حذفها
        insight.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'تم حذف الرؤية بنجاح'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@ai_bp.route('/batch-analysis', methods=['POST'])
@require_auth
def batch_analyze_students():
    """تحليل مجموعة من الطلاب"""
    try:
        user_role = session['user_role']
        
        # فقط المعلمين والإدارة يمكنهم إجراء التحليل المجمع
        if user_role not in ['teacher', 'admin']:
            return jsonify({'error': 'غير مصرح'}), 403
        
        data = request.get_json()
        student_ids = data.get('student_ids', [])
        analysis_type = data.get('analysis_type', 'performance')
        
        if not student_ids:
            return jsonify({'error': 'قائمة الطلاب مطلوبة'}), 400
        
        results = []
        
        for student_id in student_ids:
            try:
                if analysis_type == 'performance':
                    result = ai_service.analyze_student_performance(student_id)
                elif analysis_type == 'risk':
                    result = ai_service.predict_academic_risk(student_id)
                elif analysis_type == 'recommendations':
                    result = ai_service.generate_personalized_recommendations(student_id)
                else:
                    continue
                
                if result:
                    results.append({
                        'student_id': student_id,
                        'success': True,
                        'result': result
                    })
                else:
                    results.append({
                        'student_id': student_id,
                        'success': False,
                        'error': 'فشل في التحليل'
                    })
                    
            except Exception as e:
                results.append({
                    'student_id': student_id,
                    'success': False,
                    'error': str(e)
                })
        
        successful_analyses = len([r for r in results if r['success']])
        
        return jsonify({
            'message': f'تم تحليل {successful_analyses} من أصل {len(student_ids)} طالب',
            'results': results,
            'summary': {
                'total_students': len(student_ids),
                'successful_analyses': successful_analyses,
                'failed_analyses': len(student_ids) - successful_analyses
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

@ai_bp.route('/class-insights/<class_name>', methods=['GET'])
@require_auth
def get_class_insights(class_name):
    """الحصول على رؤى الصف الدراسي"""
    try:
        user_role = session['user_role']
        
        # فقط المعلمين والإدارة يمكنهم الوصول لرؤى الصف
        if user_role not in ['teacher', 'admin']:
            return jsonify({'error': 'غير مصرح'}), 403
        
        # الحصول على طلاب الصف
        students = Student.query.filter_by(class_name=class_name).all()
        
        if not students:
            return jsonify({'error': 'لا توجد طلاب في هذا الصف'}), 404
        
        class_insights = {
            'class_name': class_name,
            'total_students': len(students),
            'students_with_insights': 0,
            'risk_distribution': {'low': 0, 'medium': 0, 'high': 0},
            'recent_insights': []
        }
        
        # جمع الرؤى لكل طالب
        for student in students:
            student_insights = AIInsight.query.filter_by(
                student_id=student.id, 
                is_active=True
            ).order_by(AIInsight.generated_at.desc()).limit(3).all()
            
            if student_insights:
                class_insights['students_with_insights'] += 1
                
                # إضافة الرؤى الحديثة
                for insight in student_insights:
                    insight_data = insight.to_dict()
                    insight_data['student_name'] = student.user.name
                    insight_data['student_id_display'] = student.student_id
                    class_insights['recent_insights'].append(insight_data)
        
        # ترتيب الرؤى حسب التاريخ
        class_insights['recent_insights'].sort(
            key=lambda x: x['generated_at'], 
            reverse=True
        )
        class_insights['recent_insights'] = class_insights['recent_insights'][:20]
        
        return jsonify(class_insights), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في الخادم: {str(e)}'}), 500

