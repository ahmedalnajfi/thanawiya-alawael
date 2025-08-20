
import React, { useState } from 'react';
import ExcelUpload from '../ExcelUpload';

const AdminDashboard = ({ user, onLogout }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [formData, setFormData] = useState({});

  // بيانات تجريبية شاملة
  const [adminData, setAdminData] = useState({
    stats: {
      totalStudents: 450,
      totalTeachers: 25,
      totalParents: 380,
      totalClasses: 15,
      attendanceRate: 92.5,
      averageGrade: 78.3,
      tuitionCollection: 85.2,
      activeAlerts: 12
    },
    students: [
      {
        id: 'S001',
        name: 'أحمد محمد علي',
        class: '3أ',
        section: 'فرنسي',
        building: 'بناية البنين',
        parent: 'فاطمة أحمد',
        phone: '0501234567',
        tuitionTotal: 3000000,
        tuitionPaid: 2000000,
        status: 'نشط',
        grades: { math: 85, arabic: 78, french: 92, physics: 88 },
        attendance: 95,
        behavior: 'ممتاز'
      },
      {
        id: 'S002',
        name: 'فاطمة أحمد محمد',
        class: '3أ',
        section: 'غير فرنسي',
        building: 'بناية البنات',
        parent: 'محمد أحمد',
        phone: '0507654321',
        tuitionTotal: 3000000,
        tuitionPaid: 3000000,
        status: 'نشط',
        grades: { math: 92, arabic: 88, english: 85, chemistry: 90 },
        attendance: 98,
        behavior: 'ممتاز'
      }
    ],
    teachers: [
      {
        id: 'T001',
        name: 'د. محمد علي أحمد',
        subjects: ['الرياضيات', 'الفيزياء'],
        classes: ['3أ', '3ب', '2أ'],
        building: 'بناية البنين',
        email: 'mohamed.ali@school.edu',
        phone: '0501111111',
        salary: 1500000,
        status: 'نشط'
      },
      {
        id: 'T002',
        name: 'أ. فاطمة أحمد',
        subjects: ['اللغة العربية', 'التاريخ'],
        classes: ['3أ', '2ب'],
        building: 'بناية البنات',
        email: 'fatima.ahmed@school.edu',
        phone: '0502222222',
        salary: 1200000,
        status: 'نشط'
      }
    ],
    classes: [
      { id: 'C001', name: '3أ', section: 'فرنسي', building: 'بناية البنين', capacity: 30, enrolled: 28 },
      { id: 'C002', name: '3ب', section: 'غير فرنسي', building: 'بناية البنات', capacity: 30, enrolled: 25 }
    ],
    subjects: [
      { id: 'SUB001', name: 'الرياضيات', teacher: 'د. محمد علي أحمد', classes: ['3أ', '3ب'] },
      { id: 'SUB002', name: 'اللغة العربية', teacher: 'أ. فاطمة أحمد', classes: ['3أ', '2ب'] },
      { id: 'SUB003', name: 'اللغة الفرنسية', teacher: 'أ. سارة محمد', classes: ['3أ'] }
    ],
    tuitionSettings: {
      baseAmount: 3000000,
      frenchSectionExtra: 500000,
      discounts: { siblings: 10, excellence: 15, financial: 25 },
      paymentDeadlines: { first: '2024-09-15', second: '2024-01-15', third: '2024-04-15' }
    },
    announcements: [
      {
        id: 1,
        title: 'إجازة منتصف الفصل',
        content: 'ستبدأ إجازة منتصف الفصل الدراسي يوم الخميس القادم',
        target: 'الجميع',
        date: '2024-01-25',
        active: true
      }
    ]
  });

  const handleSave = (type, data) => {
    if (editingItem) {
      // تحديث العنصر الموجود
      setAdminData(prev => ({
        ...prev,
        [type]: prev[type].map(item => 
          item.id === editingItem.id ? { ...item, ...data } : item
        )
      }));
    } else {
      // إضافة عنصر جديد
      const newId = type.toUpperCase().substring(0, 3) + String(Date.now()).substring(-3);
      setAdminData(prev => ({
        ...prev,
        [type]: [...prev[type], { ...data, id: newId }]
      }));
    }
    setShowAddForm(false);
    setEditingItem(null);
    setFormData({});
    alert('تم الحفظ بنجاح!');
  };

  const handleDelete = (type, id) => {
    if (confirm('هل أنت متأكد من الحذف؟')) {
      setAdminData(prev => ({
        ...prev,
        [type]: prev[type].filter(item => item.id !== id)
      }));
      alert('تم الحذف بنجاح!');
    }
  };

  const handleEdit = (type, item) => {
    setEditingItem(item);
    setFormData(item);
    setShowAddForm(true);
  };

  const renderOverview = () => (
    <div className="space-y-6">
      {/* إحصائيات سريعة */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
          <h3 className="text-lg font-bold text-blue-900">إجمالي الطلاب</h3>
          <p className="text-3xl font-bold text-blue-600">{adminData.stats.totalStudents}</p>
        </div>
        <div className="bg-green-50 p-6 rounded-lg border border-green-200">
          <h3 className="text-lg font-bold text-green-900">المعلمون</h3>
          <p className="text-3xl font-bold text-green-600">{adminData.stats.totalTeachers}</p>
        </div>
        <div className="bg-purple-50 p-6 rounded-lg border border-purple-200">
          <h3 className="text-lg font-bold text-purple-900">نسبة الحضور</h3>
          <p className="text-3xl font-bold text-purple-600">{adminData.stats.attendanceRate}%</p>
        </div>
        <div className="bg-orange-50 p-6 rounded-lg border border-orange-200">
          <h3 className="text-lg font-bold text-orange-900">تحصيل الرسوم</h3>
          <p className="text-3xl font-bold text-orange-600">{adminData.stats.tuitionCollection}%</p>
        </div>
      </div>

      {/* تنبيهات مهمة */}
      <div className="bg-red-50 p-6 rounded-lg border border-red-200">
        <h3 className="text-xl font-bold text-red-900 mb-4">🚨 تنبيهات مهمة</h3>
        <div className="space-y-2">
          <div className="flex justify-between items-center p-3 bg-white rounded border">
            <span>عبدالله سالم - غياب متكرر (5 أيام)</span>
            <span className="bg-red-100 text-red-800 px-2 py-1 rounded text-sm">عالي</span>
          </div>
          <div className="flex justify-between items-center p-3 bg-white rounded border">
            <span>سارة أحمد - انخفاض الدرجات في الرياضيات</span>
            <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm">متوسط</span>
          </div>
          <div className="flex justify-between items-center p-3 bg-white rounded border">
            <span>محمد سالم - تأخر في دفع الرسوم</span>
            <span className="bg-red-100 text-red-800 px-2 py-1 rounded text-sm">عالي</span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderStudents = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">إدارة الطلاب</h2>
        <button 
          onClick={() => { setShowAddForm(true); setFormData({}); setEditingItem(null); }}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          + إضافة طالب جديد
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="border border-gray-300 p-3 text-right">الرقم</th>
              <th className="border border-gray-300 p-3 text-right">الاسم</th>
              <th className="border border-gray-300 p-3 text-right">الصف</th>
              <th className="border border-gray-300 p-3 text-right">الشعبة</th>
              <th className="border border-gray-300 p-3 text-right">البناية</th>
              <th className="border border-gray-300 p-3 text-right">ولي الأمر</th>
              <th className="border border-gray-300 p-3 text-right">الهاتف</th>
              <th className="border border-gray-300 p-3 text-right">الرسوم</th>
              <th className="border border-gray-300 p-3 text-right">الحالة</th>
              <th className="border border-gray-300 p-3 text-right">العمليات</th>
            </tr>
          </thead>
          <tbody>
            {adminData.students.map((student, index) => (
              <tr key={student.id} className="hover:bg-gray-50">
                <td className="border border-gray-300 p-3">{index + 1}</td>
                <td className="border border-gray-300 p-3">{student.name}</td>
                <td className="border border-gray-300 p-3">{student.class}</td>
                <td className="border border-gray-300 p-3">{student.section}</td>
                <td className="border border-gray-300 p-3">{student.building}</td>
                <td className="border border-gray-300 p-3">{student.parent}</td>
                <td className="border border-gray-300 p-3">{student.phone}</td>
                <td className="border border-gray-300 p-3">
                  {student.tuitionPaid.toLocaleString()} / {student.tuitionTotal.toLocaleString()} د.ع
                </td>
                <td className="border border-gray-300 p-3">
                  <span className={`px-2 py-1 rounded text-sm ${
                    student.status === 'نشط' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {student.status}
                  </span>
                </td>
                <td className="border border-gray-300 p-3">
                  <div className="flex gap-2">
                    <button 
                      onClick={() => handleEdit('students', student)}
                      className="bg-yellow-500 text-white px-2 py-1 rounded text-sm hover:bg-yellow-600"
                    >
                      تعديل
                    </button>
                    <button 
                      onClick={() => handleDelete('students', student.id)}
                      className="bg-red-500 text-white px-2 py-1 rounded text-sm hover:bg-red-600"
                    >
                      حذف
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderTeachers = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">إدارة المعلمين</h2>
        <button 
          onClick={() => { setShowAddForm(true); setFormData({}); setEditingItem(null); }}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          + إضافة معلم جديد
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="border border-gray-300 p-3 text-right">الرقم</th>
              <th className="border border-gray-300 p-3 text-right">الاسم</th>
              <th className="border border-gray-300 p-3 text-right">المواد</th>
              <th className="border border-gray-300 p-3 text-right">الصفوف</th>
              <th className="border border-gray-300 p-3 text-right">البناية</th>
              <th className="border border-gray-300 p-3 text-right">البريد الإلكتروني</th>
              <th className="border border-gray-300 p-3 text-right">الهاتف</th>
              <th className="border border-gray-300 p-3 text-right">الراتب (د.ع)</th>
              <th className="border border-gray-300 p-3 text-right">الحالة</th>
              <th className="border border-gray-300 p-3 text-right">العمليات</th>
            </tr>
          </thead>
          <tbody>
            {adminData.teachers.map((teacher, index) => (
              <tr key={teacher.id} className="hover:bg-gray-50">
                <td className="border border-gray-300 p-3">{index + 1}</td>
                <td className="border border-gray-300 p-3">{teacher.name}</td>
                <td className="border border-gray-300 p-3">{teacher.subjects.join(', ')}</td>
                <td className="border border-gray-300 p-3">{teacher.classes.join(', ')}</td>
                <td className="border border-gray-300 p-3">{teacher.building}</td>
                <td className="border border-gray-300 p-3">{teacher.email}</td>
                <td className="border border-gray-300 p-3">{teacher.phone}</td>
                <td className="border border-gray-300 p-3">{teacher.salary.toLocaleString()}</td>
                <td className="border border-gray-300 p-3">
                  <span className={`px-2 py-1 rounded text-sm ${
                    teacher.status === 'نشط' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {teacher.status}
                  </span>
                </td>
                <td className="border border-gray-300 p-3">
                  <div className="flex gap-2">
                    <button 
                      onClick={() => handleEdit('teachers', teacher)}
                      className="bg-yellow-500 text-white px-2 py-1 rounded text-sm hover:bg-yellow-600"
                    >
                      تعديل
                    </button>
                    <button 
                      onClick={() => handleDelete('teachers', teacher.id)}
                      className="bg-red-500 text-white px-2 py-1 rounded text-sm hover:bg-red-600"
                    >
                      حذف
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderTuition = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">إدارة الرسوم الدراسية</h2>
      
      {/* إعدادات الرسوم */}
      <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
        <h3 className="text-xl font-bold text-blue-900 mb-4">إعدادات الرسوم</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">الرسوم الأساسية (د.ع)</label>
            <input 
              type="number" 
              value={adminData.tuitionSettings.baseAmount}
              onChange={(e) => setAdminData(prev => ({
                ...prev,
                tuitionSettings: { ...prev.tuitionSettings, baseAmount: parseInt(e.target.value) }
              }))}
              className="w-full p-2 border rounded"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">رسوم إضافية للشعبة الفرنسية (د.ع)</label>
            <input 
              type="number" 
              value={adminData.tuitionSettings.frenchSectionExtra}
              onChange={(e) => setAdminData(prev => ({
                ...prev,
                tuitionSettings: { ...prev.tuitionSettings, frenchSectionExtra: parseInt(e.target.value) }
              }))}
              className="w-full p-2 border rounded"
            />
          </div>
        </div>
        
        <div className="mt-4">
          <h4 className="font-bold mb-2">خصومات متاحة (%)</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">خصم الأشقاء</label>
              <input 
                type="number" 
                value={adminData.tuitionSettings.discounts.siblings}
                onChange={(e) => setAdminData(prev => ({
                  ...prev,
                  tuitionSettings: { 
                    ...prev.tuitionSettings, 
                    discounts: { ...prev.tuitionSettings.discounts, siblings: parseInt(e.target.value) }
                  }
                }))}
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">خصم التفوق</label>
              <input 
                type="number" 
                value={adminData.tuitionSettings.discounts.excellence}
                onChange={(e) => setAdminData(prev => ({
                  ...prev,
                  tuitionSettings: { 
                    ...prev.tuitionSettings, 
                    discounts: { ...prev.tuitionSettings.discounts, excellence: parseInt(e.target.value) }
                  }
                }))}
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">خصم الحالة المالية</label>
              <input 
                type="number" 
                value={adminData.tuitionSettings.discounts.financial}
                onChange={(e) => setAdminData(prev => ({
                  ...prev,
                  tuitionSettings: { 
                    ...prev.tuitionSettings, 
                    discounts: { ...prev.tuitionSettings.discounts, financial: parseInt(e.target.value) }
                  }
                }))}
                className="w-full p-2 border rounded"
              />
            </div>
          </div>
        </div>

        <div className="mt-4">
          <h4 className="font-bold mb-2">مواعيد الدفع</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">الدفعة الأولى</label>
              <input 
                type="date" 
                value={adminData.tuitionSettings.paymentDeadlines.first}
                onChange={(e) => setAdminData(prev => ({
                  ...prev,
                  tuitionSettings: { 
                    ...prev.tuitionSettings, 
                    paymentDeadlines: { ...prev.tuitionSettings.paymentDeadlines, first: e.target.value }
                  }
                }))}
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">الدفعة الثانية</label>
              <input 
                type="date" 
                value={adminData.tuitionSettings.paymentDeadlines.second}
                onChange={(e) => setAdminData(prev => ({
                  ...prev,
                  tuitionSettings: { 
                    ...prev.tuitionSettings, 
                    paymentDeadlines: { ...prev.tuitionSettings.paymentDeadlines, second: e.target.value }
                  }
                }))}
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">الدفعة الثالثة</label>
              <input 
                type="date" 
                value={adminData.tuitionSettings.paymentDeadlines.third}
                onChange={(e) => setAdminData(prev => ({
                  ...prev,
                  tuitionSettings: { 
                    ...prev.tuitionSettings, 
                    paymentDeadlines: { ...prev.tuitionSettings.paymentDeadlines, third: e.target.value }
                  }
                }))}
                className="w-full p-2 border rounded"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderAnnouncements = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">إدارة الإعلانات</h2>
        <button 
          onClick={() => { setShowAddForm(true); setFormData({}); setEditingItem(null); }}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          + إضافة إعلان جديد
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="border border-gray-300 p-3 text-right">الرقم</th>
              <th className="border border-gray-300 p-3 text-right">العنوان</th>
              <th className="border border-gray-300 p-3 text-right">المحتوى</th>
              <th className="border border-gray-300 p-3 text-right">الجمهور المستهدف</th>
              <th className="border border-gray-300 p-3 text-right">التاريخ</th>
              <th className="border border-gray-300 p-3 text-right">الحالة</th>
              <th className="border border-gray-300 p-3 text-right">العمليات</th>
            </tr>
          </thead>
          <tbody>
            {adminData.announcements.map((announcement, index) => (
              <tr key={announcement.id} className="hover:bg-gray-50">
                <td className="border border-gray-300 p-3">{index + 1}</td>
                <td className="border border-gray-300 p-3">{announcement.title}</td>
                <td className="border border-gray-300 p-3">{announcement.content}</td>
                <td className="border border-gray-300 p-3">{announcement.target}</td>
                <td className="border border-gray-300 p-3">{announcement.date}</td>
                <td className="border border-gray-300 p-3">
                  <span className={`px-2 py-1 rounded text-sm ${
                    announcement.active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {announcement.active ? 'نشط' : 'غير نشط'}
                  </span>
                </td>
                <td className="border border-gray-300 p-3">
                  <div className="flex gap-2">
                    <button 
                      onClick={() => handleEdit('announcements', announcement)}
                      className="bg-yellow-500 text-white px-2 py-1 rounded text-sm hover:bg-yellow-600"
                    >
                      تعديل
                    </button>
                    <button 
                      onClick={() => handleDelete('announcements', announcement.id)}
                      className="bg-red-500 text-white px-2 py-1 rounded text-sm hover:bg-red-600"
                    >
                      حذف
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderExcel = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">رفع بيانات الطلاب والشعب عبر Excel</h2>
      <ExcelUpload />
    </div>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'overview':
        return renderOverview();
      case 'students':
        return renderStudents();
      case 'teachers':
        return renderTeachers();
      case 'tuition':
        return renderTuition();
      case 'announcements':
        return renderAnnouncements();
      case 'excel':
        return renderExcel();
      default:
        return renderOverview();
    }
  };

  const renderAddEditForm = () => {
    if (!showAddForm) return null;

    let fields = [];
    let title = '';
    let type = '';

    switch (activeTab) {
      case 'students':
        title = editingItem ? 'تعديل طالب' : 'إضافة طالب جديد';
        type = 'students';
        fields = [
          { name: 'name', label: 'الاسم', type: 'text' },
          { name: 'class', label: 'الصف', type: 'text' },
          { name: 'section', label: 'الشعبة', type: 'text' },
          { name: 'building', label: 'البناية', type: 'text' },
          { name: 'parent', label: 'ولي الأمر', type: 'text' },
          { name: 'phone', label: 'الهاتف', type: 'text' },
          { name: 'tuitionTotal', label: 'إجمالي الرسوم', type: 'number' },
          { name: 'tuitionPaid', label: 'الرسوم المدفوعة', type: 'number' },
          { name: 'status', label: 'الحالة', type: 'select', options: ['نشط', 'غير نشط'] },
          { name: 'grades', label: 'الدرجات (JSON)', type: 'textarea' },
          { name: 'attendance', label: 'نسبة الحضور', type: 'number' },
          { name: 'behavior', label: 'السلوك', type: 'text' },
        ];
        break;
      case 'teachers':
        title = editingItem ? 'تعديل معلم' : 'إضافة معلم جديد';
        type = 'teachers';
        fields = [
          { name: 'name', label: 'الاسم', type: 'text' },
          { name: 'subjects', label: 'المواد (مفصولة بفاصلة)', type: 'text' },
          { name: 'classes', label: 'الصفوف (مفصولة بفاصلة)', type: 'text' },
          { name: 'building', label: 'البناية', type: 'text' },
          { name: 'email', label: 'البريد الإلكتروني', type: 'email' },
          { name: 'phone', label: 'الهاتف', type: 'text' },
          { name: 'salary', label: 'الراتب', type: 'number' },
          { name: 'status', label: 'الحالة', type: 'select', options: ['نشط', 'غير نشط'] },
        ];
        break;
      case 'announcements':
        title = editingItem ? 'تعديل إعلان' : 'إضافة إعلان جديد';
        type = 'announcements';
        fields = [
          { name: 'title', label: 'العنوان', type: 'text' },
          { name: 'content', label: 'المحتوى', type: 'textarea' },
          { name: 'target', label: 'الجمهور المستهدف', type: 'select', options: ['الجميع', 'الطلاب', 'المعلمون', 'أولياء الأمور'] },
          { name: 'date', label: 'التاريخ', type: 'date' },
          { name: 'active', label: 'نشط', type: 'checkbox' },
        ];
        break;
      default:
        return null;
    }

    return (
      <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex justify-center items-center">
        <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-lg">
          <h2 className="text-2xl font-bold mb-4">{title}</h2>
          <form onSubmit={(e) => {
            e.preventDefault();
            const dataToSave = { ...formData };
            // معالجة الحقول الخاصة مثل الدرجات والمواد والصفوف
            if (dataToSave.grades && typeof dataToSave.grades === 'string') {
              try {
                dataToSave.grades = JSON.parse(dataToSave.grades);
              } catch (error) {
                alert('صيغة الدرجات غير صحيحة. يجب أن تكون JSON صالح.');
                return;
              }
            }
            if (dataToSave.subjects && typeof dataToSave.subjects === 'string') {
              dataToSave.subjects = dataToSave.subjects.split(',').map(s => s.trim());
            }
            if (dataToSave.classes && typeof dataToSave.classes === 'string') {
              dataToSave.classes = dataToSave.classes.split(',').map(c => c.trim());
            }
            handleSave(type, dataToSave);
          }} className="space-y-4">
            {fields.map(field => (
              <div key={field.name}>
                <label htmlFor={field.name} className="block text-sm font-medium text-gray-700">
                  {field.label}
                </label>
                {field.type === 'select' ? (
                  <select
                    id={field.name}
                    name={field.name}
                    value={formData[field.name] || ''}
                    onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
                  >
                    {field.options.map(option => (
                      <option key={option} value={option}>{option}</option>
                    ))}
                  </select>
                ) : field.type === 'textarea' ? (
                  <textarea
                    id={field.name}
                    name={field.name}
                    value={formData[field.name] || ''}
                    onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    rows="3"
                    className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
                  ></textarea>
                ) : field.type === 'checkbox' ? (
                  <input
                    type="checkbox"
                    id={field.name}
                    name={field.name}
                    checked={formData[field.name] || false}
                    onChange={(e) => setFormData({ ...formData, [field.name]: e.target.checked })}
                    className="mt-1"
                  />
                ) : (
                  <input
                    type={field.type}
                    id={field.name}
                    name={field.name}
                    value={formData[field.name] || ''}
                    onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    className="mt-1 block w-full p-2 border border-gray-300 rounded-md"
                  />
                )}
              </div>
            ))}
            <div className="flex justify-end space-x-2">
              <button
                type="button"
                onClick={() => { setShowAddForm(false); setEditingItem(null); setFormData({}); }}
                className="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400"
              >
                إلغاء
              </button>
              <button
                type="submit"
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                حفظ
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100 flex">
      {/* الشريط الجانبي */}
      <div className="w-64 bg-gradient-to-b from-blue-700 to-blue-900 text-white p-6 shadow-lg">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold">لوحة تحكم المدير</h1>
          <p className="text-blue-200">{user.username}</p>
        </div>
        <nav>
          <ul>
            <li className="mb-3">
              <button 
                onClick={() => setActiveTab('overview')}
                className={`w-full text-right py-2 px-4 rounded-lg transition duration-200 ${
                  activeTab === 'overview' ? 'bg-blue-600 font-bold' : 'hover:bg-blue-700'
                }`}
              >
                نظرة عامة
              </button>
            </li>
            <li className="mb-3">
              <button 
                onClick={() => setActiveTab('students')}
                className={`w-full text-right py-2 px-4 rounded-lg transition duration-200 ${
                  activeTab === 'students' ? 'bg-blue-600 font-bold' : 'hover:bg-blue-700'
                }`}
              >
                إدارة الطلاب
              </button>
            </li>
            <li className="mb-3">
              <button 
                onClick={() => setActiveTab('teachers')}
                className={`w-full text-right py-2 px-4 rounded-lg transition duration-200 ${
                  activeTab === 'teachers' ? 'bg-blue-600 font-bold' : 'hover:bg-blue-700'
                }`}
              >
                إدارة المعلمين
              </button>
            </li>
            <li className="mb-3">
              <button 
                onClick={() => setActiveTab('tuition')}
                className={`w-full text-right py-2 px-4 rounded-lg transition duration-200 ${
                  activeTab === 'tuition' ? 'bg-blue-600 font-bold' : 'hover:bg-blue-700'
                }`}
              >
                إدارة الرسوم الدراسية
              </button>
            </li>
            <li className="mb-3">
              <button 
                onClick={() => setActiveTab('announcements')}
                className={`w-full text-right py-2 px-4 rounded-lg transition duration-200 ${
                  activeTab === 'announcements' ? 'bg-blue-600 font-bold' : 'hover:bg-blue-700'
                }`}
              >
                إدارة الإعلانات
              </button>
            </li>
            <li className="mb-3">
              <button 
                onClick={() => setActiveTab('excel')}
                className={`w-full text-right py-2 px-4 rounded-lg transition duration-200 ${
                  activeTab === 'excel' ? 'bg-blue-600 font-bold' : 'hover:bg-blue-700'
                }`}
              >
                رفع Excel
              </button>
            </li>
            <li className="mt-8">
              <button 
                onClick={onLogout}
                className="w-full text-right py-2 px-4 rounded-lg bg-blue-500 hover:bg-blue-600 transition duration-200"
              >
                تسجيل الخروج
              </button>
            </li>
          </ul>
        </nav>
      </div>

      {/* المحتوى الرئيسي */}
      <div className="flex-1 p-8">
        {renderContent()}
        {renderAddEditForm()}
      </div>
    </div>
  );
};

export default AdminDashboard;


