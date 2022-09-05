from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAuthentication,Teacher
# Register your models here.

class AuthAdmin(UserAdmin):
    model = UserAuthentication

    list_display = ('username','first_name','is_teacher','is_superuser')
    list_filter = ('is_teacher','is_superuser')

    fieldsets = (
        ('Register New Teacher',{'fields':('username','first_name','last_name','is_teacher','password')}),
        # (('Tution_Details'),{'fields':('tution_name','teacher','tution_address')}),
        (('Special Permissions'),{'fields':('is_active',)}),
        (('Important Dates'),{'fields':('last_login','date_joined')})
    )

    class Meta:
        model = UserAuthentication


admin.site.register(UserAuthentication,AuthAdmin)


class TeacherAdmin(admin.ModelAdmin):
    model = Teacher

    list_display = ('tution_name','teacher','tution_address')

    fieldsets = (
        ('Teacher_Details',{'fields':('tution_name','teacher','tution_address','notice_expiry')}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs['queryset'] = UserAuthentication.objects.filter(is_teacher = True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Teacher,TeacherAdmin)

admin.site.site_header = "Tution Management"
admin.site.site_title = "Tution Management"
admin.site.index_title = "Tution Management"
