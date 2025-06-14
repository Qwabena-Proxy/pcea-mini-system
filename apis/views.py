# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_str
# from django.template.loader import render_to_string
# from django.core.exceptions import ValidationError
# from django.shortcuts import render, redirect
# from django.core.mail import EmailMessage
from django.core.files import File
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
import openpyxl.workbook
import openpyxl

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
        email = request.data.get("email")
        createResponse, createResponseMessage, staffEmail = createStaffUser(request, email)
        if createResponse:
            return Response(data={'message': createResponseMessage}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'message': createResponseMessage}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
class createStudentView(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        createResponse, createResponseMessage, studentEmail = createNewStudents(request, email)
        if createResponse:
            return Response(data={'message': createResponseMessage}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'message': createResponseMessage}, status=status.HTTP_406_NOT_ACCEPTABLE)

class createBulkStudentsView(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        
        DataFile = openpyxl.load_workbook(filename=file, read_only=True)
        # print(DataFile.get_sheet_names())
        # Assuming the first sheet contains the data
        sheet = DataFile.active
        # Read the first column of the sheet
        emails = []
        for row in sheet.iter_rows(min_row=2, max_col=1, values_only=True):  # Skip header row
            email = row[0]
            if email:
                emails.append(email.strip())
        if not emails:
            return Response({"error": "No valid emails found in the file."}, status=status.HTTP_400_BAD_REQUEST)
        # check for duplicates
        emails = list(set(emails))

        created = 0
        existedUsers = 0
        failedAccSend = []
        for email in emails:
            # logic to create account and send activation link
            createResponse, createResponseMessage, studentEmail = createNewStudents(request, email)
            if not createResponse:
                if "user exist" in createResponseMessage:
                    existedUsers += 1
                    continue
                elif "failed to send activation link" in createResponseMessage:
                    failedAccSend.append(email)
                    continue
            if createResponse:
                created += 1
            # Optionally, handle/report failures

        return Response({"message": f"Processed {created} emails. Already Exist Account {existedUsers}. FailedAccsend {len(failedAccSend)}", "FailedAccSend": failedAccSend}, status=status.HTTP_200_OK)
    
    # def post(self, request, *args, **kwargs):
    #     file = request.FILES.get("file")
    #     if not file:
    #         return Response(data={'message': "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
    #     try:
    #         # Assuming the file is a CSV
    #         df = pd.read_csv(file)
    #         for index, row in df.iterrows():
    #             email = row.get("email")
    #             if email:
    #                 createResponse, createResponseMessage = createNewStudents(request, email)
    #                 if not createResponse:
    #                     return Response(data={'message': createResponseMessage}, status=status.HTTP_406_NOT_ACCEPTABLE)
    #         return Response(data={'message': "Bulk student creation successful"}, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response(data={'message': f"Error processing file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
class createStudentPasswordView(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            student = StudentstsModel.objects.get(email=email)
            student.set_password(password)
            student.save()
            return Response(data={'message': "Success"}, status=status.HTTP_201_CREATED)
        except:
            return Response(data={'message': "Fail"}, status=status.HTTP_406_NOT_ACCEPTABLE)

class createStaffPasswordView(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            staff = StaffUserModel.objects.get(email=email)
            staff.set_password(password)
            staff.save()
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
        studentProgramLevel= request.data.get("studentProgramLevel")
        studentLevel= request.data.get("studentLevel")
        studentID= request.data.get("studentID")

        print(studentID)
        try:
            student= StudentstsModel.objects.get(uid= studentID)
            student.surname= studentSurname
            student.othername= otherName
            student.indexNumber= indexNumber
            student.program= ProgrameModel.objects.get(name= studentProgram)
            # student.minor_program= ProgrameModel.objects.get(name= "None")
            student.level= LevelModel.objects.get(name= studentLevel)
            if studentProgramLevel == "Primmary":
                student.isProgramJHS= False
            student.save()
            debtResponse= createDebtforStudent(student.uid)
            print(debtResponse)
            # If the student has a profile image, save it
            # if 'profileImg' in request.FILES:
            #     profileImg = request.FILES['profileImg']
            #     student.profile_img.save(f"{student.uid}_profile.jpg", File(profileImg))
            # else:
            #     student.profile_img = None
            # student.save()
            # # If the student has a telephone number, save it  
            # if studentTelephone:
            #     student.telephone = studentTelephone
            # else:
            #     student.telephone = None
            # student.save()

            return Response(data= {"message": f"Dear {studentSurname} {otherName}, your information has been recorded successfully."}, status=status.HTTP_200_OK)
        except StudentstsModel.DoesNotExist:
            return Response(data= {"message": "Student does not exist"}, status=status.HTTP_400_BAD_REQUEST)


class GetStudentsPrograms(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        headers= request.headers.get('Authorization')
        headerCheck= headersAuthorizationCheck(headers)
        if headerCheck['status']:
            userID= headerCheck['user']
            # Get active settings
            try:
                activeSettings= SettingsModel.objects.get(active= True)
            except SettingsModel.DoesNotExist:
                return Response(data={'message': "No active settings found"}, status=status.HTTP_400_BAD_REQUEST)
            # Check if student is debt cleared
            try:
                debtCheck= TutionModel.objects.get(student= userID, academicYear= activeSettings.academic_year)
                if not debtCheck.cleared:
                    return Response(data={'message': "You have an outstanding debt, please vist the account office to clear it before registering for courses"}, status=status.HTTP_400_BAD_REQUEST)
            except TutionModel.DoesNotExist:
                return Response(data={'message': "You have not paid your tuition fees for this academic year"}, status=status.HTTP_400_BAD_REQUEST)
            
            majorCourses = courseModel.objects.filter(program= ProgrameModel.objects.get(name= userID.program.name) , level= LevelModel.objects.get(name= userID.level), isGeneral= False, semester= activeSettings.current_semester)
            minorCourses = courseModel.objects.filter(program= ProgrameModel.objects.get(name= userID.program.minor), level= LevelModel.objects.get(name= userID.level), isGeneral= False, semester= activeSettings.current_semester)
            generalCourses = courseModel.objects.filter(isGeneral= True, isJHS= userID.isProgramJHS, semester= activeSettings.current_semester, level= LevelModel.objects.get(name= userID.level))
            # Combine all courses
            allCourses = majorCourses | minorCourses | generalCourses
            allCourses = allCourses.distinct()  # Remove duplicates
            print(majorCourses, minorCourses, generalCourses, allCourses)
            # Prepare the response data
            courseDict= {}
            for index, value in enumerate(allCourses):
                courseDict[index]= {
                    'ID': value.uid,
                    'CT': value.name,
                    'CC': value.code,
                    'CCHR': value.crh,
                }
            return Response(data= courseDict, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': headerCheck['message']}, status=status.HTTP_401_UNAUTHORIZED)


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
            except (StudentsTokenStorage.DoesNotExist):
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
           # Get active settings
            try:
                activeSettings= SettingsModel.objects.get(active= True)
            except SettingsModel.DoesNotExist:
                return Response(data={'message': "No active settings found"}, status=status.HTTP_400_BAD_REQUEST)
            # Check if student is debt cleared
            try:
                debtCheck= TutionModel.objects.get(student= userID, academicYear= activeSettings.academic_year)
                if not debtCheck.cleared:
                    return Response(data={'message': "You have an outstanding debt, please visit the account office to clear it before registering for courses"}, status=status.HTTP_400_BAD_REQUEST)
            except TutionModel.DoesNotExist:
                return Response(data={'message': "You have not paid your tuition fees for this academic year"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                student= StudentstsModel.objects.get(uid= userID.uid)
                infoDict= {
                    'indexNumber': student.indexNumber,
                    'fullName': f'{student.surname} {student.othername}',
                    'program': f'{student.program}',
                    'level': f'{student.level}',
                    'current_semester': f'{activeSettings.current_semester}',
                    'pogram_level': f'{student.isProgramJHS}',
                }
            except StaffUserModel.DoesNotExist:
                return Response(data={'message': headerCheck['message'], 'data': 'User Does not Exist'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={'message': headerCheck['message'], 'data': infoDict} , status=status.HTTP_200_OK)
        else:
            return Response(data={'message': headerCheck['message'], 'data': ''}, status=status.HTTP_400_BAD_REQUEST)

class StudentInfoView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        headers= request.headers.get('Authorization')
        headerCheck= headersAuthorizationCheck(headers)
        if headerCheck['status']:
            userID= headerCheck['user']
            infoDict= {}
            try:
                student= StudentstsModel.objects.get(uid= userID.uid)
                infoDict= {
                    'fullName': f'{student.surname} {student.othername}',
                    'program': f'{student.program}',
                    'pogram_level': f'{student.isProgramJHS}',
                }
            except StaffUserModel.DoesNotExist:
                return Response(data={'message': headerCheck['message'], 'data': 'User Does not Exist'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={'message': headerCheck['message'], 'data': infoDict} , status=status.HTTP_200_OK)
        else:
            return Response(data={'message': headerCheck['message'], 'data': ''}, status=status.HTTP_400_BAD_REQUEST)

class LevelCreateView(generics.GenericAPIView):
    serializer_class = LevelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            level = serializer.save()
            return Response(data={'message': f"Level {level.name} created successfully"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(data={'message': "Level already exists"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        uid = request.data.get('uid')
        if not uid:
            return Response(data={'message': "UID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            level = LevelModel.objects.get(uid=uid)
        except LevelModel.DoesNotExist:
            return Response(data={'message': "Level not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(level, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'message': f"Level {level.name} updated successfully"}, status=status.HTTP_200_OK)

class ProgramCreateView(generics.GenericAPIView):
    serializer_class = ProgramlSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            program = serializer.save()
            return Response(data={'message': f"Program {program.name} created successfully"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(data={'message': "Program already exists"}, status=status.HTTP_400_BAD_REQUEST)


class DepartmentCreateView(generics.GenericAPIView):
    serializer_class = DepartmentSerializer
    def get(self, request, *args, **kwargs):
        departments = DepartmentModel.objects.all()
        serializer = self.get_serializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            department = serializer.save()
            return Response(data={'message': f"Department {department.name} created successfully"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(data={'message': "Department already exists"}, status=status.HTTP_400_BAD_REQUEST)

class CourseCreateView(generics.GenericAPIView):
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        courses = courseModel.objects.all()
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            course = serializer.save()
            return Response(
                data={'message': f"Course {course.name} created successfully"},
                status=status.HTTP_201_CREATED
            )
        except IntegrityError:
            return Response(
                data={'message': "Course already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

class SettingsView(generics.GenericAPIView):
    serializer_class = SettingsSerializer

    # def get(self, request, *args, **kwargs):
    #     settings = SettingsModel.objects.all()
    #     serializer = self.get_serializer(settings, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        settings = SettingsModel.objects.filter(active=True)
        serializer = self.get_serializer(settings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        for x in SettingsModel.objects.all():
            x.active= False
            x.save()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        settings = serializer.save()
        debtResponse= createDebtforStudents(SettingsModel.objects.filter(active= True)[0].settings_id)
        print(debtResponse)
        return Response({'message': f"Settings for {settings.academic_year} created."}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        settings_id = request.data.get("settings_id")
        current_semester = request.data.get("current_semester")

        if not settings_id or not current_semester:
            return Response({"message": "Missing settings_id or current_semester."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            settings = SettingsModel.objects.get(settings_id=settings_id)
        except SettingsModel.DoesNotExist:
            return Response({"message": "Settings not found."}, status=status.HTTP_404_NOT_FOUND)
        settings.current_semester = current_semester
        settings.save()
        serializer = self.get_serializer(settings)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TokenRegeneration(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        refreshToken= request.data.get("refToken")
        try:
            userTokenObject= StudentsTokenStorage.objects.get(refToken= refreshToken)
            user= userTokenObject.user
            checkTokenValidity= check_token(userTokenObject.dateCreated, refreshDuration)
            if checkTokenValidity:
                generateToken= generate_token(userTokenObject.user)
                response_data = {
                    'access': generateToken['access'],
                    'refresh': generateToken['refresh'],
                    'studentID': user.uid,
                }
                #Storing of tokens
                try:
                    StudentsTokenStorage.objects.get(user= user).delete()
                except StudentsTokenStorage.DoesNotExist:
                    pass
                StudentsTokenStorage.objects.create(user= user, accessToken= generateToken['access'], refToken= generateToken['refresh']).save()
                return Response({'message': f"Token generation successful.", 'token': response_data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': f"Token generation failed."}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': f"Token generation failed."}, status=status.HTTP_400_BAD_REQUEST)

class getUpdateM(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        levels= []
        for level in LevelModel.objects.all():
            levels.append(level.name)
        programs= []
        for program in ProgrameModel.objects.all():
            programs.append(program.name)
        course= []
        for cous in courseModel.objects.all():
            course.append(cous.name)
        return Response(data={'level': levels, 'program': programs, 'course': course}, status=status.HTTP_200_OK)

'''
user must reset default password, resetlink must be send to their email

'''