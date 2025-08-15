from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin, 
    BaseUserManager, 
    UserManager,
    Permission,
    Group,
    )
from django.db import models
import uuid

#Account models

class DepartmentModel(models.Model):
    uid= models.CharField(default= uuid.uuid4, blank= False, null= False, unique= True, max_length= 255)
    name= models.CharField(max_length= 255, blank= False, null= False, unique= True)
    dateCreated= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.name

#Custom User Model Manager
class StaffUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        if not password:
            raise ValueError("The given password must be set")
        if not first_name:
            raise ValueError("The given first name must be set")
        if not last_name:
            raise ValueError("The given last name must be set")
        email = self.normalize_email(email)
        # username =
        user = self.model( email=self.normalize_email(email), first_name= first_name, last_name= last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("hasFullAccess", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")


        return self._create_user( email, password, first_name, last_name, **extra_fields)


#Custom User Model for creating accounts
class StaffUserModel(AbstractBaseUser, PermissionsMixin):
    uid= models.CharField(default= uuid.uuid4, blank= False, null= False, unique= True, max_length= 255)
    first_name= models.CharField(max_length= 240)
    last_name= models.CharField(max_length= 240)
    email= models.EmailField(db_index= True, unique= True, max_length= 240)
    profile_img= models.ImageField(upload_to='profile_images/', default='', null= True, blank= True)
    hasFullAccess= models.BooleanField(default= False)
    staffDepartment= models.ForeignKey(DepartmentModel, on_delete=models.SET_NULL, null= True, blank= True, related_name='staff_department')
    is_staff= models.BooleanField(default= False)
    is_active= models.BooleanField(default= False)
    is_superuser= models.BooleanField(default= False)
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

    objects = StaffUserManager()

    USERNAME_FIELD= 'email' # Username field must not be included in the required field
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name= 'Staff User'
        verbose_name_plural= 'Staff Users'

class TokenStorage(models.Model):
    user= models.ForeignKey(StaffUserModel, on_delete= models.CASCADE)
    accessToken= models.CharField(blank= False, null= False, max_length= 240)
    refToken= models.CharField(blank= False, null= False, max_length= 240)
    dateCreated= models.DateTimeField(blank=False, null=False, auto_now= True)

    def __str__(self):
        return f'{self.user} ---> {self.dateCreated}'

    
#Token model
class ActivationTokensModel(models.Model):
    token= models.CharField(blank=False, null=False, max_length= 204)
    timestamp= models.DateTimeField(blank=False, null=False, auto_now_add= True)
    user_id= models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f'{self.user_id} ---> {self.timestamp}'

# Category model   
class ProgrameModel(models.Model):
    uid= models.CharField(default= uuid.uuid4, blank= False, null= False, unique= True, max_length= 255)
    name= models.CharField(max_length= 255, blank= False, null= False, unique= True) 
    minor= models.CharField(max_length= 255, blank= True, null= True) 


    def __str__(self):
        return self.name

class LevelModel(models.Model):
    uid= models.CharField(default= uuid.uuid4, blank= False, null= False, unique= True, max_length= 255)
    name= models.CharField(max_length= 255, blank= False, null= False, unique= True) 

    def __str__(self):
        return self.name
    
class ProgramsLevel(models.Model):
    uid= models.CharField(default= uuid.uuid4, blank= False, null= False, unique= True, max_length= 255)
    name= models.CharField(max_length= 255, blank= False, null= False, unique= True) 

    def __str__(self):
        return self.name

class courseModel(models.Model):
    uid= models.CharField(default= uuid.uuid4, blank= False, null= False, unique= True, max_length= 255)
    name= models.CharField(max_length= 255, blank= False, null= False, unique= True)
    code= models.CharField(max_length= 15, blank= False, null= False, unique= True)
    crh= models.CharField(max_length= 15, blank= False, null= False)
    level= models.ForeignKey(LevelModel, on_delete= models.CASCADE)
    program= models.ForeignKey(ProgrameModel, on_delete= models.CASCADE, null= True, blank= True, related_name='courses')
    isGeneral= models.BooleanField(default= False)
    isJHS= models.BooleanField(default= True)
    semester= models.CharField(max_length= 5, blank= False, null= False)

    def __str__(self):
        return self.name

# Participants model manager
class StudentsModelManager(BaseUserManager):
    def _create_user(self, surname, othername, level , email, program, indexNumber, password, **extra_fields):
        if not surname:
            raise ValueError("The given surname must be set")
        if not email:
            raise ValueError("The given email must be set")
        if not othername:
            raise ValueError("The given othername must be set")
        if not level:
            raise ValueError("The given level must be set")
        if not program:
            raise ValueError("The given program must be set")
        if not indexNumber:
            raise ValueError("The given indexNumber must be set")
        if not password:
            raise ValueError("The given password must be set")
        
        user= self.model(surname= surname, othername= othername, level= level, program= program, indexNumber= indexNumber, **extra_fields)
        user.set_password(password)
        user.save(using= self._db)
        return user
    
    def create_user(self,surname, othername, level , email, program, indexNumber,pasword, **extra_fields):
        extra_fields.setdefault("uid", uuid.uuid4)
        extra_fields.setdefault("is_active", False)

        return self._create_user(surname, othername, level , email, program, indexNumber, pasword, **extra_fields)
# Participants model
class StudentstsModel(AbstractBaseUser, PermissionsMixin):
    uid= models.CharField(default= uuid.uuid4, blank= False, null= False, unique= True, max_length= 255)
    surname= models.CharField(max_length= 255, blank= False, null= False)
    othername= models.CharField(max_length= 255, blank= False, null= False)
    level= models.ForeignKey(LevelModel, on_delete=models.CASCADE)
    email= models.CharField(max_length= 255, blank= False, null= False, unique= True)
    program= models.ForeignKey(ProgrameModel, on_delete=models.CASCADE, related_name='students_major')
    # minor_program= models.ForeignKey(ProgrameModel, on_delete=models.CASCADE, related_name='students_minor')
    isProgramJHS= models.BooleanField(default= True)
    indexNumber= models.CharField(max_length=20, blank= False, null= False, unique=True)
    profile_img= models.ImageField(upload_to='students_images/', default='', null= True, blank= True)
    is_active= models.BooleanField(default= False)

    groups = models.ManyToManyField(Group, related_name='students_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='students_permissions')

    objects = StudentsModelManager()
    USERNAME_FIELD= 'email' # name field must not be included in the required field
    REQUIRED_FIELDS = ['email',]

    class Meta:
        verbose_name= 'Student User'
        verbose_name_plural= 'Student Users'

class StudentsTokenStorage(models.Model):
    user= models.ForeignKey(StudentstsModel, on_delete= models.CASCADE)
    accessToken= models.CharField(blank= False, null= False, max_length= 240)
    refToken= models.CharField(blank= False, null= False, max_length= 240)
    dateCreated= models.DateTimeField(blank=False, null=False, auto_now= True)

    def __str__(self):
        return f'{self.user} ---> {self.dateCreated}'


class StudentRegisterCourseModel(models.Model):
    register_id= models.CharField(default= uuid.uuid4, blank= False, null= False, unique= True, max_length= 255)
    stud_uuid= models.CharField(default= uuid.uuid4, blank= False, null= False, unique= True, max_length= 255)
    courses= models.CharField(blank= False, null= False, unique= True, max_length= 255)
    dateRegistered= models.DateTimeField(blank=False, null=False, auto_now_add= True)
    dateUpdated= models.DateTimeField(blank=False, null=False, auto_now= True)
    program= models.ForeignKey(ProgrameModel, on_delete=models.CASCADE)
    level= models.ForeignKey(LevelModel, on_delete= models.CASCADE)
    semester= models.CharField(max_length= 5, blank= False, null= False)

    def __str__(self):
        return f'{self.register_id}'

class SettingsModel(models.Model):
    settings_id= models.CharField(default= uuid.uuid4, blank= False, null= False, unique= True, max_length= 255)
    current_semester= models.IntegerField(default= 1)
    academic_year= models.CharField(max_length= 20, blank= False, null= False, default='2023/2024')
    academic_year_start= models.DateField(blank= False, null= False, default='2023-08-01')
    academic_year_end= models.DateField(blank= False, null= False, default='2024-07-31')
    academic_year_levels= models.CharField(max_length= 255, blank= False, null= False, default='100,200,300,400')
    academic_year_levels_tution= models.CharField(max_length= 255, blank= False, null= False, default='1000,1200,1500,1800')
    dateCreated= models.DateTimeField(blank=False, null=False, auto_now_add= True)
    active= models.BooleanField(default= False)

    def __str__(self):
        return f'Settings ID: {self.settings_id} ---------> Current semester: {self.current_semester}'


    @classmethod #This helps to access the class objects with needing to use instance
    def get_current_semeter(cls):
        semester, _ = cls.objects.get_or_create(pk= 1)
        return semester.get_current_semeter
    
    @classmethod
    def update_current_semester(cls, new_semester):
        semester, _ = cls.objects.get_or_create(pk= 1)
        semester.current_semester= new_semester
        semester.save()
        return 'Semester has been updated..'
    
class TutionModel(models.Model):
    uid= models.CharField(default= uuid.uuid4, blank= False, null= False, unique= True, max_length= 255)
    student= models.ForeignKey(StudentstsModel, on_delete=models.CASCADE)
    academicYear= models.CharField(max_length= 10, blank= False, null= False)
    amount= models.DecimalField(max_digits= 10, decimal_places= 2, blank=False, null=False)
    cleared= models.BooleanField(default=False)
    dateCreated= models.DateTimeField(blank=False, null=False, auto_now_add=True)

    def __str__(self):
        return f'{self.student.indexNumber} - {self.academicYear} - {self.amount} - {self.cleared}'
    
    
# class CourseUploadModel(models.Model):
#     uid= models.CharField(default= uuid.uuid4, blank= False, null= False, unique= True, max_length= 255)
#     courseTitle= models.CharField(max_length= 255, blank= False, null= False, unique= True)
#     courseCode= models.CharField(max_length= 15, blank= False, null= False, unique= True)
#     crh= models.CharField(max_length= 15, blank= False, null= False)
#     level= models.ForeignKey(LevelModel, on_delete= models.CASCADE)
#     program= models.ForeignKey(ProgrameModel, on_delete= models.CASCADE)
#     semester= models.CharField(max_length= 5, blank= False, null= False)
#     dateUploaded= models.DateTimeField(blank=False, null=False, auto_now_add= True)
#     uploadedBy= models.CharField(max_length= 255, blank= False, null= False, unique= True)


class Graduants(models.Model):
    name= models.CharField(blank= False, null= False, max_length= 255)
    indexNumber= models.CharField(blank= False, null= False, unique= True, max_length= 20)

    def __str__(self):
        return f'{self.name} ---- {self.indexNumber}'

class QualifiedStudents(models.Model):
    indexNumber= models.CharField(blank= False, null= False, unique= True, max_length= 20)

    def __str__(self):
        return f'{self.indexNumber}'
    
class GraduationRegistration(models.Model):
    name= models.CharField(blank= False, null= False, max_length= 255)
    indexNumber= models.CharField(blank= False, null= False, unique= True, max_length= 20)
    program= models.CharField(blank= False, null= False, max_length= 100)
    gpa= models.CharField(blank= False, null= False, max_length= 20)
    gpaClass= models.CharField(blank= False, null= False, max_length= 30)

    def __str__(self):
        return f'{self.name} --- {self.gpaClass}'
