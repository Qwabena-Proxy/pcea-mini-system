from django.contrib.auth import authenticate
from rest_framework import serializers
from core.models import *

# class StaffUserModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= StaffUserModel
#         fields= ('id', 'first_name', 'last_name', 'password', 'email', 'username', 'profile_img')
#         # fields= '__all__'

# #This function helps to specifiy which fields to return in a get request when defining your own get function
#     def __init__(self, *args, **kwargs):
#         fields = kwargs.pop('fields', None)
#         super(StaffUserModelSerializer, self).__init__(*args, **kwargs)

#         if fields is not None:
#             # Drop any fields that are not specified
#             allowed = set(fields)
#             existing = set(self.fields)
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)


class StaffLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('Invalid email or password')
        attrs['user'] = user
        return attrs

class StudentsLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('Invalid email or password')
        attrs['user'] = user
        return attrs

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelModel
        fields = ['uid', 'name']

class ProgramlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrameModel
        fields = ['uid', 'name']

class CourseSerializer(serializers.ModelSerializer):
    # For reading: show the name
    level_name = serializers.CharField(source='level.name', read_only=True)
    program_name = serializers.CharField(source='program.name', read_only=True)
    # For writing: accept the name
    level = serializers.SlugRelatedField(
        queryset=LevelModel.objects.all(),
        slug_field='name', # This is the field used for writing and you can use any field that is unique
        write_only=True
    )
    program = serializers.SlugRelatedField(
        queryset=ProgrameModel.objects.all(),
        slug_field='name',
        write_only=True
    )

    class Meta:
        model = courseModel
        fields = [
            'uid', 'name', 'code', 'crh', 'level', 'program', 'semester',
            'level_name', 'program_name'
        ]