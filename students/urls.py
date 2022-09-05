from django.urls import path
from . import views

urlpatterns = [
    path('attendance/',views.attendance,name = 'attendance'),
    path('addstudent/',views.add_student,name = "Add Student"),
    path('deletestudent/',views.del_student,name = 'Delete Student'),
    path('update_homework/',views.update_homework, name = 'update homework'),
    path('generate_attendance/',views.generate_attendance,name = 'Generating attendance Sheets'),
    path('generate_fees/',views.generate_fees,name = 'Generating fee Sheets'),
    path('update_student_fee/',views.update_student_fee,name='Student Fee'),
    path('markaspaid/',views.mark_as_paid,name="mark student as paid fee")
]