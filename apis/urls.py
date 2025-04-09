from django.urls import path
from .views import *

urlpatterns = [
    path("create-student/", createStudentView.as_view(), name='create-student'),
    path("create-student-password/", createStudentPasswordView.as_view(), name='create-student-password'),
    path("auth/update-student-info/", studentsInfoUpdate.as_view(), name='update-student-info'),
    path("auth/login/", logInView.as_view(), name='logIn'),

]
