from django.contrib import messages
from django.shortcuts import render,redirect
from students.models import student_homework,StudentFee,Attendance
from Accounts.models import UserAuthentication,Teacher
from datetime import datetime as dt
from pytz import timezone
# Create your views here.

def parent_home(request):
    if request.method == "GET":
        tutions = Teacher.objects.all()
        return render(request,'parent_home.html',{'tutions':tutions})
    else:
        messages.warning(request,'Bad Request on parent home...please try again')
        return redirect('/accounts/login/')

def show_students_data(request):
    if request.method == "GET":
        student_key = request.GET.get('parent_contact','')
        if student_key == '':
            messages.error(request,'Parent Mobile Number is required...got empty')
            return redirect('/parents/home/')
        else:
            if student_homework.objects.filter(username = student_key).exists():
                student_data = student_homework.objects.get(username = student_key)
                att = []
                fee = []
                teacher = Teacher.objects.get(teacher = student_data.teacher)
                if Attendance.objects.filter(email = student_data).exists():
                    att = Attendance.objects.filter(email = student_data)
                    if StudentFee.objects.filter(email = student_key).exists():
                        fee = StudentFee.objects.filter(email = student_key)
                td = dt.now(timezone('Asia/Kolkata')).date()
                if teacher.notice_expiry == None:
                    notice = False
                elif td >= teacher.notice_expiry:
                    notice = False
                else:
                    notice = True
                return render(request,'parent_student_data.html',{
                    'student':student_data,
                    'att':att,
                    'fee':fee,
                    'teacher' : teacher,
                    'notice' : notice
                })
            else:
                messages.error(request,'Your Mobile Number not associated with any tution..please check with your tution teacher')
                return redirect('/parents/home/')
    else:
        messages.error(request,'Only POST requests are accepted..please try again')
        return redirect('/parents/home/')
