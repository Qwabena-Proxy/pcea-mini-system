from django.urls import path
from .views import *

urlpatterns = [
    path("create-staff/", createStaffView.as_view(), name='create-staff'),
    path("create-student/", createStudentView.as_view(), name='create-student'),
    path("bulk-account-activation/", createBulkStudentsView.as_view(), name='bulk-account-activation'),
    path("create-student-password/", createStudentPasswordView.as_view(), name='create-student-password'),
    path("create-staff-password/", createStaffPasswordView.as_view(), name='create-staff-password'),
    path("auth/update-student-info/", studentsInfoUpdate.as_view(), name='update-student-info'),
    path("auth/update-staff-info/", staffsInfoUpdate.as_view(), name='update-staff-info'),
    path("auth/login/", logInView.as_view(), name='logIn'),
    path("auth/staff-login/", StaffLoginView.as_view(), name='staff-logIn'),
    path("get-course/", GetStudentsPrograms.as_view(), name='get-course'),
    path("register-course/", RegisterCourse.as_view(), name='register-course'),
    path("student-register-course/", StudentRegisterCourse.as_view(), name='student-register-course'),
    path("token-regenerate/", TokenRegeneration.as_view(), name='token-regenerate'),
    path("student-info/", StudentInfoView.as_view(), name='student-info'),

    #Managers Api
    path("create-department/", DepartmentCreateView.as_view(), name='create-department'),
    path("create-level/", LevelCreateView.as_view(), name='create-level'),
    path("create-program/", ProgramCreateView.as_view(), name='create-program'),
    path("create-course/", CourseCreateView.as_view(), name='create-course'),
    path("create-settigns/", SettingsView.as_view(), name='create-settigns'),
    path("get-update/", getUpdateM.as_view(), name='get-update'),

    # Account department Api
    path("clear-student/", ClearStudentView.as_view(), name='clear-student'),
    path("debt-student/", DebtStudentView.as_view(), name='debt-student'),


]
