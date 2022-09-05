from django.shortcuts import redirect, render
from .models import student_homework,Attendance,StudentFee
from Accounts.models import Teacher
from django.contrib import messages
from datetime import datetime as dt,timedelta
from pytz import timezone
# Create your views here.

def attendance(request):
    if request.user.is_authenticated and request.user.is_teacher:
        today = dt.now(timezone('Asia/Kolkata')).date()
        if request.method == 'POST':
            attendance_check_list = request.POST.getlist('attendance_checks')
            if len(attendance_check_list) == 0:
                messages.info(request,'Please select atleast one student to mark attendance')
                return redirect('/students/attendance/')
            else:
                students = student_homework.objects.filter(teacher = request.user)

                for student in students:
                    if student_homework.objects.filter(username = student.username,teacher = request.user):
                        user = student_homework.objects.get(username = student.username,teacher = request.user)
                        if  student.username in attendance_check_list:
                            if Attendance.objects.filter(email = user,date = today,teacher = request.user).exists():
                                att = Attendance.objects.get(email = user,date = today,teacher = request.user)
                                att.status = True
                                att.save()
                            else:
                                att = Attendance.objects.create(email = user,date = today,status = True,teacher = request.user)
                        else:
                            if Attendance.objects.filter(email = user,date = today,teacher = request.user).exists():
                                att = Attendance.objects.get(email = user,date = today,teacher = request.user)
                                att.status = False
                                att.save()
                            else:
                                att = Attendance.objects.create(email = user,date = today,status = False,teacher = request.user)

                messages.success(request,f'updated attendance for the mentioned students on date {today}')
                return redirect('/accounts/login/')
        else:
            if student_homework.objects.filter(teacher = request.user).exists():
                flag = Attendance.objects.filter(date = today,teacher = request.user).exists()
                if flag:
                    students = Attendance.objects.prefetch_related('email').filter(teacher = request.user,date = today)
                    return render(request,'student_attendance.html',{
                        'students':students,
                        'flag':flag,
                        'today' : today
                    })

                else:
                    students = student_homework.objects.filter(teacher = request.user)
                    return render(request,'student_attendance.html',{
                        'students':students,
                        'flag':flag,
                        'today' : today
                    })
            else:
                messages.warning(request,'No students in your tution...please add any')
                return redirect('/accounts/login/')
    else:
        messages.error(request,'you are not authenticated as teacher...please contact admin if the problem persists')
        return redirect('/accounts/login')

def generate_attendance(request):
    if request.user.is_authenticated and request.user.is_teacher:
        if student_homework.objects.filter(teacher = request.user).exists():
            if not Attendance.objects.filter(teacher = request.user).exists():
                messages.warning(request,"You haven't marked any attendance for in your students..please mark any to see the attendance report")
                return redirect('/accounts/login/')
            if request.method == 'GET':
                att = Attendance.objects.filter(teacher = request.user).order_by('email')
                students = student_homework.objects.filter(teacher = request.user).order_by('username')
                dates = Attendance.objects.filter(teacher = request.user).values('date').distinct().order_by('date')
                return render(request,'student_attendance_report.html',{
                    'students' : students,
                    'atts' : att,
                    'dates' : dates
                })
            else:
                messages.warning(request,'Bad request on generating attendance..please try again, if the problem persists contact admin')
                return redirect('/accounts/login/')
        else:
            messages.warning(request,'No students in you tution..please add if any')
            return redirect('/accounts/login/')
    else:
        messages.error(request,'you are not authenticated as teacher...please contact admin if the problem persists')
        return redirect('/accounts/login')

def generate_fees(request):
    if request.user.is_authenticated and request.user.is_teacher:
        if student_homework.objects.filter(teacher = request.user).exists():
            if not StudentFee.objects.filter(teacher = request.user).exists():
                messages.warning(request,"You haven't assigned any fee for in your students..please assign it to see the attendance report")
                return redirect('/accounts/login/')
            if request.method == 'GET':
                att = StudentFee.objects.filter(teacher = request.user).order_by('email')
                students = student_homework.objects.filter(teacher = request.user).order_by('username')
                dates = StudentFee.objects.filter(teacher = request.user).values('fee_date').distinct().order_by('fee_date')
                return render(request,'student_fee_report.html',{
                    'students' : students,
                    'atts' : att,
                    'dates' : dates
                })
            else:
                messages.warning(request,'Bad request on generating fees..please try again, if the problem persists contact admin')
                return redirect('/accounts/login/')
        else:
            messages.warning(request,'No students in you tution..please add if any')
            return redirect('/accounts/login/')
    else:
        messages.error(request,'you are not authenticated as teacher...please contact admin if the problem persists')
        return redirect('/accounts/login')

def add_student(request):
    if request.user.is_authenticated and request.user.is_teacher:
        if request.method == 'POST':
            student_name = request.POST.get('sname','')
            student_email = request.POST.get('email','')
            if student_name == '' or student_email == '':
                messages.error(request,'Please enter valid data')
                return redirect('/accounts/login')
            else:
                if student_homework.objects.filter(username = student_email).exists():
                    if student_homework.objects.filter(username = student_email,teacher = request.user):
                        student = student_homework.objects.get(username = student_email,teacher = request.user)
                        student.name = student_name
                        student.save()
                        messages.success(request,f'Student with email {student_email} has been updated successfully')
                        return redirect('/accounts/login/')
                    else:
                        messages.error(request,f'Student with mobile number {student_email} already associated with different teacher..please try again')
                        return redirect('/accounts/login/')
                else:
                    student_homework.objects.create(username=student_email,name=student_name,teacher = request.user)
                    messages.success(request,f'Student with email {student_email} has been created successfully')
                    return redirect('/accounts/login')
        else:
            messages.warning(request,'Bad Request on Adding Student..please try again later')
            return redirect('/accounts/login')
    else:
        messages.error(request,'you are not authenticated as teacher...please contact admin if the problem persists')
        return redirect('/accounts/login')

def del_student(request):
    if request.user.is_authenticated and request.user.is_teacher:
        if request.method == 'POST':
            checks = request.POST.getlist('student_checkbox')
            empty_students = []
            for student_email in checks:
                if student_homework.objects.filter(username = student_email,teacher = request.user).exists():
                    student = student_homework.objects.get(username = student_email,teacher = request.user)
                    deleted_tuple = student.delete()
                else:
                    empty_students.append(student_email)
            if len(empty_students) == 0:
                messages.success(request,'Deleted all selected students')
                return redirect('/accounts/login')
            else:
                messages.error(request,'Some students not associated with your tution and hence not eligible to delete')
                return redirect('/accounts/login')
        else:
            messages.warning(request,'Bad Request on removing Student..please try again later')
            return redirect('/accounts/login')
    else:
        messages.error(request,'you are not authenticated as teacher...please contact admin if the problem persists')
        return redirect('/accounts/login')

def update_homework(request):
    if request.user.is_authenticated and request.user.is_teacher:
        if request.method == 'POST':

            todays_check = request.POST.get('today_work_check','')
            if todays_check == '':
                flag = False
            else:
                flag = True
            
            students = student_homework.objects.filter(teacher = request.user)
            for student in students:
                text_val = request.POST.get(f'text_input_{student.username}','')
                if text_val == '' or text_val == 'None':
                    continue
                
                if student_homework.objects.filter(username = student.username,teacher = request.user):
                    s = student_homework.objects.get(username = student.username,teacher = request.user)
                    if flag:
                        s.today_work = text_val
                    else:
                        s.day2_work = s.day1_work
                        s.day1_work = s.today_work

                        s.today_work = text_val

                    s.save()
            if flag:
                messages.success(request,"Updated only today's homework")
            else:
                messages.success(request,'Updated last 3 days homework for the students')
            return redirect('/accounts/login/')

        else:
            if student_homework.objects.filter(teacher = request.user).exists():
                students = student_homework.objects.filter(teacher = request.user)
                return render(request,'student_homework.html',{
                    'students':students
                    # 'att':att
                })
            else:
                messages.warning(request,'No student in your tution please add any...')
                return redirect('/accounts/login/')
    else:
        messages.error(request,'you are not authenticated as teacher...please contact admin if the problem persists')
        return redirect('/accounts/login')

def update_student_fee(request):
    if request.user.is_authenticated and request.user.is_teacher:
        yearmonth = str(dt.now(timezone('Asia/Kolkata')).strftime('%Y-%m'))
        if request.method == 'POST':
            students = student_homework.objects.filter(teacher = request.user)
            print('students')
            print(len(list(students)))
            for student in students:
                if student_homework.objects.filter(username = student.username,teacher =  request.user).exists():
                    sid = student_homework.objects.get(username = student.username,teacher = request.user)
                    print(f'fee_text_{student.username}')
                    text_val = request.POST.get(f'fee_text_{student.username}','')
                    # print(text_val)
                    if text_val == '' or text_val == 'None' or not text_val.isdigit():
                        continue
                    if StudentFee.objects.filter(teacher = request.user,email = student.username,fee_date = yearmonth).exists():
                        s = StudentFee.objects.get(email = sid,teacher = request.user,fee_date = yearmonth)
                        s.paid_status = False
                        s.fee_amount = text_val
                        s.save()
                    else:
                        StudentFee.objects.create(teacher = request.user,email = sid,fee_date = yearmonth,paid_status=False,fee_amount = text_val)
            tution = Teacher.objects.get(teacher = request.user)
            tution.tution_notice = f'Tution Fee for the month {yearmonth} assigned for the student. Please ignore if already paid'
            tution.notice_expiry = dt.now(timezone('Asia/Kolkata')).date()+timedelta(days = 3)
            tution.save()
            messages.success(request,'Assigned Fee for students successfully')
            return redirect('/accounts/login/')
    
        else:
            if student_homework.objects.filter(teacher = request.user).exists():
                if StudentFee.objects.filter(teacher = request.user,fee_date = yearmonth).exists():

                    students = StudentFee.objects.prefetch_related("email").filter(teacher = request.user,fee_date = yearmonth)
                    return render(request,'student_fee.html',{
                        'students':students,
                        'fee_exists' : True
                        # 'att':att
                    })
                else:
                    students = student_homework.objects.filter(teacher = request.user)
                    return render(request,'student_fee.html',{
                        'students':students,
                        'fee_exists' : False,
                        'fee_date' : yearmonth
                    })
            else:
                messages.warning(request,'No student in your tution please add any...')
                return redirect('/accounts/login/')
    else:
        messages.error(request,'you are not authenticated as teacher...please contact admin if the problem persists')
        return redirect('/accounts/login')

def mark_as_paid(request):
    if request.user.is_authenticated and request.user.is_teacher:
        if request.method == 'POST':
            students = request.POST.getlist('student_fee_checkbox','')
            if students == '':
                messages.error(request,'Please select atleast one student to mark as paid')
                return redirect('/students/update_student_fee/')
            else:
                for student_key in students:
                    if student_homework.objects.filter(username = student_key,teacher = request.user).exists():
                        yearmonth = str(dt.now(timezone('Asia/Kolkata')).strftime('%Y-%m'))
                        student = student_homework.objects.get(username = student_key,teacher = request.user)
                        if StudentFee.objects.filter(email = student,teacher = request.user,fee_date = yearmonth,paid_status = False).exists():
                            fee = StudentFee.objects.get(email = student,teacher = request.user,fee_date = yearmonth,paid_status = False)
                            fee.paid_status = True
                            fee.paid_date = dt.now(timezone('Asia/Kolkata'))
                            fee.save()
                        
                messages.success(request,f'All selected students marked as paid for the month {yearmonth}')
                return redirect('/accounts/login/')
        else:
            messages.warning(request,'Bad Request on marking student as paid..please try again later')
            return redirect('/accounts/login')
    else:
        messages.error(request,'you are not authenticated as teacher...please contact admin if the problem persists')
        return redirect('/accounts/login')

