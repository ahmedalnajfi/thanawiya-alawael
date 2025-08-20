import React, { useState } from 'react';
import ExcelUpload from '../ExcelUpload';

const AdminDashboardSimple = ({ user, onLogout }) => {
  const [activeTab, setActiveTab] = useState('excel');

  const handleExcelUpload = (result) => {
    console.log('Excel upload result:', result);
    alert(`تم رفع ${result.count} ${result.type === 'students' ? 'طالب' : 'شعبة'} بنجاح!`);
  };

  const renderExcel = () => {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold">📊 رفع البيانات من Excel</h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* رفع بيانات الطلاب */}
          <div>
            <h3 className="text-xl font-semibold mb-4">👥 رفع بيانات الطلاب</h3>
            <ExcelUpload 
              type="students" 
              onUpload={handleExcelUpload}
            />
          </div>
          
          {/* رفع بيانات الشعب */}
          <div>
            <h3 className="text-xl font-semibold mb-4">🏫 رفع بيانات الشعب</h3>
            <ExcelUpload 
              type="classes" 
              onUpload={handleExcelUpload}
            />
          </div>
        </div>
        
        {/* إرشادات عامة */}
        <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
          <h4 className="font-bold text-blue-900 mb-3">📋 إرشادات عامة لرفع البيانات</h4>
          <div className="text-blue-800 space-y-2">
            <p>• قم بتحميل القالب المناسب أولاً من كل قسم</p>
            <p>• املأ البيانات بدقة وتأكد من عدم ترك خلايا فارغة في الحقول المطلوبة</p>
            <p>• استخدم التنسيق الصحيح للتواريخ (DD/MM/YYYY)</p>
            <p>• تأكد من صحة أرقام الهواتف والهويات</p>
            <p>• احفظ الملف بصيغة .xlsx للحصول على أفضل النتائج</p>
            <p>• يمكنك رفع عدة ملفات في أوقات مختلفة</p>
            <p>• سيتم دمج البيانات الجديدة مع البيانات الموجودة</p>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50" dir="rtl">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <img src="/logo.jpeg" alt="صُـنّاع الأوائل" className="w-10 h-10 rounded-full" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">صُـنّاع الأوائل</h1>
                <p className="text-sm text-gray-600">لوحة إدارة المدرسة</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">د. {user?.name || 'عبدالرحمن المدير'}</span>
              <span className="text-xs text-gray-500">مدير المدرسة</span>
              <button 
                onClick={onLogout}
                className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 text-sm"
              >
                تسجيل الخروج
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {renderExcel()}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <div className="flex justify-center items-center gap-2 mb-4">
              <img src="/logo.jpeg" alt="صُـنّاع الأوائل" className="w-12 h-12 rounded-full" />
              <h3 className="text-xl font-bold text-gray-900">صُـنّاع الأوائل</h3>
            </div>
            <p className="text-gray-600 mb-2">مدارس صُـنّاع الأوائل الثانوية الأهلية</p>
            <p className="text-gray-600 mb-2">📍 النجف الأشرف – شارع الإسكان / مقابل مستشفى الزهراء التعليمي</p>
            <p className="text-gray-600 mb-4">حي السلام – شارع كراج بغداد – خلف أثاث أنطاكيا</p>
            <div className="flex justify-center gap-6 text-sm text-gray-600">
              <span>📞 الإدارة: 07802814111</span>
              <span>📞 البنين: 07861890091</span>
              <span>📞 البنات: 07840008233</span>
            </div>
            <p className="text-xs text-gray-500 mt-4">© 2024 صُـنّاع الأوائل - جميع الحقوق محفوظة</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default AdminDashboardSimple;

