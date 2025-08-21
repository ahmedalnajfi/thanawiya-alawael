@echo off
chcp 65001 >nul
echo ========================================
echo   نشر مشروع ثانوية الأوائل مجاناً
echo   Deploy Thanawiya Project for FREE
echo ========================================
echo.

echo 🚀 خطة النشر المجاني:
echo.
echo 📋 المنصات المختارة:
echo   🎨 Frontend: Vercel (مجاني)
echo   ⚡ Backend: Railway (مجاني)
echo   💾 Database: PostgreSQL (مجاني)
echo.

echo [1] تحضير ملفات النشر...
echo ✅ Railway.json - إعدادات البناء
echo ✅ Procfile - إعدادات التشغيل
echo ✅ Dockerfile - حاوية Backend
echo ✅ vercel.json - إعدادات Frontend
echo ✅ .env.production - متغيرات البيئة
echo.

echo [2] الروابط المطلوبة:
echo.
echo 🔗 للـ Backend (Railway):
echo    👉 https://railway.app
echo    📝 سجل دخول بحساب GitHub
echo    ⚙️  Deploy from GitHub repo: thanawiya-alawael
echo    💿 إضافة PostgreSQL service
echo.
echo 🔗 للـ Frontend (Vercel):
echo    👉 https://vercel.com  
echo    📝 سجل دخول بحساب GitHub
echo    ⚙️  New Project: thanawiya-alawael
echo    📁 Root Directory: frontend/
echo.

echo [3] متغيرات البيئة المطلوبة:
echo.
echo 📋 Railway Environment Variables:
echo    FLASK_APP=app.py
echo    FLASK_ENV=production
echo    SECRET_KEY=your-secret-key-123456
echo    JWT_SECRET_KEY=your-jwt-secret-123456
echo    DATABASE_URL=${{Postgres.DATABASE_URL}}
echo    PYTHONPATH=/app/backend
echo.
echo 📋 Vercel Environment Variables:
echo    VITE_API_URL=https://your-railway-app.railway.app/api
echo    VITE_APP_NAME=صُنّاع الأوائل
echo    VITE_SCHOOL_NAME=مدرسة صُنّاع الأوائل الثانوية
echo.

echo [4] إعدادات البناء:
echo.
echo 🏗️ Railway Build Settings:
echo    Build Command: cd backend && pip install -r requirements.txt
echo    Start Command: cd backend && gunicorn --bind 0.0.0.0:$PORT app:app
echo.
echo 🏗️ Vercel Build Settings:
echo    Framework Preset: Vite
echo    Build Command: cd frontend && npm install && npm run build
echo    Output Directory: frontend/dist
echo    Install Command: cd frontend && npm install
echo.

echo [5] الخطوات التفصيلية:
echo.
echo 📖 راجع الدليل الشامل في:
echo    📄 FREE_DEPLOYMENT_GUIDE.md
echo.

echo ========================================
echo 🌐 الروابط المتوقعة بعد النشر:
echo ========================================
echo   Frontend: https://thanawiya-alawael.vercel.app
echo   Backend:  https://thanawiya-production.up.railway.app
echo   GitHub:   https://github.com/ahmedalnajfi/thanawiya-alawael
echo ========================================
echo.

echo 🎯 هل تريد فتح المواقع للبدء بالنشر؟
echo [1] نعم - افتح Railway و Vercel
echo [2] لا - إظهار الدليل فقط
echo.
set /p choice="اختر (1 أو 2): "

if "%choice%"=="1" (
    echo.
    echo 🌐 فتح المواقع...
    start https://railway.app
    timeout /t 2 >nul
    start https://vercel.com
    timeout /t 2 >nul
    start https://github.com/ahmedalnajfi/thanawiya-alawael
    echo ✅ تم فتح المواقع في المتصفح
) else (
    echo.
    echo 📖 راجع الدليل في: FREE_DEPLOYMENT_GUIDE.md
)

echo.
echo 🎉 بالتوفيق في النشر!
echo 💪 مشروعك سيكون متاح مجاناً على الإنترنت قريباً!
echo.
pause
