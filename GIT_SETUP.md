# دليل تثبيت Git ونشر المشروع على GitHub
# Git Installation and GitHub Publishing Guide

## 📥 تثبيت Git | Installing Git

### Windows
1. انتقل إلى الموقع الرسمي لـ Git: https://git-scm.com/
2. اضغط على "Download for Windows"
3. قم بتشغيل الملف المحمل وتابع خطوات التثبيت
4. اختر الإعدادات الافتراضية (recommended)

### macOS
```bash
# Using Homebrew (recommended)
brew install git

# Or download from official website
# https://git-scm.com/download/mac
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install git
```

## ⚙️ إعداد Git الأولي | Initial Git Configuration

```bash
# Set your name (replace with your actual name)
git config --global user.name "Your Name"

# Set your email (use the same email as your GitHub account)
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

## 🐙 إعداد GitHub | GitHub Setup

### إنشاء حساب GitHub | Create GitHub Account
1. انتقل إلى https://github.com
2. اضغط على "Sign up" لإنشاء حساب جديد
3. اتبع خطوات التسجيل واختر خطة مجانية

### إنشاء مفتاح SSH (اختياري ولكن مُوصى به) | SSH Key Setup (Optional but Recommended)

#### Windows/macOS/Linux
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# When prompted, press Enter to save in default location
# Set a passphrase or press Enter for no passphrase

# Copy public key to clipboard
# Windows
clip < ~/.ssh/id_ed25519.pub

# macOS
pbcopy < ~/.ssh/id_ed25519.pub

# Linux
cat ~/.ssh/id_ed25519.pub
# Then copy the output manually
```

#### إضافة مفتاح SSH إلى GitHub | Add SSH Key to GitHub
1. انتقل إلى GitHub.com وسجل دخولك
2. اضغط على صورة الملف الشخصي → Settings
3. في الشريط الجانبي، اضغط على "SSH and GPG keys"
4. اضغط على "New SSH key"
5. أدخل عنوان للمفتاح واللصق المفتاح العام
6. اضغط على "Add SSH key"

## 📤 نشر المشروع على GitHub | Publishing to GitHub

### 1. إنشاء مستودع جديد على GitHub | Create New Repository on GitHub
1. سجل دخولك إلى GitHub
2. اضغط على "+" في الزاوية العلوية اليمنى → "New repository"
3. أدخل اسم المستودع: `thanawiya-school-system`
4. أضف وصف: `نظام إدارة مدرسة صُنّاع الأوائل - Thanawiya School Management System`
5. اختر "Public" أو "Private" حسب تفضيلك
6. **لا تضع علامة** على "Initialize with README" (سنقوم بذلك محلياً)
7. اضغط على "Create repository"

### 2. إعداد Git محلياً | Initialize Git Locally

```bash
# Navigate to your project directory
cd "C:\Users\MSI\Desktop\thanawiya-school-system"

# Initialize Git repository
git init

# Add all files to staging area
git add .

# Create first commit
git commit -m "Initial commit: Complete Thanawiya School Management System

✨ Features:
- Student Dashboard with assignments, exams, schedule, grades
- Teacher Dashboard with class management
- Parent Dashboard with student monitoring  
- Admin Dashboard with system management
- Multi-role authentication system
- Comprehensive database models
- Modern React frontend with Tailwind CSS
- Flask backend with SQLAlchemy
- Arabic language support (RTL)

🏫 Built for Makers of Excellence Secondary School (مدرسة صُنّاع الأوائل الثانوية)"

# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/thanawiya-school-system.git

# Or if using SSH (recommended if you set up SSH keys):
# git remote add origin git@github.com:YOUR_USERNAME/thanawiya-school-system.git

# Push to GitHub
git push -u origin main
```

### 3. التحقق من النشر | Verify Publishing
1. انتقل إلى مستودع GitHub الخاص بك
2. تأكد من ظهور جميع ملفات المشروع
3. تحقق من ظهور ملف README.md بشكل صحيح

## 🔄 العمليات الأساسية لـ Git | Basic Git Operations

### إضافة تغييرات جديدة | Adding New Changes
```bash
# Check status of files
git status

# Add specific files
git add filename.py

# Add all changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push
```

### إنشاء فرع جديد للتطوير | Creating Development Branch
```bash
# Create and switch to new branch
git checkout -b development

# Push new branch to GitHub
git push -u origin development

# Switch between branches
git checkout main
git checkout development
```

### دمج التغييرات | Merging Changes
```bash
# Switch to main branch
git checkout main

# Merge development branch
git merge development

# Push merged changes
git push
```

## 🛡️ إعدادات الأمان | Security Settings

### إنشاء ملف .env للحساسيات | Create .env for Sensitive Data
```bash
# The .env file is already in .gitignore
# Make sure to create .env from .env.example in backend folder
cd backend
copy .env.example .env

# Edit .env with your actual configuration
# NEVER commit .env to Git!
```

### التحقق من .gitignore | Verify .gitignore
```bash
# Make sure .gitignore includes:
# .env
# instance/
# __pycache__/
# node_modules/
# venv/
```

## 📋 قائمة التحقق النهائية | Final Checklist

- [ ] تم تثبيت Git بنجاح
- [ ] تم إعداد اسم المستخدم والبريد الإلكتروني لـ Git
- [ ] تم إنشاء حساب GitHub
- [ ] تم إنشاء مفتاح SSH وإضافته لـ GitHub (اختياري)
- [ ] تم إنشاء مستودع جديد على GitHub
- [ ] تم رفع جميع ملفات المشروع بنجاح
- [ ] تم التحقق من عدم رفع الملفات الحساسة (.env, venv, node_modules)
- [ ] تم إضافة وصف مناسب للمستودع

## 🎯 الخطوات التالية | Next Steps

1. **إنشاء فرع التطوير:**
   ```bash
   git checkout -b development
   git push -u origin development
   ```

2. **إعداد GitHub Pages (اختياري):**
   - انتقل إلى إعدادات المستودع
   - اختر Pages من الشريط الجانبي
   - اختر المصدر (عادة main branch)

3. **إضافة متعاونين:**
   - إعدادات المستودع → Manage access
   - اضغط على "Invite a collaborator"

4. **إنشاء Issues و Projects:**
   - استخدم Issues لتتبع المهام والأخطاء
   - أنشئ Project board لإدارة سير العمل

## 🔗 روابط مفيدة | Useful Links

- **Git Documentation:** https://git-scm.com/docs
- **GitHub Guides:** https://guides.github.com/
- **Git Cheat Sheet:** https://education.github.com/git-cheat-sheet-education.pdf
- **Markdown Guide:** https://www.markdownguide.org/

## ❓ استكشاف الأخطاء الشائعة | Troubleshooting

### خطأ: "repository not found"
```bash
# Check remote URL
git remote -v

# Update remote URL if incorrect
git remote set-url origin https://github.com/YOUR_USERNAME/thanawiya-school-system.git
```

### خطأ: "Permission denied"
```bash
# If using HTTPS, check your GitHub credentials
# If using SSH, check your SSH key setup
ssh -T git@github.com
```

### خطأ: "failed to push"
```bash
# Pull latest changes first
git pull origin main

# Then push again
git push origin main
```

---

**🎉 تهانينا! تم نشر مشروع نظام إدارة مدرسة صُنّاع الأوائل بنجاح على GitHub**

**Congratulations! The Thanawiya School Management System has been successfully published to GitHub**
