from django.contrib import admin

from Accounts.models import UserAuthentication
from .models import Attendance, student_homework, StudentFee
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    model = student_homework

    list_display = ('username','name','teacher')

    fieldsets = (
        ('Student Details',{'fields':('name','username','teacher')}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs['queryset'] = UserAuthentication.objects.filter(is_teacher = True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class FeeAdmin(admin.ModelAdmin):
    model = StudentFee

    list_display = ('email','fee_date','paid_status','paid_date','teacher')

    list_filter = ('fee_date','teacher','paid_status')


admin.site.register(student_homework,StudentAdmin)
admin.site.register(Attendance)
admin.site.register(StudentFee,FeeAdmin)