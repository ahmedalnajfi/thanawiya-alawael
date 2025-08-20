import React, { useState, useEffect } from 'react';
import { 
  BookOpen, Calendar, Clock, GraduationCap, User, 
  FileText, CheckCircle, AlertCircle, TrendingUp,
  Bell, Settings, LogOut, Home, PieChart,
  Users, Target, Award, Bookmark, Calendar as CalendarIcon,
  ClipboardList, BarChart3, Eye, Download, Upload
} from 'lucide-react';

const StudentDashboard = ({ user, onLogout }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(false);
  const [dashboardData, setDashboardData] = useState({
    overview: null,
    assignments: [],
    exams: [],
    grades: [],
    schedule: null,
    attendance: null,
    settings: null
  });
  const [notifications, setNotifications] = useState([]);

  // Mock API call function (replace with real API calls)
  const fetchData = async (endpoint) => {
    setLoading(true);
    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Mock data for demonstration
      const mockData = {
        overview: {
          student_info: {
            name: 'أحمد محمد علي',
            student_id: 'ST2024001',
            class_name: '3أ'
          },
          classroom: { 
            name: '3أ - علمي',
            grade_level: '12',
            section: 'علمي'
          },
          overview: {
            upcoming_exams_count: 3,
            pending_assignments_count: 5,
            attendance_rate: 92.5,
            recent_grades_count: 8
          },
          recent_grades: [
            { id: 1, subject: 'الرياضيات', grade: 85, percentage: 85, grade_letter: 'A' },
            { id: 2, subject: 'الفيزياء', grade: 78, percentage: 78, grade_letter: 'B+' },
            { id: 3, subject: 'الكيمياء', grade: 92, percentage: 92, grade_letter: 'A+' }
          ]
        },
        assignments: [
          {
            id: 1,
            title: 'واجب الرياضيات - الفصل الثالث',
            description: 'حل المسائل من 1 إلى 20',
            due_date: '2024-08-25T23:59:59',
            assignment_type: 'homework',
            course: { subject: { name: 'الرياضيات' } },
            is_submitted: false,
            is_overdue: false
          },
          {
            id: 2,
            title: 'بحث في الفيزياء - الحركة',
            description: 'بحث عن قوانين الحركة',
            due_date: '2024-08-28T23:59:59',
            assignment_type: 'project',
            course: { subject: { name: 'الفيزياء' } },
            is_submitted: true,
            submission: { grade: 88, feedback: 'عمل ممتاز' }
          }
        ],
        exams: [
          {
            id: 1,
            title: 'امتحان شهري - الرياضيات',
            exam_date: '2024-08-30',
            start_time: '08:00',
            end_time: '10:00',
            location: 'قاعة A',
            subject: { name: 'الرياضيات' },
            exam_type: 'شهري',
            is_upcoming: true
          },
          {
            id: 2,
            title: 'اختبار قصير - الكيمياء',
            exam_date: '2024-09-02',
            start_time: '10:00',
            end_time: '11:00',
            location: 'مختبر الكيمياء',
            subject: { name: 'الكيمياء' },
            exam_type: 'يومي',
            is_upcoming: true
          }
        ],
        schedule: {
          'الأحد': [
            { period_number: 1, start_time: '08:00', end_time: '08:45', course: { subject: { name: 'الرياضيات' } }, teacher: { user: { name: 'أ. محمد أحمد' } } },
            { period_number: 2, start_time: '08:45', end_time: '09:30', course: { subject: { name: 'الفيزياء' } }, teacher: { user: { name: 'أ. فاطمة علي' } } }
          ],
          'الإثنين': [
            { period_number: 1, start_time: '08:00', end_time: '08:45', course: { subject: { name: 'الكيمياء' } }, teacher: { user: { name: 'أ. سارة محمد' } } },
            { period_number: 2, start_time: '08:45', end_time: '09:30', course: { subject: { name: 'العربي' } }, teacher: { user: { name: 'أ. أحمد حسن' } } }
          ]
        },
        grades: [
          { id: 1, score: 85, max_score: 100, percentage: 85, grade_letter: 'A', grade_system: { course: { subject: { name: 'الرياضيات' } }, grade_type: 'شهري' }, recorded_date: '2024-08-15' },
          { id: 2, score: 78, max_score: 100, percentage: 78, grade_letter: 'B+', grade_system: { course: { subject: { name: 'الفيزياء' } }, grade_type: 'يومي' }, recorded_date: '2024-08-12' }
        ]
      };
      
      return mockData[endpoint] || null;
    } catch (error) {
      console.error('Error fetching data:', error);
      return null;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Load initial data based on active tab
    loadTabData(activeTab);
  }, [activeTab]);

  const loadTabData = async (tab) => {
    const data = await fetchData(tab);
    if (data) {
      setDashboardData(prev => ({ ...prev, [tab]: data }));
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ar-SA', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatTime = (timeString) => {
    return timeString || 'غير محدد';
  };

  const getGradeColor = (percentage) => {
    if (percentage >= 90) return 'text-green-600 bg-green-50';
    if (percentage >= 80) return 'text-blue-600 bg-blue-50';
    if (percentage >= 70) return 'text-yellow-600 bg-yellow-50';
    if (percentage >= 60) return 'text-orange-600 bg-orange-50';
    return 'text-red-600 bg-red-50';
  };

  const getAssignmentStatusColor = (assignment) => {
    if (assignment.is_submitted) return 'text-green-600 bg-green-50';
    if (assignment.is_overdue) return 'text-red-600 bg-red-50';
    return 'text-yellow-600 bg-yellow-50';
  };

  const getAssignmentStatusText = (assignment) => {
    if (assignment.is_submitted) return 'مُسلم';
    if (assignment.is_overdue) return 'متأخر';
    return 'معلق';
  };

  const StatCard = ({ icon: Icon, title, value, color, subtitle }) => (
    <div className="bg-white rounded-lg shadow-md p-6 border-r-4" style={{ borderColor: color }}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-600 text-sm font-medium">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {subtitle && <p className="text-gray-500 text-xs">{subtitle}</p>}
        </div>
        <div className="rounded-full p-3" style={{ backgroundColor: color + '20' }}>
          <Icon className="w-6 h-6" style={{ color }} />
        </div>
      </div>
    </div>
  );

  const TabButton = ({ id, label, icon: Icon, isActive, onClick }) => (
    <button
      onClick={() => onClick(id)}
      className={`flex items-center space-x-2 space-x-reverse px-4 py-2 rounded-lg transition-colors ${
        isActive 
          ? 'bg-blue-600 text-white' 
          : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
      }`}
    >
      <Icon className="w-5 h-5" />
      <span className="font-medium">{label}</span>
    </button>
  );

  const renderOverview = () => {
    const data = dashboardData.overview;
    if (!data) return <div className="text-center py-8">جاري التحميل...</div>;

    return (
      <div className="space-y-6">
        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-800 rounded-lg p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold">مرحباً، {data.student_info?.name}</h1>
              <p className="opacity-90">رقم الطالب: {data.student_info?.student_id}</p>
              <p className="opacity-90">الفصل: {data.classroom?.name}</p>
            </div>
            <div className="text-right">
              <p className="text-lg font-semibold">{new Date().toLocaleDateString('ar-SA')}</p>
              <p className="opacity-90">{new Date().toLocaleDateString('ar-SA', { weekday: 'long' })}</p>
            </div>
          </div>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            icon={Calendar}
            title="الامتحانات القادمة"
            value={data.overview?.upcoming_exams_count || 0}
            color="#EF4444"
            subtitle="خلال الأسبوعين القادمين"
          />
          <StatCard
            icon={FileText}
            title="الواجبات المعلقة"
            value={data.overview?.pending_assignments_count || 0}
            color="#F59E0B"
            subtitle="يجب تسليمها قريباً"
          />
          <StatCard
            icon={TrendingUp}
            title="نسبة الحضور"
            value={`${data.overview?.attendance_rate || 0}%`}
            color="#10B981"
            subtitle="آخر 30 يوم"
          />
          <StatCard
            icon={Award}
            title="الدرجات الحديثة"
            value={data.overview?.recent_grades_count || 0}
            color="#8B5CF6"
            subtitle="آخر الدرجات المنشورة"
          />
        </div>

        {/* Recent Grades */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
            <Award className="w-5 h-5 ml-2 text-purple-600" />
            آخر الدرجات
          </h2>
          <div className="space-y-3">
            {data.recent_grades?.map(grade => (
              <div key={grade.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-semibold text-gray-900">{grade.subject}</p>
                  <p className="text-sm text-gray-600">الدرجة: {grade.grade} / {grade.max_score || 100}</p>
                </div>
                <div className="text-left">
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getGradeColor(grade.percentage)}`}>
                    {grade.grade_letter}
                  </span>
                  <p className="text-xs text-gray-500 mt-1">{grade.percentage}%</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const renderAssignments = () => {
    const assignments = dashboardData.assignments;
    if (!assignments) return <div className="text-center py-8">جاري التحميل...</div>;

    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900 flex items-center">
            <FileText className="w-6 h-6 ml-2 text-blue-600" />
            الواجبات
          </h1>
          <select className="border border-gray-300 rounded-lg px-3 py-2 text-sm">
            <option value="all">جميع الواجبات</option>
            <option value="pending">المعلقة</option>
            <option value="submitted">المُسلمة</option>
          </select>
        </div>

        <div className="grid gap-6">
          {assignments.map(assignment => (
            <div key={assignment.id} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-bold text-gray-900">{assignment.title}</h3>
                  <p className="text-gray-600 mt-1">{assignment.description}</p>
                  <div className="flex items-center mt-2 text-sm text-gray-500">
                    <BookOpen className="w-4 h-4 ml-1" />
                    <span>{assignment.course?.subject?.name}</span>
                    <span className="mx-2">•</span>
                    <span>{assignment.assignment_type === 'homework' ? 'واجب' : 'مشروع'}</span>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getAssignmentStatusColor(assignment)}`}>
                  {getAssignmentStatusText(assignment)}
                </span>
              </div>

              <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-200">
                <div className="flex items-center text-sm text-gray-600">
                  <Clock className="w-4 h-4 ml-1" />
                  <span>موعد التسليم: {formatDate(assignment.due_date)}</span>
                </div>
                <div className="flex space-x-2 space-x-reverse">
                  {assignment.is_submitted ? (
                    <div className="flex items-center text-green-600">
                      <CheckCircle className="w-4 h-4 ml-1" />
                      <span className="text-sm">تم التسليم</span>
                      {assignment.submission?.grade && (
                        <span className="mr-2 px-2 py-1 bg-green-100 text-green-800 rounded text-xs">
                          {assignment.submission.grade}%
                        </span>
                      )}
                    </div>
                  ) : (
                    <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm">
                      تسليم الواجب
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderExams = () => {
    const exams = dashboardData.exams;
    if (!exams) return <div className="text-center py-8">جاري التحميل...</div>;

    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900 flex items-center">
            <CalendarIcon className="w-6 h-6 ml-2 text-red-600" />
            الامتحانات
          </h1>
          <select className="border border-gray-300 rounded-lg px-3 py-2 text-sm">
            <option value="upcoming">القادمة</option>
            <option value="all">جميع الامتحانات</option>
            <option value="past">السابقة</option>
          </select>
        </div>

        <div className="grid gap-6">
          {exams.map(exam => (
            <div key={exam.id} className="bg-white rounded-lg shadow-md p-6 border-r-4 border-red-500">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-lg font-bold text-gray-900">{exam.title}</h3>
                  <div className="flex items-center mt-2 text-gray-600">
                    <BookOpen className="w-4 h-4 ml-1" />
                    <span>{exam.subject?.name}</span>
                    <span className="mx-2">•</span>
                    <span className="px-2 py-1 bg-gray-100 rounded text-xs">{exam.exam_type}</span>
                  </div>
                </div>
                {exam.is_upcoming && (
                  <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium">
                    قادم
                  </span>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4 pt-4 border-t border-gray-200">
                <div className="flex items-center text-sm text-gray-600">
                  <Calendar className="w-4 h-4 ml-1" />
                  <span>{formatDate(exam.exam_date)}</span>
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <Clock className="w-4 h-4 ml-1" />
                  <span>{formatTime(exam.start_time)} - {formatTime(exam.end_time)}</span>
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <Home className="w-4 h-4 ml-1" />
                  <span>{exam.location || 'غير محدد'}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderGrades = () => {
    const grades = dashboardData.grades;
    if (!grades) return <div className="text-center py-8">جاري التحميل...</div>;

    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900 flex items-center">
            <BarChart3 className="w-6 h-6 ml-2 text-purple-600" />
            الدرجات
          </h1>
          <div className="flex space-x-2 space-x-reverse">
            <select className="border border-gray-300 rounded-lg px-3 py-2 text-sm">
              <option value="">جميع المواد</option>
              <option value="math">الرياضيات</option>
              <option value="physics">الفيزياء</option>
              <option value="chemistry">الكيمياء</option>
            </select>
            <select className="border border-gray-300 rounded-lg px-3 py-2 text-sm">
              <option value="">جميع الأنواع</option>
              <option value="daily">يومي</option>
              <option value="weekly">أسبوعي</option>
              <option value="monthly">شهري</option>
            </select>
          </div>
        </div>

        <div className="grid gap-4">
          {grades.map(grade => (
            <div key={grade.id} className="bg-white rounded-lg shadow-md p-4">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-900">
                    {grade.grade_system?.course?.subject?.name}
                  </h4>
                  <p className="text-sm text-gray-600">
                    {grade.grade_system?.grade_type} • {formatDate(grade.recorded_date)}
                  </p>
                </div>
                <div className="text-left">
                  <div className={`px-4 py-2 rounded-lg ${getGradeColor(grade.percentage)}`}>
                    <span className="text-lg font-bold">{grade.grade_letter}</span>
                    <p className="text-sm">{grade.percentage}%</p>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    {grade.score} / {grade.max_score}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderSchedule = () => {
    const schedule = dashboardData.schedule;
    if (!schedule) return <div className="text-center py-8">جاري التحميل...</div>;

    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-gray-900 flex items-center">
          <CalendarIcon className="w-6 h-6 ml-2 text-green-600" />
          جدول الحصص
        </h1>

        <div className="space-y-4">
          {Object.entries(schedule).map(([day, periods]) => (
            <div key={day} className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="bg-green-600 text-white px-4 py-2">
                <h3 className="font-semibold">{day}</h3>
              </div>
              <div className="p-4">
                <div className="grid gap-3">
                  {periods.map((period, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center space-x-3 space-x-reverse">
                        <div className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm font-medium">
                          الحصة {period.period_number}
                        </div>
                        <div>
                          <p className="font-semibold text-gray-900">{period.course?.subject?.name}</p>
                          <p className="text-sm text-gray-600">{period.teacher?.user?.name}</p>
                        </div>
                      </div>
                      <div className="text-left text-sm text-gray-600">
                        <p>{formatTime(period.start_time)} - {formatTime(period.end_time)}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 rtl" dir="rtl">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4 space-x-reverse">
              <img src="/school-logo.jpeg" alt="School Logo" className="w-10 h-10 rounded-full" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">صُـنّاع الأوائل</h1>
                <p className="text-sm text-gray-600">بوابة الطالب</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4 space-x-reverse">
              <button className="relative p-2 text-gray-600 hover:text-blue-600">
                <Bell className="w-6 h-6" />
                {notifications.length > 0 && (
                  <span className="absolute -top-1 -right-1 bg-red-500 text-white rounded-full w-5 h-5 text-xs flex items-center justify-center">
                    {notifications.length}
                  </span>
                )}
              </button>
              <button 
                onClick={onLogout}
                className="flex items-center space-x-2 space-x-reverse px-4 py-2 text-gray-600 hover:text-red-600"
              >
                <LogOut className="w-5 h-5" />
                <span>تسجيل الخروج</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Sidebar Navigation */}
          <div className="lg:w-64 flex-shrink-0">
            <div className="bg-white rounded-lg shadow-md p-4">
              <nav className="space-y-2">
                <TabButton
                  id="overview"
                  label="نظرة عامة"
                  icon={Home}
                  isActive={activeTab === 'overview'}
                  onClick={setActiveTab}
                />
                <TabButton
                  id="assignments"
                  label="الواجبات"
                  icon={FileText}
                  isActive={activeTab === 'assignments'}
                  onClick={setActiveTab}
                />
                <TabButton
                  id="exams"
                  label="الامتحانات"
                  icon={CalendarIcon}
                  isActive={activeTab === 'exams'}
                  onClick={setActiveTab}
                />
                <TabButton
                  id="grades"
                  label="الدرجات"
                  icon={BarChart3}
                  isActive={activeTab === 'grades'}
                  onClick={setActiveTab}
                />
                <TabButton
                  id="schedule"
                  label="الجدول"
                  icon={Clock}
                  isActive={activeTab === 'schedule'}
                  onClick={setActiveTab}
                />
                <TabButton
                  id="attendance"
                  label="الحضور"
                  icon={Users}
                  isActive={activeTab === 'attendance'}
                  onClick={setActiveTab}
                />
                <hr className="my-4" />
                <TabButton
                  id="settings"
                  label="الإعدادات"
                  icon={Settings}
                  isActive={activeTab === 'settings'}
                  onClick={setActiveTab}
                />
              </nav>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1">
            {loading ? (
              <div className="bg-white rounded-lg shadow-md p-8">
                <div className="flex items-center justify-center space-x-2 space-x-reverse">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                  <span className="text-gray-600">جاري التحميل...</span>
                </div>
              </div>
            ) : (
              <>
                {activeTab === 'overview' && renderOverview()}
                {activeTab === 'assignments' && renderAssignments()}
                {activeTab === 'exams' && renderExams()}
                {activeTab === 'grades' && renderGrades()}
                {activeTab === 'schedule' && renderSchedule()}
                {activeTab === 'attendance' && (
                  <div className="bg-white rounded-lg shadow-md p-8 text-center">
                    <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">سجل الحضور</h3>
                    <p className="text-gray-600">قريباً سيتم عرض تفاصيل سجل الحضور والغياب</p>
                  </div>
                )}
                {activeTab === 'settings' && (
                  <div className="bg-white rounded-lg shadow-md p-8 text-center">
                    <Settings className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">الإعدادات</h3>
                    <p className="text-gray-600">قريباً سيتم توفير إعدادات الحساب والتفضيلات</p>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;
