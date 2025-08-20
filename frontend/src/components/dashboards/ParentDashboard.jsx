import React, { useState } from 'react';
import { 
  Bell, 
  LogOut, 
  BookOpen, 
  Calendar, 
  Heart, 
  CreditCard, 
  Brain,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
  DollarSign,
  User,
  Phone,
  MapPin
} from 'lucide-react';

const ParentDashboard = ({ user, onLogout }) => {
  const [activeTab, setActiveTab] = useState('الدرجات');
  const [showAIReport, setShowAIReport] = useState(false);

  // بيانات تجريبية محدثة
  const studentData = {
    name: 'أحمد محمد',
    studentId: 'S12345',
    class: 'السادس العلمي - أ',
    stream: 'علمي - فرنسي', // إضافة الشعبة
    building: 'بناية البنين', // إضافة البناية
    overallGrade: 85.8,
    attendanceRate: 91.4,
    tuitionBalance: 2000000, // بالدينار العراقي
    notifications: 2
  };

  const grades = [
    { subject: 'الرياضيات', grade: 85, total: 100, rank: 5 },
    { subject: 'الفيزياء', grade: 78, total: 100, rank: 2 },
    { subject: 'الكيمياء', grade: 92, total: 100, rank: 8 },
    { subject: 'اللغة العربية', grade: 88, total: 100, rank: -2 },
    { subject: 'اللغة الإنجليزية', grade: 90, total: 100, rank: 3 },
    { subject: 'اللغة الفرنسية', grade: 82, total: 100, rank: 1 } // إضافة الفرنسية
  ];

  const attendance = {
    totalDays: 93,
    presentDays: 85,
    absentDays: 5,
    lateDays: 3
  };

  const recentAbsences = [
    { date: '2024-01-20', reason: 'مريض', type: 'مبرر' },
    { date: '2024-01-15', reason: 'ظروف عائلية', type: 'غائب' }
  ];

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('ar-IQ', {
      style: 'currency',
      currency: 'IQD',
      minimumFractionDigits: 0
    }).format(amount).replace('IQD', 'د.ع');
  };

  const generateAIReport = () => {
    setShowAIReport(true);
  };

  const aiReport = `
تقرير الذكاء الاصطناعي - أحمد محمد
التاريخ: ${new Date().toLocaleDateString('ar-IQ')}

## التقييم العام: 85/100

## الأداء الأكاديمي
يظهر ابنك أداءً متميزاً في المواد العلمية، خاصة الكيمياء والرياضيات. 
هناك تحسن ملحوظ في الفيزياء مقارنة بالفصل السابق.

## التحليل الأكاديمي
- نقاط القوة: يتفوق في المواد العلمية خاصة الكيمياء
- قدرة ممتازة على حل المشكلات الرياضية
- تحسن مستمر في اللغة الفرنسية

## مجالات التحسين
- يحتاج إلى مزيد من التركيز على حل المشكلات
- قدرة على المشاركة أكثر في الأنشطة الصفية
- تحسين مستمر في الأداء

## نقاط القوة
- نقوة في المواد العلمية خاصة الكيمياء
- قدرة ممتازة على حل المشكلات الرياضية
- تحسن مستمر في اللغة الفرنسية

## مجالات التحسين
- يحتاج إلى تطوير مهارات إدارة الوقت
- قدرة على المشاركة أكثر في الأنشطة الصفية
- تحسين مستمر في الأداء

## التوصيات
1. تخصيص وقت إضافي لمراجعة الفيزياء
2. تشجيع المشاركة في الأنشطة اللاصفية
3. وضع جدول زمني منظم للدراسة

## الحالة النفسية والسلوكية
ابنك يعاني من ضعف بتركيزه أحياناً، لكنه يظهر تحسناً مستمراً في التفاعل مع زملائه.
  `;

  const renderTabContent = () => {
    switch(activeTab) {
      case 'الدرجات':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <BookOpen className="w-5 h-5" />
                الدرجات والأداء الأكاديمي
              </h3>
              <p className="text-gray-600 mb-4">متابعة تفصيلية لدرجات ابنك في جميع المواد</p>
              
              {grades.map((grade, index) => (
                <div key={index} className="flex items-center justify-between p-4 border-b last:border-b-0">
                  <div className="flex-1">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-medium">{grade.subject}</span>
                      <span className="text-lg font-bold">{grade.grade}/{grade.total}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full" 
                        style={{ width: `${(grade.grade / grade.total) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                  <div className="mr-4 text-right">
                    <div className={`flex items-center gap-1 ${grade.rank > 0 ? 'text-green-600' : grade.rank < 0 ? 'text-red-600' : 'text-gray-600'}`}>
                      {grade.rank > 0 ? <TrendingUp className="w-4 h-4" /> : grade.rank < 0 ? <AlertTriangle className="w-4 h-4" /> : <CheckCircle className="w-4 h-4" />}
                      <span className="text-sm">
                        {grade.rank > 0 ? `+${grade.rank}` : grade.rank < 0 ? grade.rank : 'مستقر'}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        );

      case 'الحضور':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Calendar className="w-5 h-5" />
                سجل الحضور والغيابات
              </h3>
              <p className="text-gray-600 mb-4">متابعة حضور ابنك من التفاصيل والأسباب</p>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div className="bg-green-50 p-4 rounded-lg text-center">
                  <div className="text-2xl font-bold text-green-600">{attendance.presentDays}</div>
                  <div className="text-sm text-green-700">أيام حضور</div>
                </div>
                <div className="bg-red-50 p-4 rounded-lg text-center">
                  <div className="text-2xl font-bold text-red-600">{attendance.absentDays}</div>
                  <div className="text-sm text-red-700">أيام غياب</div>
                </div>
                <div className="bg-yellow-50 p-4 rounded-lg text-center">
                  <div className="text-2xl font-bold text-yellow-600">{attendance.lateDays}</div>
                  <div className="text-sm text-yellow-700">مرات تأخير</div>
                </div>
                <div className="bg-blue-50 p-4 rounded-lg text-center">
                  <div className="text-2xl font-bold text-blue-600">{studentData.attendanceRate}%</div>
                  <div className="text-sm text-blue-700">نسبة الحضور الإجمالية</div>
                </div>
              </div>

              <div className="space-y-3">
                <h4 className="font-medium">الغيابات الأخيرة</h4>
                {recentAbsences.map((absence, index) => (
                  <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                    <div>
                      <div className="font-medium">{absence.date}</div>
                      <div className="text-sm text-gray-600">{absence.reason}</div>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs ${absence.type === 'مبرر' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {absence.type}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      case 'السلوك':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Heart className="w-5 h-5" />
                السلوك والمشاركة
              </h3>
              <p className="text-gray-600 mb-4">تقييم سلوك ابنك ومشاركته في الأنشطة المدرسية</p>
              
              <div className="space-y-4">
                <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <CheckCircle className="w-5 h-5 text-green-600" />
                    <span className="font-medium text-green-800">ملاحظة إيجابية</span>
                    <span className="text-sm text-gray-500">منذ 3 أيام</span>
                  </div>
                  <p className="text-green-700">مشاركة ممتازة في حصة الرياضيات وحل جميع التمارين بطريقة صحيحة</p>
                </div>
                
                <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Clock className="w-5 h-5 text-blue-600" />
                    <span className="font-medium text-blue-800">ملاحظة عامة</span>
                    <span className="text-sm text-gray-500">منذ أسبوع</span>
                  </div>
                  <p className="text-blue-700">يحتاج إلى تحسين في الانتباه أثناء الحصص الصباحية</p>
                </div>
              </div>
            </div>
          </div>
        );

      case 'الرسوم':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <CreditCard className="w-5 h-5" />
                الرسوم والمدفوعات
              </h3>
              <p className="text-gray-600 mb-4">متابعة حالة الرسوم الدراسية والمدفوعات</p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-red-50 p-6 rounded-lg border border-red-200">
                  <div className="flex items-center gap-2 mb-2">
                    <DollarSign className="w-6 h-6 text-red-600" />
                    <span className="font-semibold text-red-800">المبلغ المتبقي</span>
                  </div>
                  <div className="text-3xl font-bold text-red-600 mb-2">
                    {formatCurrency(studentData.tuitionBalance)}
                  </div>
                  <p className="text-sm text-red-700">موعد الاستحقاق: 15 فبراير 2024</p>
                </div>
                
                <div className="bg-green-50 p-6 rounded-lg border border-green-200">
                  <div className="flex items-center gap-2 mb-2">
                    <CheckCircle className="w-6 h-6 text-green-600" />
                    <span className="font-semibold text-green-800">المدفوعات</span>
                  </div>
                  <div className="text-3xl font-bold text-green-600 mb-2">
                    {formatCurrency(3000000)}
                  </div>
                  <p className="text-sm text-green-700">آخر دفعة: 1 يناير 2024</p>
                </div>
              </div>

              <div className="mt-6">
                <h4 className="font-medium mb-3">تاريخ المدفوعات</h4>
                <div className="space-y-2">
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                    <span>دفعة يناير 2024</span>
                    <span className="font-medium">{formatCurrency(1500000)}</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                    <span>دفعة ديسمبر 2023</span>
                    <span className="font-medium">{formatCurrency(1500000)}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      case 'رؤى الذكاء الاصطناعي':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Brain className="w-5 h-5" />
                تقرير الذكاء الاصطناعي الشامل
              </h3>
              <p className="text-gray-600 mb-4">احصل على تحليل ذكي مفصل لأداء ابنك مع توصيات مخصصة</p>
              
              <button
                onClick={generateAIReport}
                className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-lg hover:from-purple-700 hover:to-blue-700 transition-all duration-200 flex items-center gap-2"
              >
                <Brain className="w-5 h-5" />
                استخرج تقرير الذكاء الاصطناعي
              </button>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50" dir="rtl">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-4">
              <img 
                src="/school-logo.jpeg" 
                alt="صُـنّاع الأوائل" 
                className="w-10 h-10 rounded-full object-cover"
              />
              <div>
                <h1 className="text-xl font-bold text-gray-900">صُـنّاع الأوائل</h1>
                <p className="text-sm text-gray-500">لوحة ولي الأمر</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <button className="relative p-2 text-gray-600 hover:text-gray-900">
                <Bell className="w-6 h-6" />
                {studentData.notifications > 0 && (
                  <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {studentData.notifications}
                  </span>
                )}
              </button>
              
              <div className="flex items-center gap-2">
                <User className="w-8 h-8 text-gray-600" />
                <span className="text-sm font-medium">{user?.name || 'ولي الأمر'}</span>
              </div>
              
              <button
                onClick={onLogout}
                className="flex items-center gap-2 px-3 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              >
                <LogOut className="w-4 h-4" />
                تسجيل الخروج
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Student Info Card */}
        <div className="bg-white rounded-lg shadow mb-8 p-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">مرحباً، {user?.name || 'ولي الأمر'}</h2>
              <p className="text-gray-600">متابعة شاملة لأداء ابنك الأكاديمي والسلوكي</p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500">معلومات الطالب</div>
              <div className="font-semibold">{studentData.name}</div>
              <div className="text-sm text-gray-600">{studentData.class}</div>
              <div className="text-sm text-blue-600">{studentData.stream}</div>
              <div className="text-sm text-green-600">{studentData.building}</div>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">المعدل العام</p>
                <p className="text-2xl font-bold text-green-600">{studentData.overallGrade}%</p>
              </div>
              <TrendingUp className="w-8 h-8 text-green-600" />
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">نسبة الحضور</p>
                <p className="text-2xl font-bold text-blue-600">{studentData.attendanceRate}%</p>
              </div>
              <Calendar className="w-8 h-8 text-blue-600" />
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">المبلغ المتبقي</p>
                <p className="text-2xl font-bold text-red-600">{formatCurrency(studentData.tuitionBalance)}</p>
              </div>
              <DollarSign className="w-8 h-8 text-red-600" />
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">الإشعارات</p>
                <p className="text-2xl font-bold text-purple-600">{studentData.notifications}</p>
              </div>
              <Bell className="w-8 h-8 text-purple-600" />
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6" aria-label="Tabs">
              {['الدرجات', 'الحضور', 'السلوك', 'الرسوم', 'رؤى الذكاء الاصطناعي'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  {tab}
                </button>
              ))}
            </nav>
          </div>
          
          <div className="p-6">
            {renderTabContent()}
          </div>
        </div>

        {/* School Contact Info */}
        <div className="mt-8 bg-blue-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-4">معلومات التواصل</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="flex items-center gap-2 text-blue-800">
              <Phone className="w-4 h-4" />
              <span>الإدارة العامة: 07802814111</span>
            </div>
            <div className="flex items-center gap-2 text-blue-800">
              <Phone className="w-4 h-4" />
              <span>البنين: 07861890091</span>
            </div>
            <div className="flex items-center gap-2 text-blue-800">
              <Phone className="w-4 h-4" />
              <span>البنات: 07840008233</span>
            </div>
            <div className="flex items-center gap-2 text-blue-800 md:col-span-3">
              <MapPin className="w-4 h-4" />
              <span>النجف الأشرف – شارع الإسكان / مقابل مستشفى الزهراء التعليمي</span>
            </div>
            <div className="flex items-center gap-2 text-blue-800 md:col-span-3">
              <MapPin className="w-4 h-4" />
              <span>حي السلام – شارع كراج بغداد – خلف أثاث أنطاكيا</span>
            </div>
          </div>
        </div>
      </main>

      {/* AI Report Modal */}
      {showAIReport && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200 flex justify-between items-center">
              <h3 className="text-xl font-bold flex items-center gap-2">
                <Brain className="w-6 h-6 text-purple-600" />
                تقرير الذكاء الاصطناعي - {studentData.name}
              </h3>
              <button
                onClick={() => setShowAIReport(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                Close
              </button>
            </div>
            <div className="p-6">
              <div className="prose prose-sm max-w-none text-right" dir="rtl">
                <pre className="whitespace-pre-wrap font-sans text-gray-800 leading-relaxed">
                  {aiReport}
                </pre>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ParentDashboard;

