from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(ProgrameModel)
admin.site.register(StudentstsModel)
admin.site.register(StudentsTokenStorage)
admin.site.register(StaffUserModel)
admin.site.register(StaffDepartmentModel)
admin.site.register(TokenStorage)
admin.site.register(ActivationTokensModel)
admin.site.register(LevelModel)
admin.site.register(courseModel)
admin.site.register(StudentRegisterCourseModel)
admin.site.register(SettingsModel)
# admin.site.register(CourseUploadModel)