from django.db import models
from Accounts.models import UserAuthentication
# Create your models here.

class student_homework(models.Model):
    name = models.CharField(max_length=120)
    username = models.CharField(max_length=10,primary_key=True)
    teacher = models.ForeignKey(to = UserAuthentication, on_delete=models.CASCADE)
    day2_work = models.TextField(null = True)
    day1_work = models.TextField(null = True)
    today_work = models.TextField(null = True)

    def __str__(self):
        return self.username


class Attendance(models.Model):
    email = models.ForeignKey(student_homework,on_delete=models.CASCADE)
    teacher = models.ForeignKey(to = UserAuthentication, on_delete=models.CASCADE)
    date = models.DateField(null = True)
    status = models.BooleanField(null = True)

    def __str__(self):
        return str(self.email)

class StudentFee(models.Model):
    email = models.ForeignKey(student_homework,on_delete=models.CASCADE)
    teacher = models.ForeignKey(to = UserAuthentication, on_delete = models.CASCADE)
    fee_date = models.CharField(null = True,max_length = 10)
    fee_amount = models.IntegerField()
    paid_status = models.BooleanField(null = True)
    fee_initiated_date = models.DateTimeField(auto_now_add=True)
    paid_date = models.DateTimeField(null = True)

    def __str__(self):
        return str(self.email)


