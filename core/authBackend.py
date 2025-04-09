from django.contrib.auth.backends import BaseBackend
from .models import StudentstsModel

class StudentsModelBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            participant = StudentstsModel.objects.get(email=email)
            if participant.check_password(password):
                return participant
        except StudentstsModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return StudentstsModel.objects.get(pk=user_id)
        except StudentstsModel.DoesNotExist:
            return None