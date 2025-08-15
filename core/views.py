from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.contrib.auth.models import User, auth 
# from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from pathlib import Path
from .models import *
from .utils import *

# Create your views here.

def index(request):
    # exceldatafetch()
    context= {

    }
    return render(request, 'admin/manager.html', context= context)

def loginView(request):
    context= {

    }
    return render(request, 'general/login.html', context= context)

def updateStaffInfo(request):
    departments= DepartmentModel.objects.exclude(name="TestDepartment")
    context= {
        'departments': departments,
    }
    return render(request, 'admin/updateInfoStaff.html', context= context)

def updateStudentInfo(request):
    isJhs, created= ProgramsLevel.objects.get_or_create(name= 'J.H.S')
    isPri, created= ProgramsLevel.objects.get_or_create(name= 'Primmary')
    Programs= ProgrameModel.objects.exclude(name="TestProgram")
    Levels= LevelModel.objects.exclude(name="TestLevel")
    programLeves= ProgramsLevel.objects.all()
    context= {
        'studentsPrograms': Programs,
        'studentsLevels': Levels,
        'programLevels': programLeves,
    }
    return render(request, 'students/updateInfo.html', context= context)

def dashBoard(request):
    context= {

    }
    return render(request, 'students/student-dashboard.html', context= context)

def academics(request):
    context= {

    }
    return render(request, 'students/academics.html', context= context)

def courseRegistration(request):
    context= {

    }
    return render(request, 'students/courses-select.html', context= context)

def registeredCourses(request):
    context= {

    }
    return render(request, 'students/registered-courses.html', context= context)


def accountOffice(request):
    Levels= LevelModel.objects.exclude(name="TestLevel")
    deptorsDict = {}
    wdeptosDict = {}

    for level in Levels:
        students_in_level = StudentstsModel.objects.filter(level=level)
        # Get tuitions for these students (optionally filter for uncleared debts)
        tuitions = TutionModel.objects.filter(student__in=students_in_level, cleared=False)
        wTutions = TutionModel.objects.filter(student__in=students_in_level, cleared=True)

        # Collect debtors (e.g., student emails or objects)
        debtors = [t.student for t in tuitions]
        deptorsDict[level.name] = debtors

        wdeptors = [t.student for t in wTutions]
        wdeptosDict[level.name] = wdeptors
    print(deptorsDict, wdeptosDict)
    context= {
        'levels': Levels,
        'deptorsDict': deptorsDict,
        'wdeptosDict': wdeptosDict,
    }
    return render(request, 'admin/account.html', context= context)

def accountActivation(request, uidb64, token, special):
    activationStatus, userEmail, activationMessage= activateAccount(uidb64, token, special)
    context= {
        'email': userEmail,
        'activationMessage': activationMessage
    }
    if activationStatus and special == 0:
        return render(request, 'students/set-new-password.html', context= context)
    elif activationStatus and special == 1:
        return render(request, 'admin/set-new-password-staff.html', context= context)
    else:
        return render(request, 'students/activationFailed.html', context= context)


def createStaffUser(request, email, hasFullAccess=False, is_staff= True, profileImg=None):
    if StaffUserModel.objects.filter(email= email).exists() or StudentstsModel.objects.filter(email= email).exists():
        return False, 'A user exist with this email', email
    else:
        testDepartment, created= DepartmentModel.objects.get_or_create(name= "TestDepartment")
        newStaff= StaffUserModel.objects.create(
            first_name= 'first_name',
            last_name= 'last_name',
            email= email,
            hasFullAccess= hasFullAccess,
            staffDepartment= testDepartment,
            is_staff= is_staff,
            profile_img= profileImg
        )
        newStaff.save()
        linkResponse= getActivationLink(request, newStaff, True)
        if linkResponse:
            return True, 'User has been created successfully', newStaff.email
        else:
            return False, 'Account has been created but failed to send activation link', newStaff.email
    
def createNewStudents(request, email):
    testProgram, created= ProgrameModel.objects.get_or_create(name= "TestProgram")
    testLevel, created= LevelModel.objects.get_or_create(name= "TestLevel")

    if StudentstsModel.objects.filter(email= email).exists() or StaffUserModel.objects.filter(email= email).exists():
        return False, 'A user exist with this email', email
    else:
        newStudents= StudentstsModel.objects.create(
            surname= 'TestName',
            othername= 'TestName',
            level= testLevel,
            email= email,
            program= testProgram,
            indexNumber= f'TestIndexNumber{StudentstsModel.objects.count()+1}',
        )
        newStudents.save()
        linkResponse= getActivationLink(request, newStudents)
        if linkResponse:
            return True, 'User has been created successfully', newStudents.email
        else:
            return False, 'Account has been created but failed to send activation link', newStudents.email

def sendActivationLink(request, email, userType, special= False):
    if userType == 'student':
        user= StudentstsModel.objects.get(email= email)
    elif userType == 'staff':
        user= StaffUserModel.objects.get(email= email)
    else:
        user= None
    if user is not None:
        linkResponse= getActivationLink(request, user, special)
        if linkResponse:
            return True, 'User has been created successfully'
        else:
            return False, 'Account has been created but failed to send activation link'

@csrf_exempt
def graduationRegistration(request):
    if request.method == 'POST':
        indexNumber= request.POST.get('indexNumber')
        try:
            check= GraduationRegistration.objects.get(indexNumber= indexNumber)
            return JsonResponse({'message': f'{check.name} you have already registered', 'code': 400})
        except GraduationRegistration.DoesNotExist:
            try:
                QualifiedStudents.objects.get(indexNumber= indexNumber)
                return JsonResponse({'message': 'Student is qualified', 'code': 200})
            except QualifiedStudents.DoesNotExist:
                try:
                    std= Graduants.objects.get(indexNumber= indexNumber)
                    return JsonResponse({'message': f'{std.name} you do not qualify to register please visit the account office to clear all debts', 'code': 400})
                except Graduants.DoesNotExist:
                    return JsonResponse({'message': 'Student data does not exist, please visit the account office to make corrections', 'code': 400})
    context= {
    }
    return render(request, 'students/graduationRegistration.html', context= context)

@csrf_exempt
def registerGraduant(request):
    if request.method == 'POST':
        name= request.POST.get('name')
        indexNumber= request.POST.get('indexNumber')
        program= request.POST.get('program')
        gpa= request.POST.get('gpa')
        gpaClass= request.POST.get('gpaClass')

        try:
            QualifiedStudents.objects.get(indexNumber= indexNumber)
            try:
                newGraduant= GraduationRegistration.objects.create(
                    name= name,
                    indexNumber= indexNumber,
                    program= program,
                    gpa= gpa,
                    gpaClass= gpaClass
                )
                newGraduant.save()
                return JsonResponse({'message': 'Details saved', 'code': 200})
            except:
                return JsonResponse({'message': 'Something happened...Please try again', 'code': 400})
        except QualifiedStudents.DoesNotExist:
            return JsonResponse({'message': 'Student is not qualified to register', 'code': 400})

