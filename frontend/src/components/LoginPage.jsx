import React, { useState } from 'react';
import { GraduationCap, User, Lock, Phone, MapPin } from 'lucide-react';

const LoginPage = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [selectedRole, setSelectedRole] = useState('parent');

  const handleSubmit = (e) => {
    e.preventDefault();
    // إنشاء بيانات المستخدم بناءً على الدور المحدد
    const userData = {
      role: selectedRole,
      username: username,
      name: selectedRole === 'parent' ? 'فاطمة أحمد محمد' : 
            selectedRole === 'teacher' ? 'د. محمد علي' :
            selectedRole === 'admin' ? 'مدير المدرسة' :
            selectedRole === 'student' ? 'أحمد محمد علي' : 'مستخدم'
    };
    onLogin(userData);
  };

  const handleRoleSelect = (role) => {
    setSelectedRole(role);
    // تعبئة تلقائية للبيانات حسب الدور
    switch (role) {
      case 'parent':
        setUsername('parent');
        setPassword('123456');
        break;
      case 'teacher':
        setUsername('teacher');
        setPassword('123456');
        break;
      case 'admin':
        setUsername('admin');
        setPassword('123456');
        break;
      case 'student':
        setUsername('student');
        setPassword('123456');
        break;
      default:
        setUsername('');
        setPassword('');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-700 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* School Logo and Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <img 
              src="/school-logo.jpeg" 
              alt="صُـنّاع الأوائل" 
              className="w-24 h-24 rounded-full border-4 border-white shadow-lg object-cover"
            />
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">صُـنّاع الأوائل</h1>
          <p className="text-blue-200">نظام إدارة الطلاب المتكامل</p>
          
          {/* School Information */}
          <div className="mt-4 text-blue-100 text-sm space-y-1">
            <div className="flex items-center justify-center gap-2">
              <MapPin className="w-4 h-4" />
              <span>النجف الأشرف - حي السلام</span>
            </div>
            <div className="flex items-center justify-center gap-2">
              <Phone className="w-4 h-4" />
              <span>الإدارة: 07802814111</span>
            </div>
          </div>
        </div>

        {/* Login Form */}
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">تسجيل الدخول</h2>
            <p className="text-gray-600">أدخل بياناتك للوصول إلى النظام</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                اسم المستخدم
              </label>
              <div className="relative">
                <User className="absolute right-3 top-3 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full pr-10 pl-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-right"
                  placeholder="أدخل اسم المستخدم"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                كلمة المرور
              </label>
              <div className="relative">
                <Lock className="absolute right-3 top-3 h-5 w-5 text-gray-400" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pr-10 pl-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-right"
                  placeholder="أدخل كلمة المرور"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition duration-200 font-medium"
            >
              تسجيل الدخول
            </button>
          </form>

          {/* Role Selection */}
          <div className="mt-6">
            <p className="text-center text-gray-600 mb-4">تجربة سريعة:</p>
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => handleRoleSelect('parent')}
                className={`p-3 rounded-lg border-2 transition-all ${
                  selectedRole === 'parent'
                    ? 'border-pink-500 bg-pink-50 text-pink-700'
                    : 'border-gray-200 hover:border-pink-300'
                }`}
              >
                <User className="w-5 h-5 mx-auto mb-1" />
                <span className="text-sm font-medium">ولي أمر</span>
              </button>
              
              <button
                onClick={() => handleRoleSelect('teacher')}
                className={`p-3 rounded-lg border-2 transition-all ${
                  selectedRole === 'teacher'
                    ? 'border-orange-500 bg-orange-50 text-orange-700'
                    : 'border-gray-200 hover:border-orange-300'
                }`}
              >
                <User className="w-5 h-5 mx-auto mb-1" />
                <span className="text-sm font-medium">معلم</span>
              </button>
              
              <button
                onClick={() => handleRoleSelect('admin')}
                className={`p-3 rounded-lg border-2 transition-all ${
                  selectedRole === 'admin'
                    ? 'border-green-500 bg-green-50 text-green-700'
                    : 'border-gray-200 hover:border-green-300'
                }`}
              >
                <User className="w-5 h-5 mx-auto mb-1" />
                <span className="text-sm font-medium">مدير</span>
              </button>
              
              <button
                onClick={() => handleRoleSelect('student')}
                className={`p-3 rounded-lg border-2 transition-all ${
                  selectedRole === 'student'
                    ? 'border-blue-500 bg-blue-50 text-blue-700'
                    : 'border-gray-200 hover:border-blue-300'
                }`}
              >
                <GraduationCap className="w-5 h-5 mx-auto mb-1" />
                <span className="text-sm font-medium">طالب</span>
              </button>
            </div>
          </div>

          {/* Contact Information */}
          <div className="mt-6 pt-6 border-t border-gray-200">
            <div className="text-center text-xs text-gray-500 space-y-1">
              <div>البنين: 07861890091 | البنات: 07840008233</div>
              <div>© 2024 صُـنّاع الأوائل. جميع الحقوق محفوظة</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;

