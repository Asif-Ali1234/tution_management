from django.urls import path,include
from . import views

urlpatterns = [
    path('home/',views.parent_home,name="parent home"),
    path('show_data/',views.show_students_data,name="Showing Student Data")
]