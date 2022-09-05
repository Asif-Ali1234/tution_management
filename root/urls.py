from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.root, name = "root"),
    path('accounts/',include('Accounts.urls')),
    path('students/',include('students.urls')),
    path('parents/',include('parents.urls'))
]