# دليل إعداد وتشغيل نظام إدارة مدرسة صُنّاع الأوائل
# Setup Guide for Thanawiya School Management System

## 📋 المتطلبات الأساسية | Prerequisites

### النظام | System Requirements
- Windows 10/11, macOS 10.15+, or Linux Ubuntu 18.04+
- Python 3.8 or higher
- Node.js 18.0 or higher
- npm or pnpm package manager
- Git (for version control)

### التحقق من المتطلبات | Verify Requirements
```bash
# Check Python version
python --version
# or
python3 --version

# Check Node.js version
node --version

# Check npm version
npm --version

# Check Git version
git --version
```

## 🚀 خطوات التثبيت | Installation Steps

### 1. تحميل المشروع | Clone the Project

```bash
# Navigate to your desired directory
cd Desktop

# If using Git (when repository is published)
git clone https://github.com/your-username/thanawiya-school-system.git
cd thanawiya-school-system

# Or extract the project folder if downloaded as ZIP
```

### 2. إعداد الخادم الخلفي | Backend Setup

#### أ. الانتقال إلى مجلد الخادم الخلفي | Navigate to Backend
```bash
cd backend
```

#### ب. إنشاء بيئة افتراضية | Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### ج. تثبيت المتطلبات | Install Requirements
```bash
pip install -r requirements.txt
```

#### د. إعداد متغيرات البيئة | Setup Environment Variables
```bash
# Copy the example environment file
copy .env.example .env          # Windows
# or
cp .env.example .env           # macOS/Linux

# Edit .env file with your preferred text editor
notepad .env                   # Windows
# or
nano .env                      # macOS/Linux
```

#### هـ. إعداد قاعدة البيانات | Setup Database
```bash
# Initialize the database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Or if using app.py directly
python app.py
```

### 3. إعداد الواجهة الأمامية | Frontend Setup

#### أ. الانتقال إلى مجلد الواجهة الأمامية | Navigate to Frontend
```bash
# From project root
cd frontend
```

#### ب. تثبيت المتطلبات | Install Dependencies
```bash
# Using npm
npm install

# Or using pnpm (recommended)
pnpm install
```

#### ج. إعداد متغيرات البيئة (اختياري) | Setup Environment Variables (Optional)
```bash
# Copy environment example if it exists
copy .env.local.example .env.local    # Windows
# or  
cp .env.local.example .env.local      # macOS/Linux
```

## 🎯 تشغيل التطبيق | Running the Application

### تشغيل الخادم الخلفي | Start Backend Server
```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if not already active)
# Windows
venv\Scripts\activate
# macOS/Linux  
source venv/bin/activate

# Run the Flask application
python app.py

# The backend will be available at: http://localhost:5000
```

### تشغيل الواجهة الأمامية | Start Frontend Development Server
```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Start development server
npm run dev
# or
pnpm dev

# The frontend will be available at: http://localhost:5173
```

## 🔐 بيانات الدخول الافتراضية | Default Login Credentials

للوصول إلى النظام، يمكنك استخدام البيانات التالية:

### مدير المدرسة | School Administrator
- **اسم المستخدم | Username:** `admin`
- **كلمة المرور | Password:** `123456`

### المعلم | Teacher
- **اسم المستخدم | Username:** `teacher` 
- **كلمة المرور | Password:** `123456`

### ولي الأمر | Parent
- **اسم المستخدم | Username:** `parent`
- **كلمة المرور | Password:** `123456`

### الطالب | Student
- **اسم المستخدم | Username:** `student`
- **كلمة المرور | Password:** `123456`

## 🛠️ إعدادات إضافية | Additional Configuration

### إعداد قاعدة بيانات الإنتاج | Production Database Setup

#### PostgreSQL
```bash
# Install PostgreSQL first
# Then update .env file:
DATABASE_URL=postgresql://username:password@localhost:5432/thanawiya_db
```

#### MySQL
```bash  
# Install MySQL first
# Then update .env file:
DATABASE_URL=mysql://username:password@localhost:3306/thanawiya_db
```

### إعداد البريد الإلكتروني | Email Configuration
```bash
# Update .env file with your email settings:
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_USE_TLS=True
```

### إعداد Redis للكاش والجلسات | Redis Setup for Caching
```bash
# Install Redis first
# Then update .env file:
REDIS_URL=redis://localhost:6379/0
```

## 📱 الميزات المتاحة | Available Features

### للطلاب | For Students
- عرض النظرة العامة على الأداء الأكاديمي
- تتبع الواجبات والمهام
- جدول الامتحانات القادمة  
- جدول الحصص اليومي
- عرض الدرجات والتقييمات
- إعدادات الحساب الشخصي

### للمعلمين | For Teachers
- إدارة الصفوف والطلاب
- إنشاء وإدارة الواجبات
- تسجيل الحضور والغياب
- إدخال وإدارة الدرجات
- التواصل مع أولياء الأمور

### لأولياء الأمور | For Parents
- متابعة الأداء الأكاديمي للأبناء
- عرض التقارير والدرجات
- متابعة الحضور والغياب
- التواصل مع المعلمين

### للإدارة | For Administration
- إدارة شاملة للنظام
- إدارة المستخدمين والأدوار
- التقارير والإحصائيات
- إعدادات النظام العامة

## 🔧 استكشاف الأخطاء | Troubleshooting

### مشاكل شائعة | Common Issues

#### الخادم الخلفي لا يعمل | Backend Not Starting
```bash
# Check if virtual environment is activated
# Verify all dependencies are installed
pip install -r requirements.txt

# Check database connection
# Verify .env file configuration
```

#### الواجهة الأمامية لا تعمل | Frontend Not Starting  
```bash
# Clear node modules and reinstall
rm -rf node_modules
npm install

# Check Node.js version compatibility
node --version
```

#### مشاكل قاعدة البيانات | Database Issues
```bash
# Reset database
rm instance/*.db
python app.py

# Or run migrations
flask db upgrade
```

#### مشاكل CORS | CORS Issues
```bash
# Ensure backend CORS is configured properly
# Check CORS_ALLOWED_ORIGINS in .env file
```

## 📞 الدعم والمساعدة | Support & Help

### الحصول على المساعدة | Getting Help
- راجع ملف README.md للحصول على معلومات تفصيلية
- تحقق من ملفات السجل في مجلد `logs/`
- تأكد من تشغيل جميع الخدمات المطلوبة

### معلومات الاتصال | Contact Information
- **الإدارة | Administration:** 07802814111
- **قسم البنين | Boys Section:** 07861890091
- **قسم البنات | Girls Section:** 07840008233

## 🚀 النشر في الإنتاج | Production Deployment

### إعداد الإنتاج | Production Setup
```bash
# Update .env for production
FLASK_ENV=production
DEBUG=False
SESSION_COOKIE_SECURE=True

# Use production database
DATABASE_URL=postgresql://user:pass@host:port/db

# Configure web server (nginx + gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### نصائح الأمان | Security Tips
- غيّر جميع كلمات المرور الافتراضية
- استخدم HTTPS في الإنتاج
- قم بعمل نسخ احتياطية منتظمة
- راقب السجلات بانتظام

---

**© 2024 مدرسة صُنّاع الأوائل الثانوية**  
**جميع الحقوق محفوظة**
