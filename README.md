# نظام إدارة مدرسة صُنّاع الأوائل الثانوية
# Thanawiya School Management System - "Makers of Excellence"

A comprehensive school management system for "Makers of Excellence" secondary school in Najaf Al-Ashraf, Iraq.

## 📖 Overview / نظرة عامة

This is a full-stack school management system built with React frontend and Flask backend, designed specifically for secondary schools in Iraq.

**English:** This system provides comprehensive student management, grade tracking, attendance monitoring, and parent-teacher communication tools.

**العربية:** هذا النظام يوفر إدارة شاملة للطلاب، وتتبع الدرجات، ومراقبة الحضور، وأدوات التواصل بين الأهل والمعلمين.

## 🏗️ Architecture / البنية المعمارية

- **Frontend**: React 19 with Vite, TailwindCSS, and modern UI components
- **Backend**: Flask with SQLAlchemy, RESTful API
- **Database**: SQLite for development, PostgreSQL-ready for production
- **Authentication**: JWT-based authentication system
- **Real-time**: WebSocket support for notifications

## 🌟 Features / المميزات

### For Students / للطلاب
- View grades and academic progress / عرض الدرجات والتقدم الأكاديمي
- Access assignment and homework / الوصول للواجبات والمهام
- Check attendance records / فحص سجلات الحضور
- Communication with teachers / التواصل مع المعلمين

### For Parents / للأهل
- Monitor child's academic performance / مراقبة الأداء الأكاديمي للطفل
- Receive notifications about grades and attendance / استقبال إشعارات الدرجات والحضور
- Direct communication with teachers / التواصل المباشر مع المعلمين
- Access to school announcements / الوصول لإعلانات المدرسة

### For Teachers / للمعلمين
- Grade management and assignment creation / إدارة الدرجات وإنشاء الواجبات
- Attendance tracking / تتبع الحضور
- Student progress reports / تقارير تقدم الطلاب
- Parent communication tools / أدوات التواصل مع الأهل

### For Administrators / للإداريين
- Complete system management / إدارة شاملة للنظام
- User account management / إدارة حسابات المستخدمين
- Academic year and semester setup / إعداد العام الدراسي والفصول
- System analytics and reporting / تحليلات وتقارير النظام

## 📁 Project Structure / هيكل المشروع

```
thanawiya-school-system/
├── backend/                 # Flask backend application
│   ├── src/                # Source code
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── static/         # Static files
│   ├── migrations/         # Database migrations
│   ├── instance/           # Database files
│   ├── app.py              # Main application file
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend application
│   ├── src/                # Source code
│   │   ├── components/     # React components
│   │   ├── assets/         # Static assets
│   │   └── App.jsx         # Main app component
│   ├── public/             # Public assets
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
└── README.md               # This file
```

## 🚀 Getting Started / البدء

### Prerequisites / المتطلبات المسبقة
- Python 3.8+ for backend
- Node.js 18+ for frontend
- Git for version control

### Backend Setup / إعداد الخادم الخلفي

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py
```

### Frontend Setup / إعداد الواجهة الأمامية

```bash
cd frontend
npm install  # or pnpm install
npm run dev  # or pnpm dev
```

## 🖥️ Default Access / الوصول الافتراضي

The system includes demo accounts for testing:

### Parent Account / حساب ولي الأمر
- Username: `parent`
- Password: `123456`

### Teacher Account / حساب المعلم
- Username: `teacher`  
- Password: `123456`

### Admin Account / حساب المدير
- Username: `admin`
- Password: `123456`

## 🏫 School Information / معلومات المدرسة

**School Name:** مدرسة صُنّاع الأوائل الثانوية  
**Location:** النجف الأشرف - حي السلام  
**Contact:** 
- Administration: 07802814111
- Boys Section: 07861890091  
- Girls Section: 07840008233

## 🛠️ Technologies Used / التقنيات المستخدمة

### Frontend Technologies
- React 19.1.0 with hooks and modern patterns
- Vite for fast development and building
- TailwindCSS for styling
- Radix UI components for accessibility
- React Router for navigation
- React Hook Form for form management
- Zustand for state management
- React Query for server state
- Framer Motion for animations

### Backend Technologies
- Flask 3.1.1 web framework
- SQLAlchemy 2.0+ for ORM
- Alembic for database migrations
- Flask-JWT-Extended for authentication
- Flask-CORS for cross-origin requests
- Flask-SocketIO for real-time features
- Marshmallow for data validation
- OpenAI integration for AI features

## 📊 Database Schema / مخطط قاعدة البيانات

The system includes comprehensive models for:
- User management (students, parents, teachers, admins)
- Academic structure (subjects, classes, academic years)
- Grade and attendance tracking
- Communication and notifications
- AI-powered features

## 🔒 Security Features / مميزات الأمان

- JWT-based authentication
- Password hashing with bcrypt
- Input validation and sanitization
- CORS protection
- Rate limiting
- SQL injection prevention

## 🌐 API Documentation / توثيق API

The backend provides RESTful APIs with the following main endpoints:
- `/api/auth/*` - Authentication endpoints
- `/api/students/*` - Student management
- `/api/parents/*` - Parent operations
- `/api/teachers/*` - Teacher functionality
- `/api/admin/*` - Administrative operations

## 📱 Responsive Design / التصميم المتجاوب

The frontend is fully responsive and works on:
- Desktop computers / أجهزة الكمبيوتر
- Tablets / الأجهزة اللوحية  
- Mobile phones / الهواتف المحمولة

## 🎨 UI/UX Features / مميزات واجهة المستخدم

- Modern and clean interface
- Right-to-left (RTL) support for Arabic
- Dark and light mode support
- Accessibility compliance
- Intuitive navigation
- Interactive animations and transitions

## 🔄 Development Status / حالة التطوير

✅ **Completed Features:**
- User authentication system
- Dashboard layouts for all user types
- Basic CRUD operations
- Database schema and models
- API endpoints structure
- Frontend component architecture

🚧 **In Progress:**
- Advanced reporting features
- Real-time notifications
- Mobile app development
- AI-powered analytics

## 🤝 Contributing / المساهمة

This project is designed for "Makers of Excellence" secondary school. For contributions or customizations, please contact the development team.

## 📄 License / الترخيص

This project is developed specifically for مدرسة صُنّاع الأوائل الثانوية (Makers of Excellence Secondary School).

## 📞 Support / الدعم الفني

For technical support or questions:
- Email: [Contact school administration]
- Phone: 07802814111

---

**© 2024 مدرسة صُنّاع الأوائل الثانوية - Makers of Excellence Secondary School**  
**جميع الحقوق محفوظة - All Rights Reserved**
