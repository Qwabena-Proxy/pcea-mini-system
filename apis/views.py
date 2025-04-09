# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.sites.shortcuts import get_current_site
from django.db.utils import IntegrityError 
# from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_exempt
# from django.template.loader import render_to_string
# from django.core.exceptions import ValidationError
# from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib.auth.models import auth 
from rest_framework import generics, status
# from django.core.mail import EmailMessage
# from django.core.files import File
from django.conf import settings
from .serializers import *
from core.models import *
from core.utils import *
from core.views import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
accessDuration= settings.ACCESS_TOKEN_DURATION
refreshDuration= settings.REFRESH_TOKEN_DURATION
bearerAuth= settings.BEARER_KEY

# Create your views here.

class StaffLoginView(generics.GenericAPIView):
    serializer_class = StaffLoginSerializer

    def post(self, request, *args, **kwargs):
        # Create an instance of the serializer with the request data
        serializer = self.get_serializer(data=request.data)
        
        # Validate the serializer
        serializer.is_valid(raise_exception=True)
        
        # If valid, get the user from the validated data
        user = serializer.validated_data['user']

        # Generate the access and refresh tokens
        generateToken= generate_token(user)
        #Storing of tokens
        try:
            TokenStorage.objects.get(user= user).delete()
        except TokenStorage.DoesNotExist:
            pass
        TokenStorage.objects.create(user= user, accessToken= generateToken['access'], refToken= generateToken['refresh']).save()
        
        # Construct the response data
        response_data = {
            'access': generateToken['access'],
            'refresh': generateToken['refresh'],
            'email': user.email,
        }
        
        # Return a successful response
        return Response(data= response_data, status=status.HTTP_200_OK)

class StudentsLoginView(generics.GenericAPIView):
    serializer_class = StudentsLoginSerializer

    def post(self, request, *args, **kwargs):
        # Create an instance of the serializer with the request data
        serializer = self.get_serializer(data=request.data)
        resetRequired= False
        
        # Validate the serializer
        serializer.is_valid(raise_exception=True)
        
        # If valid, get the user from the validated data
        user = serializer.validated_data['user']

        # Generate the access and refresh tokens
        generateToken= generate_token(user)
        #Storing of tokens
        try:
            ParticipantsTokenStorage.objects.get(user= user).delete()
        except ParticipantsTokenStorage.DoesNotExist:
            pass
        ParticipantsTokenStorage.objects.create(user= user, accessToken= generateToken['access'], refToken= generateToken['refresh']).save()
        
        # Construct the response data
        response_data = {
            'access': generateToken['access'],
            'refresh': generateToken['refresh'],
            'email': user.email,
        }
        
        # Return a successful response
        return Response(data= response_data, status=status.HTTP_200_OK)

class createStaffView(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        first_name= request.POST.get("firstName")
        last_name= request.POST.get("lastName")
        email= request.POST.get("email")
        password= request.POST.get("password")
        profileImg= request.FILES.get("profileImg")
        DepartmentName= request.POST.get("department")
        if profileImg == None:
            profileImg= ''
        createResponse, createResponseMessage= createStaffUser(
            request= request,
            first_name= first_name,
            last_name= last_name,
            password= password,
            email= email,
            profileImg= profileImg,
            staffDepartment= StaffDepartmentModel.objects.get(name= DepartmentName),
            is_staff= True
        )
        if createResponse:
            return Response(data= {'message': createResponseMessage}, status=status.HTTP_201_CREATED)
        else:
            return Response(data= {'message': createResponseMessage}, status=status.HTTP_406_NOT_ACCEPTABLE)
        

class createStudentView(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        createResponse, createResponseMessage = createNewStudents(request, email)
        if createResponse:
            return Response(data={'message': createResponseMessage}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'message': createResponseMessage}, status=status.HTTP_406_NOT_ACCEPTABLE)

class createStudentPasswordView(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            print(email, password)
            student = StudentstsModel.objects.get(email=email)
            student.set_password(password)
            student.save()
            return Response(data={'message': "Success"}, status=status.HTTP_201_CREATED)
        except:
            return Response(data={'message': "Fail"}, status=status.HTTP_406_NOT_ACCEPTABLE)

class logInView(generics.GenericAPIView):
    serializer_class = StudentsLoginSerializer

    def post(self, request, *args, **kwargs):
        # Create an instance of the serializer with the request data
        serializer = self.get_serializer(data=request.data)
        
        # Validate the serializer
        serializer.is_valid(raise_exception=True)
        
        # If valid, get the user from the validated data
        user = serializer.validated_data['user']

        # Generate the access and refresh tokens
        generateToken= generate_token(user)
        #Storing of tokens
        try:
            StudentsTokenStorage.objects.get(user= user).delete()
        except StudentsTokenStorage.DoesNotExist:
            pass
        StudentsTokenStorage.objects.create(user= user, accessToken= generateToken['access'], refToken= generateToken['refresh']).save()
        

        # Checking if the user is required to update their info on first login
        if user.surname == "TestName":
            updateRequired= True
        else:
            updateRequired= False

        # Construct the response data
        response_data = {
            'access': generateToken['access'],
            'refresh': generateToken['refresh'],
            'email': user.email,
            'updateRequired': updateRequired,
            'studentID': user.uid,
        }
        
        # Return a successful response
        return Response(data= response_data, status=status.HTTP_200_OK)


class studentsInfoUpdate(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        studentSurname= request.data.get("studentSurname")
        otherName= request.data.get("otherName")
        indexNumber= request.data.get("indexNumber")
        studentTelephone= request.data.get("studentTelephone")
        studentProgram= request.data.get("studentProgram")
        studentLevel= request.data.get("studentLevel")
        studentEmail= request.data.get("studentEmail")
        try:
            student= StudentstsModel.objects.get(email= studentEmail)
            student.surname= studentSurname
            student.othername= otherName
            student.indexNumber= indexNumber
            student.program= ProgrameModel.objects.get(name= studentProgram)
            student.level= studentLevel
            student.save()

            return Response(data= {"message": f"Dear {studentSurname} {otherName}, your information has been recorded successfully."}, status=status.HTTP_200_OK)
        except StudentstsModel.DoesNotExist:
            return Response(data= {"message": "Student does not exist"}, status=status.HTTP_400_BAD_REQUEST)



# class CreateProgramView(generics.GenericAPIView):
#     serializer_class= ProgramSerializer

#     def get_queryset(self):
#         return ProgramModel.objects.all()

#     def get(self, request, *args, **kwargs):
#         headers= request.headers.get('Authorization')
#         headersCheck= headersAuthorizationCheck(headers)
#         if headersCheck["status"]:
#             programs = self.get_queryset()
                        
#             # Serialize the programs but only include specific fields
#             serializer = self.serializer_class(programs, many=True, fields=('uid', 'name', 'createdBy', 'dateCreated', 'paymentRequired'))  # Specify the fields you want
            
#             # Return the serialized data
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             if headersCheck["code"] == 401:
#                 return Response(data= headersCheck["message"], status=status.HTTP_401_UNAUTHORIZED)
#             else:
#                 return Response(data= headersCheck["message"], status=status.HTTP_404_NOT_FOUND)

#     def post(self, request, *args, **kwargs):
#         # Create an instance of the serializer with the request data
#         headers= request.headers.get('Authorization')
#         headersCheck= headersAuthorizationCheck(headers)
#         if headersCheck["status"]:
#             programName = request.data.get('name')
#             paymentRequired = request.data.get('paymentRequired')


#             if paymentRequired == 'true':
#                 paymentRequired= True
#             elif paymentRequired == 'false':
#                 paymentRequired= False
#             else:
#                 pass

#             try:
#                 newProgram= ProgramModel.objects.create(name= programName, paymentRequired= paymentRequired, createdBy= CustomUserModel.objects.get(username= headersCheck["user"]))
#                 newProgram.save()
#             except IntegrityError:
#                 return Response(data= {"message": "Program Already Exist"}, status=status.HTTP_409_CONFLICT)
            
#             # Construct the response data
#             response_data = {
#                 'message': 'Program Created'
#             }
            
#             # Return a successful response
#             return Response(data= response_data, status=status.HTTP_201_CREATED)
#         else:
#             if headersCheck["code"] == 401:
#                 return Response(data= headersCheck["message"], status=status.HTTP_401_UNAUTHORIZED)
#             else:
#                 return Response(data= headersCheck["message"], status=status.HTTP_404_NOT_FOUND)
            
#     def delete(self, request, *args, **kwargs):
#         headers= request.headers.get('Authorization')
#         headersCheck= headersAuthorizationCheck(headers)
#         if headersCheck["status"]:
#             programUID = request.headers.get('Program')
#             try:
#                 Program= ProgramModel.objects.get(uid= programUID)
#                 canDeleteProgram= programParticipantsDelete(Program.name)
#                 if canDeleteProgram:
#                     Program.delete()
#             except ProgramModel.DoesNotExist:
#                 return Response(data= {"message": "Program Does Not Exist"}, status=status.HTTP_400_BAD_REQUEST)
            
#             # Construct the response data
#             response_data = {
#                 'message': 'Program Deleted'
#             }
            
#             # Return a successful response
#             return Response(data= response_data, status=status.HTTP_202_ACCEPTED)
#         else:
#             if headersCheck["code"] == 401:
#                 return Response(data= headersCheck["message"], status=status.HTTP_401_UNAUTHORIZED)
#             else:
#                 return Response(data= headersCheck["message"], status=status.HTTP_404_NOT_FOUND)


'''
user must reset default password, resetlink must be send to their email

'''