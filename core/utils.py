# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt

#Password validator
#--Rules
# length 8 or more
# Can't contain any personla info
# Must be alphanumeric(Uppera case, Number and a symbol)


from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.crypto import constant_time_compare
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.utils.http import base36_to_int
from django.core.mail import EmailMessage
import re, string, random, datetime
from django.utils import timezone
from django.conf import settings
from pathlib import Path
from .models import *
import openpyxl
import os

BASE_DIR = Path(__file__).resolve().parent.parent
accessDuration= settings.ACCESS_TOKEN_DURATION
refreshDuration= settings.REFRESH_TOKEN_DURATION
bearerAuth= settings.BEARER_KEY


def is_strong_password(password, username, email, firstname= None, lastname= None):
    #Checking password length
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long.'
    else:
        personal_info= [username, firstname, lastname, email]
        for info in personal_info:
            if info and info.lower() in password.lower():
                return False, 'Password must not contain personal information.'
        #Checking for personal info
        if firstname is None and lastname is None:
                if re.search(f'(?=.*{username})(?=.*{email})', password):
                    return False, 'Password must not contain personal information.'
                else:
                    #Checking for alphanumeric and symbol
                    if re.search('^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
                        return True, 'Strong password.'
                    else:
                        return False, 'Password must contain at least one uppercase letter, one number, and one of these special characters. @$!%*?&'
        else:
            if re.search(f'(?=.*{username})(?=.*{firstname})(?=.*{lastname})(?=.*{email})', password):
                return False, 'Password must not contain personal information.'
            else:
                #Checking for alphanumeric and symbol
                if re.search('^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
                    return True, 'Strong password.'
                else:
                    return False, 'Password must contain at least one uppercase letter, one number, and one of these special characters. @$!%*?&'


def headersAuthorizationCheck(header):
    headers_access_token= header

    if headers_access_token and headers_access_token != 'null': # Checking if headaersAccessToken is not None or not == null
        authSplit= headers_access_token.split(' ')
        if authSplit[0] == bearerAuth: 
            try:
                token= StudentsTokenStorage.objects.get(accessToken= authSplit[1])
                isActive= check_token(token.dateCreated, accessDuration)
                if isActive:
                    return {"message": "Approved","code": 200, "user": token.user, "status": True}
                else:
                    return {'message': 'Access token has expired use your refresh token to generate new tokens and try again.', "code": 401, "status": False}
                
            except StudentsTokenStorage.DoesNotExist:
                try:
                    token= TokenStorage.objects.get(accessToken= authSplit[1])
                    isActive= check_token(token.dateCreated, accessDuration)
                    if isActive:
                        return {"message": "Approved","code": 200, "user": token.user, "status": True}
                    else:
                        return {'message': 'Access token has expired use your refresh token to generate new tokens and try again.', "code": 401, "status": False}   
                except TokenStorage.DoesNotExist:
                    # If token doesn't exist in both storage
                    if authSplit[1] == 'null':
                        return {"message": "Access token doesn't exist.","code": 400, "status": False}
                    else:
                        # If token doesn't exist in both storage and is not null
                        return {"message": "Access token doesn't exist.","code": 400, "status": False}
        else:
            return {"message": f"The authorization scheme used is incorrect. Please use '{bearerAuth} <token>' as the format for the Authorization header.", "code": 401, "status": False}
    return {'message': 'Access token is required.', "code": 401, "status": False}


def check_token(dateCreated, duration):
        # Checking if tokens is still valid
        expiration_time= timezone.now() - timezone.timedelta(minutes= int(duration))
        if dateCreated > expiration_time:
            return True
        else:
            return False


def generate_token(user):
    # Generating new access and refresh tokens
    access = AccessToken.for_user(user)
    refresh = RefreshToken.for_user(user)

    return {'access': str(access), 'refresh': str(refresh)}


def getActivationLink(request, user, special= False):
    if special:
        adminRequest= 1
    else:
        adminRequest= 0
    try:
        current_site= get_current_site(request) #Geting the curent site domain
        token= ActivationValidator.make_token(user) #Generating hash 
        tokenID= ActivationTokensModel.objects.create(token=token, user_id=user.id) # Registering token to database
        tokenID.save()
        mail_subject= 'Account Activation' #Email to be sent preparation process
        message= render_to_string('mail/accountactivation.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
            'special': adminRequest,
        })
        email= EmailMessage(
            mail_subject, message, to=[user.email]
        )
        email.content_subtype = 'html'
        email.send()
        return True
    except:
        return False



def activateAccount(uidb64, token, special): 
    # user= auth.get_user_model()
    try: # Decoding the hashes recieved from the link to verify if it a valid link to activate their account

        uid= force_str(urlsafe_base64_decode(uidb64))
        if int(special) == 1:
            user= StaffUserModel.objects.get(pk= uid)
        else:
            user= StudentstsModel.objects.get(pk= uid)
    except (TypeError, ValidationError, OverflowError, StaffUserModel.DoesNotExist, StudentstsModel.DoesNotExist):
        user= None

    if user is not None and ActivationValidator.check_activation_token(user, token, settings.ACCOUNT_ACTIVATION_TOKEN_EXPIRY_DURATION): # checking the validity of the token
        user.is_active= True
        user.save()
        ActivationTokensModel.objects.get(token= token).delete()
        # auth.login(request, user)
        return True, user.email , "Account activation successfully"
    else:
        return False, None, "Account activation failed"


class ActivationValidator(PasswordResetTokenGenerator):
     
    def _num_to_timestamp(self, num):
        """
        Converts a base36 encoded number to a timestamp.
        """
        try:
            return int(num, 36)
        except ValueError:
            raise ValueError("Invalid base36 encoded timestamp")
        
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.is_active)
        )
    
    def check_activation_token(self, user, token, duration):
        try:
            get_token_from_database= ActivationTokensModel.objects.get(token= token)
            expiration_time= timezone.now() - timezone.timedelta(minutes= int(duration))
            if get_token_from_database is not None and get_token_from_database.user_id == user.id: #checking if token exist and also if token was generated by the current user
                if get_token_from_database.timestamp > expiration_time: #checking if it still valid
                    return True
                else:
                    get_token_from_database.delete() # deleting token if it has expired
                    return False
            else:
                return False
        except (TypeError, ValueError, OverflowError, ActivationTokensModel.DoesNotExist):
            return False
        
   
# Create an instance of the custom token generator Validator
ActivationValidator = ActivationValidator()

def createDebtforStudent(uid):
    try:
        student = StudentstsModel.objects.get(uid=uid)
    except StudentstsModel.DoesNotExist:
        return "Student not found."

    # Get the current settings
    settings = SettingsModel.objects.filter(active=True).first()
    if not settings:
        return "No active settings found."

    # Parse levels and tuitions
    levels = [level.strip() for level in settings.academic_year_levels.split(',')]
    tuitions = [tution.strip() for tution in settings.academic_year_levels_tution.split(',')]

    if len(levels) != len(tuitions):
        return "Levels and tuition counts do not match."

    # Map level name to tuition amount
    level_tuition_map = dict(zip(levels, tuitions))
    
    student_level_name = student.level.name

    print(student_level_name, level_tuition_map, levels, tuitions)
    if student_level_name in level_tuition_map:
        amount = level_tuition_map[student_level_name]
        # Check if debt already exists for this student and academic year
        if not TutionModel.objects.filter(student=student, academicYear=settings.academic_year).exists():
            TutionModel.objects.create(
                student=student,
                academicYear=settings.academic_year,
                amount=amount,
                cleared=False
            )
            return f"Debt created for student {student.surname} {student.othername}."
        else:
            return "Debt already exists for this student."
    else:
        return "Student's level does not match any defined tuition levels."

def createDebtforStudents(settings_id):
    try:
        settings = SettingsModel.objects.get(settings_id=settings_id)
    except SettingsModel.DoesNotExist:
        return "Settings not found."

    # Parse levels and tuitions
    levels = [level.strip() for level in settings.academic_year_levels.split(',')]
    tuitions = [tution.strip() for tution in settings.academic_year_levels_tution.split(',')]

    if len(levels) != len(tuitions):
        return "Levels and tuition counts do not match."

    # Map level name to tuition amount
    level_tuition_map = dict(zip(levels, tuitions))
    print(level_tuition_map)

    students = StudentstsModel.objects.all()
    created_count = 0
    if not students:
        return "No students found."
    else:
        for student in students:
            student_level_name = student.level.name
            if student_level_name in level_tuition_map:
                amount = level_tuition_map[student_level_name]
                # Check if debt already exists for this student and academic year
                if not TutionModel.objects.filter(student=student, academicYear=settings.academic_year).exists():
                    TutionModel.objects.create(
                        student=student,
                        academicYear=settings.academic_year,
                        amount=amount,
                        cleared=False
                    )
                    created_count += 1

        return f"Debt created for {created_count} students."


def exceldatafetch():
    DataFile = openpyxl.load_workbook(filename=os.path.join(BASE_DIR, 'graduants.xlsx'))
    sheet_students = DataFile['STUDENTS']
    sheet_qualified = DataFile['QUALIFIED']

    # Remove leading/trailing spaces from names in QUALIFIED
    qualified_names = [cell.value.strip() for cell in sheet_qualified['A'] if cell.value]

    # Build a mapping of name -> index from STUDENTS sheet (also strip names)
    student_map = {}
    for idx_cell, name_cell in zip(sheet_students['A'], sheet_students['B']):
        if name_cell.value and idx_cell.value:
            student_map[name_cell.value.strip()] = idx_cell.value

    # For each qualified name, get index number if exists
    qualified_indexes = []
    matched= 0
    unmatched= 0
    total= 0
    for name in qualified_names:
        index = student_map.get(name)
        if index:
            qualified_indexes.append(index)
            matched += 1
            QualifiedStudents.objects.create(indexNumber= index).save()
        else:
            unmatched += 1
            print(f"Name not found: {name}")
        total += 1
    print(f'um: {unmatched}/n m: {matched} /n t:{total}')

    return qualified_indexes
            
# def exceldatafetch():
#     DataFile = openpyxl.load_workbook(filename=os.path.join(BASE_DIR, 'graduants.xlsx'))
#     sheet_students = DataFile['STUDENTS']
#     sheet_qualified = DataFile['QUALIFIED']

#     # Get all names from QUALIFIED sheet (column A)
#     qualified_names = [cell.value for cell in sheet_qualified['A'] if cell.value]

#     # Build a mapping of name -> index from STUDENTS sheet
#     student_map = {}
#     for idx_cell, name_cell in zip(sheet_students['A'], sheet_students['B']):
#         if name_cell.value and idx_cell.value:
#             student_map[name_cell.value] = idx_cell.value

#     # For each qualified name, get index number if exists
#     qualified_indexes = []
#     for name in qualified_names:
#         index = student_map.get(name)
#         if index:
#             qualified_indexes.append(index)
#             print(index)  # Print index number for matched name
#         else:
#             print(f"Name not found: {name}")

#     print(qualified_indexes)
            


