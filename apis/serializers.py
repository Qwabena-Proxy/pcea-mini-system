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
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('Invalid username or password')
        attrs['user'] = user
        return attrs

class StudentsLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(name=attrs['username'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('Invalid username or password')
        attrs['user'] = user
        return attrs


# class TokenStorageSerializer(serializers.ModelSerializer):

#     class Meta:
#         model= TokenStorage
#         fields= ('accessToken', 'refToken')

# #This function helps to specifiy which fields to return in a get request when defining your own get function
#     def __init__(self, *args, **kwargs):
#         fields = kwargs.pop('fields', None)
#         super(TokenStorageSerializer, self).__init__(*args, **kwargs)

#         if fields is not None:
#             # Drop any fields that are not specified
#             allowed = set(fields)
#             existing = set(self.fields)
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)

# class ProgramSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= ProgramModel
#         fields= ('uid', 'name', 'createdBy', 'dateCreated', 'paymentRequired')

#     #This function helps to specifiy which fields to return in a get request when defining your own get function
#     def __init__(self, *args, **kwargs):
#         fields = kwargs.pop('fields', None)
#         super(ProgramSerializer, self).__init__(*args, **kwargs)

#         if fields is not None:
#             # Drop any fields that are not specified
#             allowed = set(fields)
#             existing = set(self.fields)
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model= CategoryModel
#         fields= ('uid', 'name', 'program', 'createdBy', 'dateCreated')

#     #This function helps to specifiy which fields to return in a get request when defining your own get function
#     def __init__(self, *args, **kwargs):
#         fields = kwargs.pop('fields', None)
#         super(CategorySerializer, self).__init__(*args, **kwargs)

#         if fields is not None:
#             # Drop any fields that are not specified
#             allowed = set(fields)
#             existing = set(self.fields)
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)

# class ParticipantsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= ParticipantsModel
#         fields= ('uid', 'name', 'email', 'program', 'category', 'numberOfVote', 'voteCode', 'profile_img', 'bio')

#     #This function helps to specifiy which fields to return in a get request when defining your own get function
#     def __init__(self, *args, **kwargs):
#         fields = kwargs.pop('fields', None)
#         super(ParticipantsSerializer, self).__init__(*args, **kwargs)

#         if fields is not None:
#             # Drop any fields that are not specified
#             allowed = set(fields)
#             existing = set(self.fields)
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)