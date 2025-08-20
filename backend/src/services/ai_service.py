import openai
import json
from datetime import datetime, timedelta
from src.models.user import Student, Grade, Attendance, BehaviorNote, AIInsight, db
from sqlalchemy import func

class AIService:
    def __init__(self):
        # OpenAI client is already configured via environment variables
        self.client = openai.OpenAI()
    
    def analyze_student_performance(self, student_id):
        """تحليل شامل لأداء الطالب باستخدام الذكاء الاصطناعي"""
        try:
            student = Student.query.get(student_id)
            if not student:
                return None
            
            # جمع البيانات
            grades = Grade.query.filter_by(student_id=student_id).all()
            attendance_records = Attendance.query.filter_by(student_id=student_id).all()
            behavior_notes = BehaviorNote.query.filter_by(student_id=student_id).all()
            
            # تحضير البيانات للتحليل
            student_data = self._prepare_student_data(student, grades, attendance_records, behavior_notes)
            
            # إنشاء prompt للذكاء الاصطناعي
            prompt = self._create_analysis_prompt(student_data)
            
            # استدعاء OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "أنت مستشار تعليمي خبير متخصص في تحليل أداء الطلاب. قم بتحليل البيانات المقدمة وقدم رؤى عملية ومفيدة باللغة العربية."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            analysis_result = response.choices[0].message.content
            
            # حفظ النتيجة في قاعدة البيانات
            insight = AIInsight(
                student_id=student_id,
                insight_type='performance_analysis',
                content=analysis_result,
                confidence_score=0.85,
                generated_at=datetime.utcnow()
            )
            db.session.add(insight)
            db.session.commit()
            
            return {
                'analysis': analysis_result,
                'student_data': student_data,
                'insight_id': insight.id
            }
            
        except Exception as e:
            print(f"خطأ في تحليل أداء الطالب: {str(e)}")
            return None
    
    def generate_comprehensive_report(self, student_id):
        """إنتاج تقرير شامل للطالب"""
        try:
            student = Student.query.get(student_id)
            if not student:
                return None
            
            # جمع البيانات الشاملة
            grades = Grade.query.filter_by(student_id=student_id).all()
            attendance_records = Attendance.query.filter_by(student_id=student_id).all()
            behavior_notes = BehaviorNote.query.filter_by(student_id=student_id).all()
            
            # حساب الإحصائيات
            stats = self._calculate_statistics(grades, attendance_records, behavior_notes)
            
            # إنشاء prompt للتقرير الشامل
            prompt = self._create_report_prompt(student, stats)
            
            # استدعاء OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "أنت مستشار تعليمي خبير. قم بإنشاء تقرير شامل ومفصل عن أداء الطالب يتضمن التحليل والتوصيات والخطة العملية للتحسين. استخدم اللغة العربية الفصحى."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.6
            )
            
            report_content = response.choices[0].message.content
            
            # حفظ التقرير
            insight = AIInsight(
                student_id=student_id,
                insight_type='comprehensive_report',
                content=report_content,
                confidence_score=0.90,
                generated_at=datetime.utcnow()
            )
            db.session.add(insight)
            db.session.commit()
            
            return {
                'report': report_content,
                'statistics': stats,
                'student_info': {
                    'name': student.user.name,
                    'student_id': student.student_id,
                    'class': student.class_name
                },
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"خطأ في إنتاج التقرير الشامل: {str(e)}")
            return None
    
    def predict_academic_risk(self, student_id):
        """تقييم مخاطر الأداء الأكاديمي"""
        try:
            student = Student.query.get(student_id)
            if not student:
                return None
            
            # جمع البيانات الحديثة (آخر 3 أشهر)
            three_months_ago = datetime.utcnow() - timedelta(days=90)
            
            recent_grades = Grade.query.filter(
                Grade.student_id == student_id,
                Grade.date_recorded >= three_months_ago
            ).all()
            
            recent_attendance = Attendance.query.filter(
                Attendance.student_id == student_id,
                Attendance.date >= three_months_ago.date()
            ).all()
            
            recent_behavior = BehaviorNote.query.filter(
                BehaviorNote.student_id == student_id,
                BehaviorNote.date_recorded >= three_months_ago
            ).all()
            
            # تحليل المخاطر
            risk_factors = self._analyze_risk_factors(recent_grades, recent_attendance, recent_behavior)
            
            # إنشاء prompt لتقييم المخاطر
            prompt = self._create_risk_assessment_prompt(student, risk_factors)
            
            # استدعاء OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "أنت خبير في تقييم المخاطر الأكاديمية. قم بتحليل البيانات وتحديد مستوى المخاطر مع تقديم توصيات للتدخل المبكر باللغة العربية."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.5
            )
            
            risk_assessment = response.choices[0].message.content
            
            # تحديد مستوى المخاطر
            risk_level = self._determine_risk_level(risk_factors)
            
            # حفظ التقييم
            insight = AIInsight(
                student_id=student_id,
                insight_type='risk_assessment',
                content=risk_assessment,
                confidence_score=0.80,
                generated_at=datetime.utcnow()
            )
            db.session.add(insight)
            db.session.commit()
            
            return {
                'risk_level': risk_level,
                'assessment': risk_assessment,
                'risk_factors': risk_factors,
                'recommendations': self._get_risk_recommendations(risk_level)
            }
            
        except Exception as e:
            print(f"خطأ في تقييم المخاطر الأكاديمية: {str(e)}")
            return None
    
    def generate_personalized_recommendations(self, student_id):
        """إنتاج توصيات شخصية للطالب"""
        try:
            student = Student.query.get(student_id)
            if not student:
                return None
            
            # تحليل نقاط القوة والضعف
            strengths_weaknesses = self._analyze_strengths_weaknesses(student_id)
            
            # إنشاء prompt للتوصيات الشخصية
            prompt = self._create_recommendations_prompt(student, strengths_weaknesses)
            
            # استدعاء OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "أنت مستشار تعليمي متخصص في وضع خطط التحسين الشخصية. قدم توصيات عملية ومحددة وقابلة للتطبيق باللغة العربية."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.7
            )
            
            recommendations = response.choices[0].message.content
            
            # حفظ التوصيات
            insight = AIInsight(
                student_id=student_id,
                insight_type='personalized_recommendations',
                content=recommendations,
                confidence_score=0.85,
                generated_at=datetime.utcnow()
            )
            db.session.add(insight)
            db.session.commit()
            
            return {
                'recommendations': recommendations,
                'strengths': strengths_weaknesses['strengths'],
                'weaknesses': strengths_weaknesses['weaknesses'],
                'action_plan': self._create_action_plan(strengths_weaknesses)
            }
            
        except Exception as e:
            print(f"خطأ في إنتاج التوصيات الشخصية: {str(e)}")
            return None
    
    def _prepare_student_data(self, student, grades, attendance_records, behavior_notes):
        """تحضير بيانات الطالب للتحليل"""
        # حساب المعدل العام
        avg_grade = sum(grade.grade for grade in grades) / len(grades) if grades else 0
        
        # حساب نسبة الحضور
        total_days = len(attendance_records)
        present_days = len([a for a in attendance_records if a.status == 'present'])
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        # تحليل السلوك
        positive_behavior = len([n for n in behavior_notes if n.note_type == 'positive'])
        negative_behavior = len([n for n in behavior_notes if n.note_type == 'negative'])
        
        # تجميع الدرجات حسب المادة
        subjects_performance = {}
        for grade in grades:
            if grade.subject not in subjects_performance:
                subjects_performance[grade.subject] = []
            subjects_performance[grade.subject].append(grade.grade)
        
        for subject in subjects_performance:
            grades_list = subjects_performance[subject]
            subjects_performance[subject] = {
                'average': sum(grades_list) / len(grades_list),
                'count': len(grades_list),
                'trend': 'improving' if len(grades_list) >= 2 and grades_list[0] > grades_list[-1] else 'stable'
            }
        
        return {
            'student_info': {
                'name': student.user.name,
                'student_id': student.student_id,
                'class': student.class_name
            },
            'academic_performance': {
                'overall_average': round(avg_grade, 2),
                'subjects_performance': subjects_performance,
                'total_grades': len(grades)
            },
            'attendance': {
                'percentage': round(attendance_percentage, 2),
                'total_days': total_days,
                'present_days': present_days,
                'absent_days': total_days - present_days
            },
            'behavior': {
                'positive_notes': positive_behavior,
                'negative_notes': negative_behavior,
                'total_notes': len(behavior_notes)
            }
        }
    
    def _create_analysis_prompt(self, student_data):
        """إنشاء prompt لتحليل أداء الطالب"""
        return f"""
        قم بتحليل أداء الطالب التالي بناءً على البيانات المقدمة:
        
        معلومات الطالب:
        - الاسم: {student_data['student_info']['name']}
        - رقم الطالب: {student_data['student_info']['student_id']}
        - الصف: {student_data['student_info']['class']}
        
        الأداء الأكاديمي:
        - المعدل العام: {student_data['academic_performance']['overall_average']}
        - عدد الدرجات المسجلة: {student_data['academic_performance']['total_grades']}
        - أداء المواد: {json.dumps(student_data['academic_performance']['subjects_performance'], ensure_ascii=False)}
        
        الحضور:
        - نسبة الحضور: {student_data['attendance']['percentage']}%
        - إجمالي الأيام: {student_data['attendance']['total_days']}
        - أيام الحضور: {student_data['attendance']['present_days']}
        - أيام الغياب: {student_data['attendance']['absent_days']}
        
        السلوك:
        - ملاحظات إيجابية: {student_data['behavior']['positive_notes']}
        - ملاحظات سلبية: {student_data['behavior']['negative_notes']}
        - إجمالي الملاحظات: {student_data['behavior']['total_notes']}
        
        المطلوب:
        1. تحليل نقاط القوة والضعف
        2. تقييم الأداء العام
        3. تحديد المجالات التي تحتاج تحسين
        4. تقديم توصيات عملية
        """
    
    def _create_report_prompt(self, student, stats):
        """إنشاء prompt للتقرير الشامل"""
        return f"""
        أنشئ تقريراً شاملاً ومفصلاً عن الطالب {student.user.name} (رقم الطالب: {student.student_id}) في الصف {student.class_name}.
        
        الإحصائيات:
        {json.dumps(stats, ensure_ascii=False, indent=2)}
        
        يجب أن يتضمن التقرير:
        1. ملخص تنفيذي للأداء العام
        2. تحليل مفصل للأداء الأكاديمي
        3. تقييم الحضور والانتظام
        4. تحليل السلوك والمشاركة
        5. نقاط القوة والإنجازات
        6. المجالات التي تحتاج تطوير
        7. توصيات محددة للتحسين
        8. خطة عمل للفترة القادمة
        
        اجعل التقرير مهنياً ومفيداً للطالب وولي الأمر والمعلمين.
        """
    
    def _create_risk_assessment_prompt(self, student, risk_factors):
        """إنشاء prompt لتقييم المخاطر"""
        return f"""
        قم بتقييم المخاطر الأكاديمية للطالب {student.user.name} بناءً على البيانات الحديثة:
        
        عوامل المخاطر المحددة:
        {json.dumps(risk_factors, ensure_ascii=False, indent=2)}
        
        المطلوب:
        1. تحديد مستوى المخاطر (منخفض/متوسط/عالي)
        2. تحليل العوامل المؤثرة
        3. التنبؤ بالاتجاهات المستقبلية
        4. توصيات للتدخل المبكر
        5. خطة متابعة مقترحة
        """
    
    def _create_recommendations_prompt(self, student, strengths_weaknesses):
        """إنشاء prompt للتوصيات الشخصية"""
        return f"""
        ضع توصيات شخصية مفصلة للطالب {student.user.name} بناءً على تحليل نقاط القوة والضعف:
        
        نقاط القوة:
        {json.dumps(strengths_weaknesses['strengths'], ensure_ascii=False)}
        
        نقاط الضعف:
        {json.dumps(strengths_weaknesses['weaknesses'], ensure_ascii=False)}
        
        المطلوب:
        1. استراتيجيات لتعزيز نقاط القوة
        2. خطط لمعالجة نقاط الضعف
        3. أساليب دراسة مناسبة
        4. أنشطة إضافية مقترحة
        5. جدول زمني للتحسين
        6. مؤشرات قياس التقدم
        """
    
    def _calculate_statistics(self, grades, attendance_records, behavior_notes):
        """حساب الإحصائيات الشاملة"""
        # إحصائيات الدرجات
        grade_stats = {
            'total_grades': len(grades),
            'average': sum(grade.grade for grade in grades) / len(grades) if grades else 0,
            'highest': max(grade.grade for grade in grades) if grades else 0,
            'lowest': min(grade.grade for grade in grades) if grades else 0
        }
        
        # إحصائيات الحضور
        attendance_stats = {
            'total_days': len(attendance_records),
            'present': len([a for a in attendance_records if a.status == 'present']),
            'absent': len([a for a in attendance_records if a.status == 'absent']),
            'late': len([a for a in attendance_records if a.status == 'late']),
            'percentage': 0
        }
        
        if attendance_stats['total_days'] > 0:
            attendance_stats['percentage'] = (attendance_stats['present'] / attendance_stats['total_days']) * 100
        
        # إحصائيات السلوك
        behavior_stats = {
            'total_notes': len(behavior_notes),
            'positive': len([n for n in behavior_notes if n.note_type == 'positive']),
            'negative': len([n for n in behavior_notes if n.note_type == 'negative']),
            'neutral': len([n for n in behavior_notes if n.note_type == 'neutral'])
        }
        
        return {
            'grades': grade_stats,
            'attendance': attendance_stats,
            'behavior': behavior_stats
        }
    
    def _analyze_risk_factors(self, recent_grades, recent_attendance, recent_behavior):
        """تحليل عوامل المخاطر"""
        risk_factors = {
            'academic_decline': False,
            'poor_attendance': False,
            'behavioral_issues': False,
            'grade_trend': 'stable',
            'attendance_rate': 0,
            'negative_behavior_ratio': 0
        }
        
        # تحليل الاتجاه الأكاديمي
        if len(recent_grades) >= 3:
            recent_avg = sum(grade.grade for grade in recent_grades[-3:]) / 3
            older_avg = sum(grade.grade for grade in recent_grades[:-3]) / len(recent_grades[:-3]) if len(recent_grades) > 3 else recent_avg
            
            if recent_avg < older_avg - 5:
                risk_factors['academic_decline'] = True
                risk_factors['grade_trend'] = 'declining'
            elif recent_avg > older_avg + 5:
                risk_factors['grade_trend'] = 'improving'
        
        # تحليل الحضور
        if recent_attendance:
            present_days = len([a for a in recent_attendance if a.status == 'present'])
            attendance_rate = (present_days / len(recent_attendance)) * 100
            risk_factors['attendance_rate'] = attendance_rate
            
            if attendance_rate < 85:
                risk_factors['poor_attendance'] = True
        
        # تحليل السلوك
        if recent_behavior:
            negative_notes = len([n for n in recent_behavior if n.note_type == 'negative'])
            negative_ratio = (negative_notes / len(recent_behavior)) * 100
            risk_factors['negative_behavior_ratio'] = negative_ratio
            
            if negative_ratio > 30:
                risk_factors['behavioral_issues'] = True
        
        return risk_factors
    
    def _determine_risk_level(self, risk_factors):
        """تحديد مستوى المخاطر"""
        risk_score = 0
        
        if risk_factors['academic_decline']:
            risk_score += 3
        if risk_factors['poor_attendance']:
            risk_score += 2
        if risk_factors['behavioral_issues']:
            risk_score += 2
        
        if risk_score >= 5:
            return 'high'
        elif risk_score >= 3:
            return 'medium'
        else:
            return 'low'
    
    def _get_risk_recommendations(self, risk_level):
        """الحصول على توصيات حسب مستوى المخاطر"""
        recommendations = {
            'low': [
                'متابعة دورية للأداء',
                'تشجيع الاستمرار في الأداء الجيد',
                'تطوير المهارات الإضافية'
            ],
            'medium': [
                'متابعة أسبوعية مع المعلمين',
                'وضع خطة تحسين محددة',
                'تقديم الدعم الإضافي',
                'تواصل منتظم مع ولي الأمر'
            ],
            'high': [
                'تدخل فوري ومكثف',
                'اجتماع عاجل مع ولي الأمر',
                'وضع خطة تحسين شاملة',
                'متابعة يومية للأداء',
                'تقديم الدعم النفسي والأكاديمي'
            ]
        }
        
        return recommendations.get(risk_level, [])
    
    def _analyze_strengths_weaknesses(self, student_id):
        """تحليل نقاط القوة والضعف"""
        grades = Grade.query.filter_by(student_id=student_id).all()
        attendance_records = Attendance.query.filter_by(student_id=student_id).all()
        behavior_notes = BehaviorNote.query.filter_by(student_id=student_id).all()
        
        strengths = []
        weaknesses = []
        
        # تحليل الأداء الأكاديمي
        subjects_performance = {}
        for grade in grades:
            if grade.subject not in subjects_performance:
                subjects_performance[grade.subject] = []
            subjects_performance[grade.subject].append(grade.grade)
        
        for subject, grade_list in subjects_performance.items():
            avg = sum(grade_list) / len(grade_list)
            if avg >= 85:
                strengths.append(f'أداء ممتاز في مادة {subject}')
            elif avg < 70:
                weaknesses.append(f'يحتاج تحسين في مادة {subject}')
        
        # تحليل الحضور
        if attendance_records:
            present_days = len([a for a in attendance_records if a.status == 'present'])
            attendance_rate = (present_days / len(attendance_records)) * 100
            
            if attendance_rate >= 95:
                strengths.append('انتظام ممتاز في الحضور')
            elif attendance_rate < 85:
                weaknesses.append('يحتاج تحسين في الانتظام')
        
        # تحليل السلوك
        if behavior_notes:
            positive_notes = len([n for n in behavior_notes if n.note_type == 'positive'])
            negative_notes = len([n for n in behavior_notes if n.note_type == 'negative'])
            
            if positive_notes > negative_notes:
                strengths.append('سلوك إيجابي ومشاركة فعالة')
            elif negative_notes > positive_notes:
                weaknesses.append('يحتاج تحسين في السلوك')
        
        return {
            'strengths': strengths,
            'weaknesses': weaknesses
        }
    
    def _create_action_plan(self, strengths_weaknesses):
        """إنشاء خطة عمل"""
        action_plan = {
            'short_term': [],  # خطة قصيرة المدى (شهر)
            'medium_term': [], # خطة متوسطة المدى (فصل دراسي)
            'long_term': []    # خطة طويلة المدى (سنة دراسية)
        }
        
        # خطط قصيرة المدى
        if strengths_weaknesses['weaknesses']:
            action_plan['short_term'].append('تحديد المواد التي تحتاج تحسين فوري')
            action_plan['short_term'].append('وضع جدول دراسي يومي')
        
        # خطط متوسطة المدى
        action_plan['medium_term'].append('تقييم التقدم الشهري')
        action_plan['medium_term'].append('تطوير استراتيجيات دراسة جديدة')
        
        # خطط طويلة المدى
        action_plan['long_term'].append('تحقيق أهداف أكاديمية محددة')
        action_plan['long_term'].append('تطوير المهارات الشخصية والاجتماعية')
        
        return action_plan

