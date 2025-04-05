# from django.contrib.auth.decorators import login_required
# from adminSystem.models import AdminDeveloperUserModel
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.models import User, auth 
# # from django.shortcuts import get_object_or_404
# from questionSystem.models import QuizHistory
# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from django.contrib import messages
# from paymentSystem.models import *
# from referralSystem.views import *
# from questionSystem.views import *
# from paymentSystem.views import *
# from django.conf import settings
# from django.urls import reverse
# from .tokensGenerator import *
# from pathlib import Path
# from .models import *
# from .forms import *
# from .utils import is_strong_password
# import os

#Password validator
#--Rules
# length 8 or more
# Can't contain any personla info
# Must be alphanumeric(Uppera case, Number and a symbol)


from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import re, string, random, datetime
from django.utils import timezone
from django.conf import settings
from pathlib import Path
from .models import *
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
            

# def generate_unique_participants_code(length=5):
#     """
#     Generates a unique alphanumeric participants code.
#     """
#     characters = string.ascii_letters + string.digits
#     code = ''.join(random.choice(characters) for _ in range(length))

#     # Check if the code already exists in the database
#     while ParticipantCodeModel.objects.filter(code=code).exists():
#         code = ''.join(random.choice(characters) for _ in range(length))

#     return code


def headersAuthorizationCheck(header):
    headers_access_token= header

    if headers_access_token and headers_access_token != 'null': # Checking if headaersAccessToken is not None or not == null
        authSplit= headers_access_token.split(' ')
        if authSplit[0] == bearerAuth:    
            try:
                token= TokenStorage.objects.get(accessToken= authSplit[1])
                isActive= check_token(token.dateCreated, accessDuration)
                if isActive:
                    return {"message": "Approved","code": 200, "user": token.user, "status": True}
                else:
                    return {'message': 'Access token has expired use your refresh token to generate new tokens and try again.', "code": 401, "status": False}
                
            except TokenStorage.DoesNotExist:
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

def getActivationLink(request, user):
    try:
        current_site= get_current_site(request) #Geting the curent site domain
        token= RefreshToken.for_user(user) #Generating hash 
        tokenID= ActivationTokensModel.objects.create(token=token, user_id=user.id) # Registering token to database
        tokenID.save()
        mail_subject= 'Account Activation' #Email to be sent preparation process
        message= render_to_string('mail/accountactivation.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
        })
        email= EmailMessage(
            mail_subject, message, to=[user.email]
        )
        email.content_subtype = 'html'
        email.send()
        return True
    except:
        return False



# def activateAccount(request, uidb64, token): 
#     user= auth.get_user_model()

#     try: # Decoding the hashes recieved from the link to verify if it a valid link to activate their account
#         uid= force_str(urlsafe_base64_decode(uidb64))
#         user= CustomUserModel.objects.get(pk= uid)
#     except (TypeError, ValidationError, OverflowError, CustomUserModel.DoesNotExist):
#         user= None
#     tokenDate= ActivationTokensModel.objects.get(user_id= uid)
#     if user is not None and check_token(tokenDate.timestamp, settings.ACCOUNT_ACTIVATION_TOKEN_EXPIRY_DURATION): # checking the validity of the token
#         user.is_active= True
#         user.save()
#         ActivationTokensModel.objects.get(token= token).delete()
#         return render(request, 'mail/accountActivationSuccess.html', context= {})    
#     else:
#         return render(request, 'mail/accountActivationFailed.html', context= {})


            