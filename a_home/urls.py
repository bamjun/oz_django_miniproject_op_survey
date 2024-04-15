from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('survey/', survey, name='survey'),
    path('survey/<int:num_question>/', surveyview, name='surveyview'),
]
