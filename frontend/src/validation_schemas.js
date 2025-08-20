import { z } from 'zod';

// Login validation schema
export const loginSchema = z.object({
  username: z.string()
    .min(3, 'اسم المستخدم يجب أن يكون على الأقل 3 أحرف')
    .max(20, 'اسم المستخدم يجب أن لا يتجاوز 20 حرف')
    .regex(/^[a-zA-Z0-9_]+$/, 'اسم المستخدم يجب أن يحتوي على أحرف وأرقام فقط'),

  password: z.string()
    .min(6, 'كلمة المرور يجب أن تكون على الأقل 6 أحرف')
    .max(50, 'كلمة المرور طويلة جداً'),

  role: z.enum(['parent', 'teacher', 'admin'], {
    errorMap: () => ({ message: 'نوع المستخدم غير صحيح' })
  })
});

// Student data validation
export const studentSchema = z.object({
  name: z.string()
    .min(2, 'اسم الطالب يجب أن يكون على الأقل حرفين')
    .max(100, 'اسم الطالب طويل جداً')
    .regex(/^[؀-ۿ\s]+$/, 'اسم الطالب يجب أن يكون باللغة العربية'),

  studentId: z.string()
    .regex(/^[A-Z]\d{3}$/, 'رقم الطالب يجب أن يكون بصيغة A001'),

  className: z.string()
    .min(1, 'الصف مطلوب')
    .max(10, 'اسم الصف طويل جداً'),

  section: z.string()
    .min(1, 'القسم مطلوب')
    .max(20, 'اسم القسم طويل جداً'),

  phoneNumber: z.string()
    .regex(/^05\d{8}$/, 'رقم الهاتف يجب أن يبدأ بـ 05 ويحتوي على 10 أرقام'),

  parentName: z.string()
    .min(2, 'اسم ولي الأمر يجب أن يكون على الأقل حرفين')
    .max(100, 'اسم ولي الأمر طويل جداً')
});

// Grade validation
export const gradeSchema = z.object({
  subject: z.string().min(1, 'المادة مطلوبة'),
  grade: z.number()
    .min(0, 'الدرجة لا يمكن أن تكون أقل من 0')
    .max(100, 'الدرجة لا يمكن أن تتجاوز 100'),
  examType: z.enum(['quiz', 'midterm', 'final', 'assignment'], {
    errorMap: () => ({ message: 'نوع الاختبار غير صحيح' })
  }),
  date: z.string().refine((date) => !isNaN(Date.parse(date)), {
    message: 'تاريخ غير صحيح'
  })
});

// Behavior note validation
export const behaviorNoteSchema = z.object({
  note: z.string()
    .min(10, 'الملاحظة يجب أن تكون على الأقل 10 أحرف')
    .max(500, 'الملاحظة طويلة جداً'),

  type: z.enum(['positive', 'negative', 'neutral'], {
    errorMap: () => ({ message: 'نوع الملاحظة غير صحيح' })
  }),

  date: z.string().refine((date) => !isNaN(Date.parse(date)), {
    message: 'تاريخ غير صحيح'
  })
});

// Excel upload validation
export const excelUploadSchema = z.object({
  file: z.instanceof(File)
    .refine((file) => file.size <= 5 * 1024 * 1024, 'حجم الملف يجب أن لا يتجاوز 5 ميجابايت')
    .refine(
      (file) => ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'].includes(file.type),
      'نوع الملف يجب أن يكون Excel'
    ),

  type: z.enum(['students', 'grades', 'attendance'], {
    errorMap: () => ({ message: 'نوع البيانات غير صحيح' })
  })
});

// API response validation
export const apiResponseSchema = z.object({
  success: z.boolean(),
  message: z.string().optional(),
  data: z.any().optional(),
  error: z.string().optional()
});

// Helper function to validate and format errors
export const validateAndFormatErrors = (schema, data) => {
  const result = schema.safeParse(data);

  if (!result.success) {
    const errors = {};
    result.error.errors.forEach((error) => {
      const path = error.path.join('.');
      errors[path] = error.message;
    });
    return { isValid: false, errors };
  }

  return { isValid: true, data: result.data };
};

// Custom validation hook
export const useValidation = () => {
  const validate = (schema, data) => {
    return validateAndFormatErrors(schema, data);
  };

  return { validate };
};
