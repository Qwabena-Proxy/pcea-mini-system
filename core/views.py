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
    context= {

    }
    return render(request, 'admin/manager.html', context= context)

def loginView(request):
    context= {

    }
    return render(request, 'general/login.html', context= context)

def updateStudentInfo(request):
    Programs= ProgrameModel.objects.all()
    Levels= LevelModel.objects.all()
    context= {
        'studentsPrograms': Programs,
        'studentsLevels': Levels,
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

def accountActivation(request, uidb64, token, special):
    activationStatus, userEmail, activationMessage= activateAccount(uidb64, token, special)
    context= {
        'email': userEmail,
        'activationMessage': activationMessage
    }
    if activationStatus:
        return render(request, 'students/set-new-password.html', context= context)
    else:
        return render(request, 'students/activationFailed.html', context= context)


def createStaffUser(request, first_name, last_name, password, email, profileImg, staffDepartment, is_staff, hasFullAccess=False):
    if StaffUserModel.objects.filter(email= email).exists():
        return False, 'A user exist with this email'
    else:
        newStaff= StaffUserModel.objects.create(
            first_name= first_name,
            last_name= last_name,
            email= email,
            hasFullAccess= hasFullAccess,
            staffDepartment= staffDepartment,
            is_staff= is_staff,
            profile_img= profileImg
        )
        newStaff.set_password(password)
        newStaff.save()
        linkResponse= getActivationLink(request, newStaff)
        if linkResponse:
            return True, 'User has been created successfully'
        else:
            return False, 'Account has been created but failed to send activation link'
    
def createNewStudents(request, email):

    try:
        testProgram= ProgrameModel.objects.get("TestProgram")
    except ProgrameModel.DoesNotExist:
        ProgrameModel.objects.create("TestProgram").save()

    try:
        testLevel= LevelModel.objects.get("TestLevel")
    except LevelModel.DoesNotExist:
        LevelModel.objects.create("TestLevel").save()

    if StudentstsModel.objects.filter(email= email).exists():
        return False, 'A user exist with this email'
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
        print(linkResponse)
        if linkResponse:
            return True, 'User has been created successfully'
        else:
            return False, 'Account has been created but failed to send activation link'

def sendActivationLink(request, user, userType, special= False):
    if userType == 'student':
        user= StudentstsModel.objects.get(uid= user.uid)
    elif userType == 'staff':
        user= StaffUserModel.objects.get(uid= user.uid)
    else:
        user= None
    if user is not None:
        linkResponse= getActivationLink(request, user, special)
        if linkResponse:
            return True, 'User has been created successfully'
        else:
            return False, 'Account has been created but failed to send activation link'

