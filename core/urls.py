from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index-page'),
    path('login/', loginView, name='login-page'),
    path('students/update-info/', updateStudentInfo, name='students-update-info'),
    path('staff/update-info/', updateStaffInfo, name='staff-update-info'),
    path('students/dashboard/', dashBoard, name='students-dashboard'),
    path('students/academics/', academics, name='students-academics'),
    path('students/academics/course-registration/', courseRegistration, name='students-academics-course-registration'),
    path('students/academics/registered-courses/', registeredCourses, name='students-academics-registered-courses'),
    path('activate/<str:uidb64>/<str:token>/<int:special>/', accountActivation, name='activate-account'),
    path('account-office/', accountOffice, name='account-office'),
]
