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


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentModel
        fields = ['uid', 'name']

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelModel
        fields = ['uid', 'name']

class ProgramlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrameModel
        fields = ['uid', 'name', 'minor']

class CourseSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='level.name', read_only=True)
    program_name = serializers.SerializerMethodField()

    level = serializers.SlugRelatedField(
        queryset=LevelModel.objects.all(),
        slug_field='name',
        write_only=True
    )
    program = serializers.SlugRelatedField(
        queryset=ProgrameModel.objects.all(),
        slug_field='name',
        write_only=True,
        required=False,
        allow_null=True
    )

    isJHS = serializers.BooleanField()


    class Meta:
        model = courseModel
        fields = [
            'uid', 'name', 'code', 'crh', 'level', 'program', 'semester',
            'level_name', 'program_name', 'isGeneral', 'isJHS'
        ]

    def to_internal_value(self, data):
        data = data.copy()
        if 'isJHS' in data:
            val = data['isJHS']
            if isinstance(val, str):
                data['isJHS'] = val.lower() in ('true', '1', 'yes')
        return super().to_internal_value(data)
    
    def get_program_name(self, obj):
        if obj.isGeneral or obj.program is None:
            return "General"
        return obj.program.name

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingsModel
        fields = [
            'settings_id', 'current_semester', 'academic_year', 'academic_year_start',
            'academic_year_end', 'academic_year_levels', 'academic_year_levels_tution',
            'dateCreated', 'active'
        ]