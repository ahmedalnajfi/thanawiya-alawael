# 🚀 دليل النشر والنهر - Deployment Guide

## نظام إدارة مدرسة صُنّاع الأوائل
### Makers of Excellence School Management System

---

## 📋 خطوات النشر السريعة / Quick Deployment Steps

### المرحلة 1: تثبيت Git
**إذا لم يكن Git مثبتاً على جهازك:**

1. **التحميل:**
   - انتقل إلى: https://git-scm.com/download/win
   - حمل الإصدار المناسب لنظامك (64-bit أو 32-bit)

2. **التثبيت:**
   - افتح الملف المحمل
   - اتبع خطوات التثبيت (يمكنك الضغط على Next لجميع الخيارات الافتراضية)

### المرحلة 2: النشر الآلي (الطريقة السهلة)

**ببساطة:**
1. اضغط مرتين على الملف `publish-to-github.bat` في مجلد المشروع
2. اتبع التعليمات التي تظهر على الشاشة

**الملف الآلي سيقوم بـ:**
- ✅ التحقق من تثبيت Git
- ✅ إعداد Git باسمك وبريدك الإلكتروني
- ✅ تهيئة مستودع Git محلي
- ✅ إضافة جميع ملفات المشروع
- ✅ إنشاء أول commit
- ✅ ربط المشروع بـ GitHub
- ✅ رفع المشروع

---

## 🛠️ النشر اليدوي / Manual Deployment

### 1. فتح موجه الأوامر
```bash
# انتقل إلى مجلد المشروع
cd C:\Users\MSI\Desktop\thanawiya-school-system
```

### 2. إعداد Git (لأول مرة فقط)
```bash
git config --global user.name "اسمك"
git config --global user.email "your.email@example.com"
```

### 3. تهيئة المستودع
```bash
git init
git add .
git commit -m "Initial commit: مشروع نظام إدارة مدرسة صُنّاع الأوائل"
```

### 4. إنشاء مستودع GitHub
1. انتقل إلى: https://github.com
2. اضغط على "+" ثم "New repository"
3. **اسم المستودع:** `thanawiya-alawael`
4. **الوصف:** `نظام إدارة مدرسة صُنّاع الأوائل - Thanawiya School Management System`
5. اختر **Public** أو **Private**
6. **لا تضع علامة** على "Initialize with README"
7. اضغط "Create repository"

### 5. ربط ورفع المشروع
```bash
# استبدل USERNAME باسم المستخدم الخاص بك
git remote add origin https://github.com/USERNAME/thanawiya-alawael.git
git branch -M main
git push -u origin main
```

---

## 🌐 إعداد الاستضافة / Hosting Setup

### خيارات الاستضافة المجانية:

#### 1. Heroku (للـ Backend)
```bash
# تثبيت Heroku CLI أولاً
heroku create thanawiya-backend
heroku config:set FLASK_ENV=production
git push heroku main
```

#### 2. Vercel (للـ Frontend)
```bash
# تثبيت Vercel CLI
npm i -g vercel
cd frontend
vercel --prod
```

#### 3. Netlify (للـ Frontend)
1. انتقل إلى: https://netlify.com
2. اربط حساب GitHub
3. اختر المستودع `thanawiya-alawael`
4. Build Command: `cd frontend && npm run build`
5. Publish Directory: `frontend/dist`

---

## ⚙️ متغيرات البيئة / Environment Variables

### Backend (.env)
```env
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///thanawiya.db
JWT_SECRET_KEY=your-jwt-secret-here
```

### Frontend (.env)
```env
VITE_API_URL=https://your-backend-url.herokuapp.com/api
VITE_APP_NAME=صُنّاع الأوائل
```

---

## 🔧 إعداد قاعدة البيانات / Database Setup

### الإنتاج / Production
```bash
# إنشاء الجداول
python -c "from app import db; db.create_all()"

# إضافة البيانات الأولية
python seed_data.py
```

---

## 📊 البيانات التجريبية / Demo Accounts

### الحسابات الافتراضية:
- **مدير:** admin@thanawiya.edu / admin123
- **معلم:** teacher@thanawiya.edu / teacher123  
- **طالب:** student@thanawiya.edu / student123
- **ولي أمر:** parent@thanawiya.edu / parent123

---

## 🚨 استكشاف الأخطاء / Troubleshooting

### مشاكل شائعة:

#### Git غير موجود:
```
'git' is not recognized as an internal or external command
```
**الحل:** تثبيت Git من الرابط أعلاه وإعادة تشغيل موجه الأوامر

#### مساحة القرص ممتلئة:
```
No space left on device
```
**الحل:** 
- حذف ملفات غير ضرورية
- نقل المشروع لقرص آخر
- استخدام التنظيف: `git clean -fd`

#### مشاكل الرفع:
```
Permission denied (publickey)
```
**الحل:** استخدام HTTPS بدلاً من SSH:
```bash
git remote set-url origin https://github.com/USERNAME/thanawiya-alawael.git
```

---

## 📞 الدعم الفني / Support

### إذا واجهت أي مشاكل:
1. **تحقق من سجل الأخطاء** في موجه الأوامر
2. **تأكد من الاتصال بالإنترنت**
3. **تحقق من صحة أسماء المستخدم وكلمات المرور**
4. **راجع دليل GitHub الرسمي:** https://docs.github.com

---

## ✅ قائمة المراجعة النهائية / Final Checklist

- [ ] Git مثبت ومعداً
- [ ] مستودع GitHub منشئ
- [ ] ملفات المشروع مرفوعة
- [ ] متغيرات البيئة معدة
- [ ] قاعدة البيانات منشئة
- [ ] البيانات التجريبية مضافة
- [ ] الاستضافة معدة ومفعلة

---

## 🎉 تهانينا!

**مشروعك الآن منشور بنجاح على GitHub! 🎉**

**الروابط المتوقعة:**
- 📂 **GitHub Repository:** https://github.com/YOUR_USERNAME/thanawiya-alawael
- 🌐 **Live Frontend:** https://your-app.vercel.app
- ⚡ **Backend API:** https://your-backend.herokuapp.com

---

> **تم إنجاز المشروع بواسطة:** نظام الذكي الاصطناعي المتخصص في التطوير  
> **تاريخ الإنشاء:** ديسمبر 2024  
> **المطور:** فريق صُنّاع الأوائل التقني
