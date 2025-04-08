from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index-page'),
    path('activate/<str:uidb64>/<str:token>/<int:special>/', accountActivation, name='activate-account'),
]
