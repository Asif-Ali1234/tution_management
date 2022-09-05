from django.contrib import messages
from django.contrib.auth.models import auth
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
import time
from .models import UserAuthentication as User_Authentication,Teacher
from students.models import student_homework,Attendance,StudentFee
from datetime import datetime as dt
from pytz import timezone
from tution_tutorials.settings import ALLOWED_HOSTS as domain

# Create your views here.

otpdict={}

registerotpdict = {}

attemptsdict={}

def get_render_context(user):
    if student_homework.objects.filter(teacher = user).exists():
        # students exists for the teacher
        students = student_homework.objects.filter(teacher = user)
    else:
        students = None
    # check if any tution is associated with the teacher
    tution = Teacher.objects.get(teacher = user)
    no_of_students = 0 if students == None else len(students)
    today = dt.now(timezone('Asia/Kolkata')).date()
    # checking if the attendance for today taken or not
    flag = Attendance.objects.filter(date = today,teacher = user).exists()
    parent_link = f'{domain[0]}/parents/home/'
    td = dt.now(timezone('Asia/Kolkata')).date()
    yearmonth = str(dt.now(timezone('Asia/Kolkata')).strftime('%Y-%m'))
    if StudentFee.objects.filter(teacher = user,fee_date = yearmonth).exists():
        fee_exists = True
    else:
        fee_exists = False
    if tution.notice_expiry == None:
        new_notice = True
    elif td < tution.notice_expiry:
        new_notice = False
    else:
        new_notice = True
    render_context = {
        'students':students,
        'count':no_of_students,
        'button_check':flag,
        'tution' : tution,
        'parent_link':parent_link,
        'new_notice':new_notice,
        'fee_exists':fee_exists
    }
    return render_context

def login(request):
    if request.user.is_authenticated and request.user.is_teacher:
        # user is already authenticated and user is the teacher
        render_context = get_render_context(request.user)
        return render(request,"After_login_page.html",render_context)

    elif request.user.is_authenticated and request.user.is_superuser:
        return redirect('/admin/')
    
    if request.method=="POST":
        username=request.POST["username"]
        passwd=request.POST["passwd"]
        # Authenticating User with username and password
        user=auth.authenticate(username=username,password=passwd)
        if User_Authentication.objects.filter(username=username,is_teacher = True).exists():
            # checking username and password
            if user is not None:
                if Teacher.objects.filter(teacher = username).exists():
                    # logging the user and rendering the after login page
                    auth.login(request,user)
                    render_context = get_render_context(user)
                    return render(request,"After_login_page.html",render_context)

                else:
                    messages.info(request,f'No tution associated with the user - {username}..please contact admin')
                    return redirect('/accounts/login/')
            else:
                # username and password is not matched...redirecting to login
                messages.error(request,"Username and Password is not matched")
                return redirect("/accounts/login/")
        else:
            messages.warning(request,"Sorry...this account is not registered as Teacher!!! Please contact Admin")
            return redirect('/accounts/login/')
    else:
        return render(request,"login.html")
    
    
def logout(request):
    auth.logout(request)
    messages.info(request,"You have been logged out Successfully")
    return redirect("/")

# def ContactUs(request):
#     if request.method=="POST":
#         username=request.POST["useremail"]
#         firstname=request.POST["userfirstname"]
#         lastname=request.POST['userlastname']
#         number=request.POST['usermobilenumber']
#         message=request.POST['usermessage']
#         if Contact_Messages.objects.filter(username=username).exists():
#             user=Contact_Messages.objects.get(username=username)
#             msg=user.message+'\n$#!  '+message
#             user.user_firstname=firstname
#             user.user_lastname=lastname
#             user.user_mobilenumber=number
#             user.message=msg
#             user.save()
#             messages.success(request, "You have sent "+str(msg.count('$#!'))+" messages we will definitely look into it Please wait for us to take action")
#             return render(request,'contact_us.html')
#         else:
#             message="$#!  "+message
#             Contact_Messages.objects.create(username=username,user_firstname=firstname,
#             user_lastname=lastname,user_mobilenumber=number,message=message)
#             messages.success(request, "You Message has been sent we will definitely respond to it via Email within in a day check out your Email")
#             return render(request,'contact_us.html')
#     else:
#         return render(request,"contact_us.html")

# def forgotpassword(request):
#     # function for otp generation
#     if(request.method=="POST"):
#         otp=""
#         for i in range(6):
#             otp+=str(r.randint(1,9))
#         receiver=request.POST["receiver_name"]
#         if User_Authentication.objects.filter(username=receiver).exists():
#             userdetails=User_Authentication.objects.get(username=receiver)
#             firstname=userdetails.first_name
#             # send_mail('[Resume Generator]Please Reset Your Password','Hello '+ str(firstname) +' , Warm Regards \n'+'\nIt seems you have forgotten your Account Password\n'+'\nBut don\'t worry You can Reset your Password  Using OTP below :\n'+'\n\t\t\t\t\tYour Otp to reset password is '+str(otp)+'\n\n\n\nThanks,\nThe Resume Generator Team',primary_mail,
#             # [receiver,],fail_silently=False)
#             otpdict[receiver]=otp
#             attemptsdict[receiver]=3
#             messages.info(request,"OTP has been sent to your registered Email Id or Username")
#             return render(request,"otp_verification.html",{'name':receiver})
#         else:
#             messages.error(request,"Username doesn't exist.Please Enter Valid Username")
#             return redirect("forgotpassword")
#     else:
#         return render(request,'forgotpassword.html')

# def verifyotp(request):
#     if(request.method=="POST"):
#         user_otp=request.POST["user_otp"]
#         receiver=request.POST["receiver"]
#         try:
#             otp=otpdict[receiver]
#             if attemptsdict[receiver]>0:

#                 if(otp==user_otp):
#                     del(otpdict[receiver])
#                     attemptsdict[receiver]=0
#                     return render(request,"change_passwd.html",{'name':receiver})
#                 else:
#                     messages.error(request,"Otp is not matched Please Try Again")
#                     atemptstr="Remaining Attempts : "+str(attemptsdict[receiver])
#                     attemptsdict[receiver]-=1
#                     return render(request,"otp_verification.html",{'name':receiver,'attempts':atemptstr})
#             elif attemptsdict[receiver]==0:
#                 messages.error(request,"Otp Attempts limit reached . Please Generate Again")
#                 return redirect("forgotpassword")
#         except KeyError:
#             messages.error(request,"The otp generated has expired or deleted Please regenerate again")
#             return redirect("forgotpassword")
#     else:
#         return render(request,"otp_verification.html")


# def changepassword(request):
#     if(request.method=="POST"):
#         requested_user=request.POST["change_requested_user"]
#         passwd=request.POST["npasswd"]
#         cnfrmpasswd=request.POST["cnfrmpasswd"]
#         if passwd==cnfrmpasswd:
#             user=User_Authentication.objects.get(username=requested_user)
#             user.set_password(passwd)
#             user.save()
#             auth.logout(request)
#             firstname=user.first_name
#             # send_mail('[Resume Generator]Password Changed','Hello '+str(firstname)+' , Security Threat \n'+'\nYour password for the the account '+str(requested_user[:3])+'*'*int(len(str(requested_user)))+str(requested_user[::-1][:3][::-1]) +' has changed recently \n'+'\nIf you don\'t change your password contact us Immediately with your details'+'\n\n If this was you simply ignore this email '+'\n\n\n\nThanks,\nThe Resume Generator Team',primary_mail,
#             # [requested_user,],fail_silently=False)
#             messages.success(request,"Your password has been successfully changed Please login again")
#             return redirect("login")
#         else:
#             messages.warning(request,"Passwords Not Matched")
#             return render(request,"change_passwd.html",{'name':requested_user})
#     else:
#         return render(request,"change_passwd.html")

# def changepasswordafterlogin(request):
#     if request.method == "POST":
#         curpasswd=request.POST["oldpasswd"]
#         username=request.user
#         userauth=auth.authenticate(username=username,password=curpasswd)
#         if userauth is None:
#             messages.error(request,"Current Password not matched Please try again or reset it by signing out")
#             return redirect('changepasswordafterlogin')
#         else:
#             passwd=request.POST["newpasswd"]
#             cnfrmpasswd=request.POST["cnfrmpasswd"]
#             if passwd==cnfrmpasswd:
#                 user=User_Authentication.objects.get(username=username)
#                 user.set_password(passwd)
#                 user.save()
#                 auth.logout(request)
#                 firstname=user.first_name
#                 # send_mail('[Resume Generator]Password Changed','Hello '+str(firstname)+' , Security Threat \n'+'\nYour password for the the account '+str(username)+' has changed recently \n'+'\nIf you don\'t change your password contact us Immediately with your details'+'\n\n If this was you simply ignore this email '+'\n\n\n\nThanks,\nThe Resume Generator Team',primary_mail,
#                 # [username,],fail_silently=False)
#                 messages.success(request,"Your password has been successfully changed Please login again")
#                 return redirect("login")
#             else:
#                 messages.error(request,"Passwords not matched Please try again")
#                 return redirect('changepasswordafterlogin')
#     else:
#         return render(request,'chngpasswdaftrlgn.html')

# def deleteaccount(request):
#     if request.method=="POST":
#         username=request.user

#         userpasswd=request.POST['reqpasswd']

#         userauth=auth.authenticate(username=username,password=userpasswd)

#         if userauth is None:
#             messages.error(request,'Password not matched with your account')

#             return render(request,'deleteaccount.html',{'username':username})

#         else:
#             auth.logout(request)

#             user=User_Authentication.objects.get(username=username)

#             deletedtuple=user.delete()

#             totalsavings=deletedtuple[0]

#             messages.warning(request,'we have deleted '+str(totalsavings)+' fields of you , If you face any problems feel free to contact us')
#             return redirect("/")


#     else:
#         return render(request,'deleteaccount.html',{'username':request.user})

# def checkusername(request):
#     username = request.GET['username']

#     if User_Authentication.objects.filter(username=username).exists():
#             time.sleep(2)
#             data = {
#                 'error':True,
#                 'msg':'Username already exists Please try again',
#             }
#             return JsonResponse(data)
    
#     else:
#         otp=""
#         for i in range(6):
#             otp+=str(r.randint(1,9))
#         time.sleep(1)
#         # send_mail('[Resume Generator]Verify Email','Please give the below OTP in order to verify your account registered with Resume Generator'+'\nOTP is '+str(otp)+'\n\n\n\nThanks,\nThe Resume Generator Team',primary_mail,
#         #         [username,],fail_silently=False)
#         registerotpdict[username] = otp

#         data = {
#             'error':False,
#             'msg':'OTP has been sent to your mail',
#         }

#         return JsonResponse(data)

# def verifyregistrationotp(request):
#     otp = request.GET['registerotp']

#     username = request.GET['username']

#     if username in registerotpdict.keys():
#         time.sleep(2)
#         if registerotpdict[username] == otp:
#             data = {
#                 'error':False,
#             }
#             del(registerotpdict[username])
#         else:
#             data = {
#                 'error':True,
#                 'msg':'OTP is not matched or Invalid Please try again'
#             }
#     else:
#         time.sleep(1)
#         data = {
#             'error':True,
#             'msg':'OTP is not generated for this mail Please generate again'
#         }

#     return JsonResponse(data)

def checkloginusername(request):
    username = request.GET['username']

    time.sleep(1)

    if User_Authentication.objects.filter(username=username).exists():
        data = {
            'error':False
        }
    else:
        data = {
            'error':True,
            'msg':"Username doesn't exists please try again"
        }

    return JsonResponse(data)

def update_tution(request):
    if request.user.is_authenticated and request.user.is_teacher:
        if request.method == 'POST':
            tution_name = request.POST.get('tution_name','')
            tution_addr = request.POST.get('tution_addr','')
            if tution_name != '' or tution_addr != '':
                teacher = Teacher.objects.get(teacher = request.user)
                teacher.tution_name = tution_name
                teacher.tution_address = tution_addr
                teacher.save()
                messages.success(request,'successfully updated tution details...')
                return redirect('/accounts/login/')
            else:
                messages.error(request,'parameters not properly passed for updating..please try again')
                return redirect('/accounts/login/')
        else:
            messages.error(request,'Bad request on updating tution detials please try again..if the problem persists contact admin')
            return redirect('/accounts/login/')
    else:
        messages.warning(request,'you are not authenticated as teacher..please contact admin')
        return redirect('/accounts/login/')

def update_notice(request):
    if request.user.is_authenticated and request.user.is_teacher:
        if request.method == 'POST':
            tution_notice = request.POST.get('tution_notice','')
            expiry = request.POST.get('notice_expiry','')
            if tution_notice != '':
                teacher = Teacher.objects.get(teacher = request.user)
                teacher.tution_notice = tution_notice
                if expiry != '':
                    teacher.notice_expiry = expiry   
                teacher.save()
                messages.success(request,'successfully updated tution notice...')
                return redirect('/accounts/login/')

            else:
                messages.error(request,'parameters not properly passed for updating..please try again')
                return redirect('/accounts/login/')
        else:
            messages.error(request,'Bad request on updating tution detials please try again..if the problem persists contact admin')
            return redirect('/accounts/login/')
    else:
        messages.warning(request,'you are not authenticated as teacher..please contact admin')
        return redirect('/accounts/login/')

def delete_notice(request):
    if request.user.is_authenticated and request.user.is_teacher:
        if request.method == 'GET':
            teacher = Teacher.objects.get(teacher = request.user)
            teacher.tution_notice = ''
            teacher.notice_expiry = None   
            teacher.save()
            messages.warning(request,'successfully deleted tution notice...')
            return redirect('/accounts/login/')
        else:
            messages.error(request,'Bad request on updating tution detials please try again..if the problem persists contact admin')
            return redirect('/accounts/login/')
    else:
        messages.warning(request,'you are not authenticated as teacher..please contact admin')
        return redirect('/accounts/login/')
