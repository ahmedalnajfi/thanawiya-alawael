import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { 
  BookOpen, 
  Users, 
  Calendar, 
  MessageSquare,
  LogOut,
  Plus,
  Save,
  Clock,
  CheckCircle,
  AlertCircle,
  Star,
  TrendingUp
} from 'lucide-react'

const TeacherDashboard = ({ user, onLogout }) => {
  const [selectedClass, setSelectedClass] = useState('3أ')
  const [newGrade, setNewGrade] = useState({ student: '', subject: '', grade: '', type: '' })
  const [newNote, setNewNote] = useState({ student: '', note: '', type: 'positive' })

  // بيانات تجريبية للمعلم
  const teacherData = {
    name: 'د. محمد علي أحمد',
    subjects: ['الرياضيات', 'الفيزياء'],
    classes: ['3أ', '3ب', '2أ'],
    students: [
      {
        id: 'S001',
        name: 'أحمد محمد علي',
        class: '3أ',
        avatar: '/api/placeholder/50/50',
        grades: [
          { subject: 'الرياضيات', grade: 85, date: '2024-01-20', type: 'امتحان' },
          { subject: 'الفيزياء', grade: 78, date: '2024-01-18', type: 'واجب' }
        ],
        attendance: {
          present: 18,
          absent: 2,
          late: 1,
          total: 21
        },
        behavior: [
          { date: '2024-01-15', type: 'positive', note: 'مشاركة ممتازة في الحصة' },
          { date: '2024-01-10', type: 'positive', note: 'ساعد زميله في حل المسائل' }
        ],
        engagement: 8,
        focus: 7,
        participation: 9
      },
      {
        id: 'S002',
        name: 'فاطمة أحمد محمد',
        class: '3أ',
        avatar: '/api/placeholder/50/50',
        grades: [
          { subject: 'الرياضيات', grade: 92, date: '2024-01-20', type: 'امتحان' },
          { subject: 'الفيزياء', grade: 88, date: '2024-01-18', type: 'واجب' }
        ],
        attendance: {
          present: 20,
          absent: 1,
          late: 0,
          total: 21
        },
        behavior: [
          { date: '2024-01-16', type: 'positive', note: 'تفوق في حل المسائل المعقدة' },
          { date: '2024-01-12', type: 'positive', note: 'قيادة ممتازة في العمل الجماعي' }
        ],
        engagement: 10,
        focus: 9,
        participation: 10
      },
      {
        id: 'S003',
        name: 'عبدالله سالم',
        class: '3أ',
        avatar: '/api/placeholder/50/50',
        grades: [
          { subject: 'الرياضيات', grade: 65, date: '2024-01-20', type: 'امتحان' },
          { subject: 'الفيزياء', grade: 70, date: '2024-01-18', type: 'واجب' }
        ],
        attendance: {
          present: 16,
          absent: 4,
          late: 1,
          total: 21
        },
        behavior: [
          { date: '2024-01-14', type: 'neutral', note: 'يحتاج إلى مزيد من التركيز' },
          { date: '2024-01-08', type: 'negative', note: 'تأخر عن الحصة' }
        ],
        engagement: 5,
        focus: 4,
        participation: 6
      }
    ],
    todaySchedule: [
      { time: '08:00', class: '3أ', subject: 'الرياضيات', room: '101' },
      { time: '09:00', class: '3ب', subject: 'الفيزياء', room: '205' },
      { time: '10:30', class: '2أ', subject: 'الرياضيات', room: '101' },
      { time: '12:00', class: '3أ', subject: 'الفيزياء', room: '205' }
    ]
  }

  const currentClassStudents = teacherData.students.filter(s => s.class === selectedClass)

  const handleAddGrade = () => {
    if (newGrade.student && newGrade.subject && newGrade.grade && newGrade.type) {
      // هنا سيتم إضافة الدرجة إلى قاعدة البيانات
      console.log('Adding grade:', newGrade)
      setNewGrade({ student: '', subject: '', grade: '', type: '' })
      alert('تم إضافة الدرجة بنجاح')
    }
  }

  const handleAddNote = () => {
    if (newNote.student && newNote.note) {
      // هنا سيتم إضافة الملاحظة إلى قاعدة البيانات
      console.log('Adding note:', newNote)
      setNewNote({ student: '', note: '', type: 'positive' })
      alert('تم إضافة الملاحظة بنجاح')
    }
  }

  const markAttendance = (studentId, status) => {
    // هنا سيتم تسجيل الحضور
    console.log('Marking attendance:', studentId, status)
    alert(`تم تسجيل ${status} للطالب`)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <BookOpen className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">ثانوية الأوائل</h1>
                <p className="text-sm text-gray-500">لوحة المعلم</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">{teacherData.name}</p>
                <p className="text-xs text-gray-500">معلم {teacherData.subjects.join(' و ')}</p>
              </div>
              <Avatar>
                <AvatarFallback>مع</AvatarFallback>
              </Avatar>
              <Button variant="outline" size="sm" onClick={onLogout}>
                <LogOut className="w-4 h-4 ml-2" />
                تسجيل الخروج
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">مرحباً، {teacherData.name}</h2>
          <p className="text-gray-600">إدارة شاملة لدرجات وحضور وسلوك الطلاب</p>
        </div>

        {/* Today's Schedule */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="w-5 h-5" />
              جدول اليوم
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {teacherData.todaySchedule.map((lesson, index) => (
                <div key={index} className="p-4 border rounded-lg bg-blue-50">
                  <div className="flex items-center justify-between mb-2">
                    <Badge variant="outline">{lesson.time}</Badge>
                    <Badge>{lesson.class}</Badge>
                  </div>
                  <h3 className="font-medium text-gray-900">{lesson.subject}</h3>
                  <p className="text-sm text-gray-600">قاعة {lesson.room}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Class Selector */}
        <div className="mb-6">
          <Label htmlFor="class-select" className="text-base font-medium">اختر الفصل:</Label>
          <Select value={selectedClass} onValueChange={setSelectedClass}>
            <SelectTrigger className="w-48 mt-2">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {teacherData.classes.map((cls) => (
                <SelectItem key={cls} value={cls}>{cls}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">عدد الطلاب</p>
                  <p className="text-2xl font-bold text-blue-600">{currentClassStudents.length}</p>
                </div>
                <Users className="w-8 h-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">متوسط الحضور</p>
                  <p className="text-2xl font-bold text-green-600">
                    {Math.round(currentClassStudents.reduce((sum, s) => sum + (s.attendance.present / s.attendance.total * 100), 0) / currentClassStudents.length)}%
                  </p>
                </div>
                <CheckCircle className="w-8 h-8 text-green-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">متوسط الدرجات</p>
                  <p className="text-2xl font-bold text-purple-600">
                    {Math.round(currentClassStudents.reduce((sum, s) => sum + s.grades.reduce((gSum, g) => gSum + g.grade, 0) / s.grades.length, 0) / currentClassStudents.length)}
                  </p>
                </div>
                <TrendingUp className="w-8 h-8 text-purple-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">الملاحظات الإيجابية</p>
                  <p className="text-2xl font-bold text-orange-600">
                    {currentClassStudents.reduce((sum, s) => sum + s.behavior.filter(b => b.type === 'positive').length, 0)}
                  </p>
                </div>
                <Star className="w-8 h-8 text-orange-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Tabs */}
        <Tabs defaultValue="students" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="students">الطلاب</TabsTrigger>
            <TabsTrigger value="grades">إدخال الدرجات</TabsTrigger>
            <TabsTrigger value="attendance">تسجيل الحضور</TabsTrigger>
            <TabsTrigger value="notes">الملاحظات السلوكية</TabsTrigger>
          </TabsList>

          {/* Students Overview */}
          <TabsContent value="students">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="w-5 h-5" />
                  نظرة عامة على طلاب فصل {selectedClass}
                </CardTitle>
                <CardDescription>
                  معلومات شاملة عن أداء وسلوك الطلاب
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {currentClassStudents.map((student) => (
                    <div key={student.id} className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-3">
                          <Avatar>
                            <AvatarImage src={student.avatar} />
                            <AvatarFallback>{student.name.charAt(0)}</AvatarFallback>
                          </Avatar>
                          <div>
                            <h3 className="font-medium text-gray-900">{student.name}</h3>
                            <p className="text-sm text-gray-600">فصل {student.class}</p>
                          </div>
                        </div>
                        <div className="flex gap-2">
                          <Badge variant="outline">
                            متوسط: {Math.round(student.grades.reduce((sum, g) => sum + g.grade, 0) / student.grades.length)}
                          </Badge>
                          <Badge variant={student.attendance.present / student.attendance.total >= 0.9 ? 'default' : 'destructive'}>
                            حضور: {Math.round(student.attendance.present / student.attendance.total * 100)}%
                          </Badge>
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="space-y-2">
                          <Label className="text-sm font-medium">مستوى المشاركة</Label>
                          <div className="flex items-center gap-2">
                            <div className="flex-1 bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-blue-600 h-2 rounded-full" 
                                style={{ width: `${student.engagement * 10}%` }}
                              ></div>
                            </div>
                            <span className="text-sm text-gray-600">{student.engagement}/10</span>
                          </div>
                        </div>

                        <div className="space-y-2">
                          <Label className="text-sm font-medium">مستوى التركيز</Label>
                          <div className="flex items-center gap-2">
                            <div className="flex-1 bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-green-600 h-2 rounded-full" 
                                style={{ width: `${student.focus * 10}%` }}
                              ></div>
                            </div>
                            <span className="text-sm text-gray-600">{student.focus}/10</span>
                          </div>
                        </div>

                        <div className="space-y-2">
                          <Label className="text-sm font-medium">المشاركة الاجتماعية</Label>
                          <div className="flex items-center gap-2">
                            <div className="flex-1 bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-purple-600 h-2 rounded-full" 
                                style={{ width: `${student.participation * 10}%` }}
                              ></div>
                            </div>
                            <span className="text-sm text-gray-600">{student.participation}/10</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Add Grades */}
          <TabsContent value="grades">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Plus className="w-5 h-5" />
                  إدخال الدرجات
                </CardTitle>
                <CardDescription>
                  إضافة درجات جديدة للطلاب
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="student-select">الطالب</Label>
                      <Select value={newGrade.student} onValueChange={(value) => setNewGrade({...newGrade, student: value})}>
                        <SelectTrigger>
                          <SelectValue placeholder="اختر الطالب" />
                        </SelectTrigger>
                        <SelectContent>
                          {currentClassStudents.map((student) => (
                            <SelectItem key={student.id} value={student.id}>{student.name}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label htmlFor="subject-select">المادة</Label>
                      <Select value={newGrade.subject} onValueChange={(value) => setNewGrade({...newGrade, subject: value})}>
                        <SelectTrigger>
                          <SelectValue placeholder="اختر المادة" />
                        </SelectTrigger>
                        <SelectContent>
                          {teacherData.subjects.map((subject) => (
                            <SelectItem key={subject} value={subject}>{subject}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label htmlFor="grade-input">الدرجة</Label>
                      <Input
                        id="grade-input"
                        type="number"
                        min="0"
                        max="100"
                        value={newGrade.grade}
                        onChange={(e) => setNewGrade({...newGrade, grade: e.target.value})}
                        placeholder="أدخل الدرجة"
                      />
                    </div>

                    <div>
                      <Label htmlFor="type-select">نوع التقييم</Label>
                      <Select value={newGrade.type} onValueChange={(value) => setNewGrade({...newGrade, type: value})}>
                        <SelectTrigger>
                          <SelectValue placeholder="اختر نوع التقييم" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="امتحان">امتحان</SelectItem>
                          <SelectItem value="واجب">واجب</SelectItem>
                          <SelectItem value="مشاركة">مشاركة</SelectItem>
                          <SelectItem value="مشروع">مشروع</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <Button onClick={handleAddGrade} className="w-full">
                      <Save className="w-4 h-4 ml-2" />
                      حفظ الدرجة
                    </Button>
                  </div>

                  <div className="space-y-4">
                    <h3 className="font-medium text-gray-900">الدرجات الأخيرة</h3>
                    <div className="space-y-3 max-h-96 overflow-y-auto">
                      {currentClassStudents.flatMap(student => 
                        student.grades.map((grade, index) => (
                          <div key={`${student.id}-${index}`} className="p-3 border rounded-lg">
                            <div className="flex items-center justify-between">
                              <div>
                                <p className="font-medium text-gray-900">{student.name}</p>
                                <p className="text-sm text-gray-600">{grade.subject} - {grade.type}</p>
                              </div>
                              <div className="text-left">
                                <Badge variant={grade.grade >= 85 ? 'default' : grade.grade >= 70 ? 'secondary' : 'destructive'}>
                                  {grade.grade}/100
                                </Badge>
                                <p className="text-xs text-gray-500 mt-1">{grade.date}</p>
                              </div>
                            </div>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Attendance */}
          <TabsContent value="attendance">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="w-5 h-5" />
                  تسجيل الحضور - فصل {selectedClass}
                </CardTitle>
                <CardDescription>
                  تسجيل حضور وغياب الطلاب لليوم
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {currentClassStudents.map((student) => (
                    <div key={student.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center gap-3">
                        <Avatar>
                          <AvatarImage src={student.avatar} />
                          <AvatarFallback>{student.name.charAt(0)}</AvatarFallback>
                        </Avatar>
                        <div>
                          <h3 className="font-medium text-gray-900">{student.name}</h3>
                          <p className="text-sm text-gray-600">
                            نسبة الحضور: {Math.round(student.attendance.present / student.attendance.total * 100)}%
                          </p>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <Button 
                          size="sm" 
                          variant="outline"
                          onClick={() => markAttendance(student.id, 'حاضر')}
                          className="text-green-600 border-green-600 hover:bg-green-50"
                        >
                          <CheckCircle className="w-4 h-4 ml-1" />
                          حاضر
                        </Button>
                        <Button 
                          size="sm" 
                          variant="outline"
                          onClick={() => markAttendance(student.id, 'غائب')}
                          className="text-red-600 border-red-600 hover:bg-red-50"
                        >
                          <AlertCircle className="w-4 h-4 ml-1" />
                          غائب
                        </Button>
                        <Button 
                          size="sm" 
                          variant="outline"
                          onClick={() => markAttendance(student.id, 'متأخر')}
                          className="text-yellow-600 border-yellow-600 hover:bg-yellow-50"
                        >
                          <Clock className="w-4 h-4 ml-1" />
                          متأخر
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Behavior Notes */}
          <TabsContent value="notes">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MessageSquare className="w-5 h-5" />
                  الملاحظات السلوكية
                </CardTitle>
                <CardDescription>
                  إضافة ملاحظات حول سلوك ومشاركة الطلاب
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="note-student-select">الطالب</Label>
                      <Select value={newNote.student} onValueChange={(value) => setNewNote({...newNote, student: value})}>
                        <SelectTrigger>
                          <SelectValue placeholder="اختر الطالب" />
                        </SelectTrigger>
                        <SelectContent>
                          {currentClassStudents.map((student) => (
                            <SelectItem key={student.id} value={student.id}>{student.name}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label htmlFor="note-type-select">نوع الملاحظة</Label>
                      <Select value={newNote.type} onValueChange={(value) => setNewNote({...newNote, type: value})}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="positive">إيجابية</SelectItem>
                          <SelectItem value="neutral">محايدة</SelectItem>
                          <SelectItem value="negative">سلبية</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label htmlFor="note-text">الملاحظة</Label>
                      <Textarea
                        id="note-text"
                        value={newNote.note}
                        onChange={(e) => setNewNote({...newNote, note: e.target.value})}
                        placeholder="اكتب ملاحظتك هنا..."
                        rows={4}
                      />
                    </div>

                    <Button onClick={handleAddNote} className="w-full">
                      <Save className="w-4 h-4 ml-2" />
                      حفظ الملاحظة
                    </Button>
                  </div>

                  <div className="space-y-4">
                    <h3 className="font-medium text-gray-900">الملاحظات الأخيرة</h3>
                    <div className="space-y-3 max-h-96 overflow-y-auto">
                      {currentClassStudents.flatMap(student => 
                        student.behavior.map((note, index) => (
                          <div key={`${student.id}-${index}`} className="p-3 border rounded-lg">
                            <div className="flex items-start justify-between mb-2">
                              <Badge variant={
                                note.type === 'positive' ? 'default' : 
                                note.type === 'negative' ? 'destructive' : 'secondary'
                              }>
                                {note.type === 'positive' ? 'إيجابي' : 
                                 note.type === 'negative' ? 'سلبي' : 'محايد'}
                              </Badge>
                              <span className="text-xs text-gray-500">{note.date}</span>
                            </div>
                            <p className="font-medium text-gray-900 mb-1">{student.name}</p>
                            <p className="text-sm text-gray-600">{note.note}</p>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}

export default TeacherDashboard

