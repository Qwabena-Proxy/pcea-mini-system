from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index-page'),
    path('login/', loginView, name='login-page'),
    path('students/update-info/', updateStudentInfo, name='students-update-info'),
    path('students/dashboard/', dashBoard, name='students-dashboard'),
    path('activate/<str:uidb64>/<str:token>/<int:special>/', accountActivation, name='activate-account'),
]
