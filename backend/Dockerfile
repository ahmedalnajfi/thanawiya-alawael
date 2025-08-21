# استخدام Python 3.11 slim image
FROM python:3.11-slim

# تثبيت system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    libcairo2-dev \
    libgirepository1.0-dev \
    && rm -rf /var/lib/apt/lists/*

# إعداد مجلد العمل
WORKDIR /app

# نسخ ملفات requirements وتثبيت dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ ملفات المشروع
COPY . .

# إنشاء مجلد instance للـ database
RUN mkdir -p instance

# تعريف المتغيرات البيئية
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# فتح المنفذ
EXPOSE 5000

# تشغيل التطبيق
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
