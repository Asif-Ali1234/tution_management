from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserAuthentication(AbstractUser):
    username=models.CharField(max_length=10,primary_key=True)
    Address=models.CharField(max_length=1024)
    is_teacher = models.BooleanField(blank = True, null = True)
    is_parent = models.BooleanField(blank = True,null = True)

    def __str__(self):
        return self.username


class Teacher(models.Model):
    teacher = models.OneToOneField(to = UserAuthentication,on_delete=models.CASCADE)
    # teacher = models.ForeignKey(to=UserAuthentication,on_delete=models.CASCADE)
    tution_name = models.CharField(max_length=1024)
    tution_address = models.CharField(max_length=1024)
    tution_notice = models.CharField(max_length = 2048)
    notice_expiry = models.DateField(null = True,blank = True)

    def __str__(self):
        return str(self.teacher)

