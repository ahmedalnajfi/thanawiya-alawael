@echo off
chcp 65001 > nul
echo ========================================
echo   نشر مشروع ثانوية الأوائل على GitHub
echo   Publishing Thanawiya Project to GitHub
echo ========================================
echo.

echo [1/6] التحقق من إعداد Git...
git --version
if errorlevel 1 (
    echo ❌ Git غير مثبت! يرجى تثبيت Git من: https://git-scm.com/
    echo ❌ Git not installed! Please install Git from: https://git-scm.com/
    pause
    exit /b 1
)

echo [2/6] إعداد Git (إذا لم يكن معداً من قبل)...
echo يرجى إدخال اسمك:
set /p USER_NAME="Enter your name: "
echo يرجى إدخال بريدك الإلكتروني:
set /p USER_EMAIL="Enter your email: "

git config --global user.name "%USER_NAME%"
git config --global user.email "%USER_EMAIL%"

echo [3/6] تهيئة مستودع Git...
git init

echo [4/6] إضافة جميع الملفات...
git add .

echo [5/6] إنشاء أول commit...
git commit -m "Initial commit: مشروع نظام إدارة مدرسة صُنّاع الأوائل

✨ الميزات المتاحة / Available Features:
- لوحة تحكم الطالب مع الواجبات والامتحانات والجدول والدرجات
- لوحة تحكم المعلم لإدارة الصفوف
- لوحة تحكم ولي الأمر لمتابعة الأبناء  
- لوحة تحكم المدير لإدارة النظام
- نظام مصادقة متعدد الأدوار
- نماذج قاعدة بيانات شاملة
- واجهة React حديثة مع Tailwind CSS
- خادم Flask مع SQLAlchemy
- دعم اللغة العربية (RTL)

🏫 مصمم خصيصاً لمدرسة صُنّاع الأوائل الثانوية
🏫 Built for Makers of Excellence Secondary School"

echo [6/6] الآن تحتاج لإنشاء مستودع على GitHub:
echo.
echo 📋 خطوات إنشاء المستودع على GitHub:
echo 1. انتقل إلى https://github.com
echo 2. اضغط على "+" ثم "New repository"
echo 3. اسم المستودع: thanawiya-alawael
echo 4. الوصف: نظام إدارة مدرسة صُنّاع الأوائل - Thanawiya School Management System
echo 5. اختر Public أو Private
echo 6. لا تضع علامة على "Initialize with README"
echo 7. اضغط "Create repository"
echo.
echo بعد إنشاء المستودع، أدخل اسم المستخدم GitHub الخاص بك:
set /p GITHUB_USERNAME="GitHub Username: "

echo إضافة الرابط البعيد...
git remote add origin https://github.com/%GITHUB_USERNAME%/thanawiya-alawael.git

echo رفع المشروع إلى GitHub...
git branch -M main
git push -u origin main

echo.
echo ✅ تم! المشروع متاح الآن على:
echo 🔗 https://github.com/%GITHUB_USERNAME%/thanawiya-alawael
echo.
pause
