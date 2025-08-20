import React, { useState } from 'react';

const ExcelUpload = ({ onUpload, type = 'students' }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [preview, setPreview] = useState([]);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && (selectedFile.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || 
                         selectedFile.type === 'application/vnd.ms-excel')) {
      setFile(selectedFile);
      // هنا يمكن إضافة معاينة للملف
    } else {
      alert('يرجى اختيار ملف Excel صحيح (.xlsx أو .xls)');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert('يرجى اختيار ملف Excel أولاً');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);

    try {
      const response = await fetch('/api/upload-excel', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        alert(`تم رفع ${result.count} ${type === 'students' ? 'طالب' : 'شعبة'} بنجاح!`);
        if (onUpload) onUpload(result);
        setFile(null);
        setPreview([]);
      } else {
        const error = await response.json();
        alert(`خطأ في الرفع: ${error.message}`);
      }
    } catch (error) {
      alert(`خطأ في الاتصال: ${error.message}`);
    } finally {
      setUploading(false);
    }
  };

  const downloadTemplate = () => {
    const templateUrl = type === 'students' 
      ? '/api/download-template/students' 
      : '/api/download-template/classes';
    
    const link = document.createElement('a');
    link.href = templateUrl;
    link.download = `template_${type}.xlsx`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const getRequiredFields = () => {
    if (type === 'students') {
      return [
        'الاسم الكامل',
        'رقم الهوية',
        'تاريخ الميلاد',
        'الصف',
        'الشعبة (فرنسي/غير فرنسي)',
        'اسم ولي الأمر',
        'رقم هاتف ولي الأمر',
        'العنوان',
        'الجنس (ذكر/أنثى)',
        'البناية (بنين/بنات)'
      ];
    } else {
      return [
        'اسم الشعبة',
        'الصف',
        'النوع (فرنسي/غير فرنسي)',
        'المرحلة الدراسية',
        'عدد الطلاب المتوقع',
        'البناية (بنين/بنات)',
        'المعلم المسؤول'
      ];
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-bold mb-4 text-right">
        رفع {type === 'students' ? 'بيانات الطلاب' : 'بيانات الشعب'} من Excel
      </h3>

      {/* تحميل القالب */}
      <div className="mb-6 p-4 bg-blue-50 rounded-lg">
        <h4 className="font-semibold mb-2 text-right">📋 تحميل القالب</h4>
        <p className="text-sm text-gray-600 mb-3 text-right">
          قم بتحميل القالب أولاً وملء البيانات المطلوبة
        </p>
        <button
          onClick={downloadTemplate}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 text-sm"
        >
          📥 تحميل قالب Excel
        </button>
      </div>

      {/* الحقول المطلوبة */}
      <div className="mb-6 p-4 bg-yellow-50 rounded-lg">
        <h4 className="font-semibold mb-2 text-right">📝 الحقول المطلوبة</h4>
        <div className="grid grid-cols-2 gap-2 text-sm">
          {getRequiredFields().map((field, index) => (
            <div key={index} className="text-right text-gray-700">
              • {field}
            </div>
          ))}
        </div>
      </div>

      {/* رفع الملف */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2 text-right">
          اختر ملف Excel
        </label>
        <input
          type="file"
          accept=".xlsx,.xls"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          disabled={uploading}
        />
      </div>

      {file && (
        <div className="mb-4 p-3 bg-green-50 rounded-lg">
          <p className="text-sm text-green-700 text-right">
            ✅ تم اختيار الملف: {file.name}
          </p>
          <p className="text-xs text-gray-500 text-right">
            الحجم: {(file.size / 1024 / 1024).toFixed(2)} MB
          </p>
        </div>
      )}

      {/* أزرار التحكم */}
      <div className="flex gap-3 justify-end">
        <button
          onClick={() => {
            setFile(null);
            setPreview([]);
          }}
          className="px-4 py-2 text-gray-600 border border-gray-300 rounded hover:bg-gray-50"
          disabled={uploading}
        >
          إلغاء
        </button>
        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {uploading ? (
            <span className="flex items-center gap-2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              جاري الرفع...
            </span>
          ) : (
            '📤 رفع البيانات'
          )}
        </button>
      </div>

      {/* تعليمات إضافية */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-semibold mb-2 text-right">💡 تعليمات مهمة</h4>
        <ul className="text-sm text-gray-600 space-y-1 text-right">
          <li>• تأكد من ملء جميع الحقول المطلوبة</li>
          <li>• استخدم التنسيق الصحيح للتواريخ (DD/MM/YYYY)</li>
          <li>• تأكد من صحة أرقام الهواتف</li>
          <li>• لا تترك خلايا فارغة في الحقول المطلوبة</li>
          <li>• احفظ الملف بصيغة .xlsx للحصول على أفضل النتائج</li>
        </ul>
      </div>
    </div>
  );
};

export default ExcelUpload;

