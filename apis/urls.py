from django.urls import path
from .views import *

urlpatterns = [
    path("create-student", createStudentView.as_view(), name='create-student'),
]
