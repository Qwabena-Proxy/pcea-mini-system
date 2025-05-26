# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_str
# from django.template.loader import render_to_string
# from django.core.exceptions import ValidationError
# from django.shortcuts import render, redirect
# from django.core.mail import EmailMessage
# from django.core.files import File
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.contrib.auth.models import auth 
from rest_framework import generics, status
from django.db.utils import IntegrityError 
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
            StudentsTokenStorage.objects.get(user= user).delete()
        except StudentsTokenStorage.DoesNotExist:
            pass
        StudentsTokenStorage.objects.create(user= user, accessToken= generateToken['access'], refToken= generateToken['refresh']).save()
        
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
        studentID= request.data.get("studentID")
        print(studentID)
        try:
            student= StudentstsModel.objects.get(uid= studentID)
            student.surname= studentSurname
            student.othername= otherName
            student.indexNumber= indexNumber
            student.program= ProgrameModel.objects.get(name= studentProgram)
            student.level= studentLevel
            student.save()

            return Response(data= {"message": f"Dear {studentSurname} {otherName}, your information has been recorded successfully."}, status=status.HTTP_200_OK)
        except StudentstsModel.DoesNotExist:
            return Response(data= {"message": "Student does not exist"}, status=status.HTTP_400_BAD_REQUEST)


class GetStudentsPrograms(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        headers= request.headers.get('Authorization')
        headerCheck= headersAuthorizationCheck(headers)
        if headerCheck['status']:
            userID= headerCheck['user']
            cousersInfo= courseModel.objects.filter(program= ProgrameModel.objects.get(name= userID.program), level= LevelModel.objects.get(name= userID.level), semester= '2')
            courseDict= {}
            for index, value in enumerate(cousersInfo):
                courseDict[index]= {
                    'ID': value.uid,
                    'CT': value.name,
                    'CC': value.code,
                    'CCHR': value.crh,
                }
            return Response(data= courseDict, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': headerCheck['message']}, status=status.HTTP_400_BAD_REQUEST)


class RegisterCourse(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        headers= request.headers.get('Authorization')
        headerCheck= headersAuthorizationCheck(headers)
        if headerCheck['status']:
            userID= headerCheck['user']
            selectedCourses= str(request.data.get("courses")).split(",")
            selectedCoursesd = [course.strip() for course in selectedCourses]
            joinedCourses = ",".join(selectedCoursesd)
            try:
                registeredCourses = StudentRegisterCourseModel.objects.filter(stud_uuid=userID.uid)
                if registeredCourses.exists():
                    # If the user has already registered for courses, update with the new courses
                    existingCourseRegistration = registeredCourses.first()
                    existingCourseRegistration.courses= joinedCourses
                    existingCourseRegistration.save()
                else:
                    newRegistration= StudentRegisterCourseModel.objects.create(
                        stud_uuid= userID.uid,
                        courses= joinedCourses,
                        program= ProgrameModel.objects.get(name= userID.program),
                        level= LevelModel.objects.get(name= userID.level),
                        semester= SettingsModel.objects.all().first().current_semester,
                    )
                    newRegistration.save()
            except IntegrityError:
                return Response(data={'message': "You have already registered for this course"}, status=status.HTTP_409_CONFLICT)
            return Response(data={'message': headerCheck['message']} , status=status.HTTP_200_OK)
        else:
            return Response(data={'message': headerCheck['message']}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        headers= request.headers.get('Authorization')
        headerCheck= headersAuthorizationCheck(headers)
        if headerCheck['status']:
            userID= headerCheck['user']
            try:
                registeredCourses= StudentRegisterCourseModel.objects.get(stud_uuid=userID.uid)
            except:
                return Response(data={'message': "Something happened this registration doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            registeredCourses= registeredCourses.courses.split(',')
            courseDict= {}
            for index, course in enumerate(registeredCourses):
                courseObj= courseModel.objects.get(uid= course)
                courseDict[index]= {
                    'code': courseObj.code,
                    'title': courseObj.name,
                    'crh': courseObj.crh
                }

            return Response(data={'message': headerCheck['message'], 'data': courseDict} , status=status.HTTP_200_OK)
        else:
            return Response(data={'message': headerCheck['message'], 'data': ''}, status=status.HTTP_400_BAD_REQUEST)


class StudentRegisterCourse(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        headers= request.headers.get('Authorization')
        headerCheck= headersAuthorizationCheck(headers)
        if headerCheck['status']:
            userID= headerCheck['user']
            infoDict= {}
            try:
                student= StudentstsModel.objects.get(uid= userID.uid)
                infoDict= {
                    'indexNumber': student.indexNumber,
                    'fullName': f'{student.surname} {student.othername}',
                    'program': f'{student.program}',
                    'level': f'{student.level}',
                    'current_semester': f'{SettingsModel.objects.all().first().current_semester}'
                }
            except StaffUserModel.DoesNotExist:
                return Response(data={'message': headerCheck['message'], 'data': 'User Does not Exist'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={'message': headerCheck['message'], 'data': infoDict} , status=status.HTTP_200_OK)
        else:
            return Response(data={'message': headerCheck['message'], 'data': ''}, status=status.HTTP_400_BAD_REQUEST)


'''
user must reset default password, resetlink must be send to their email

'''