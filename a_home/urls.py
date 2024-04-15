from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('survey/', survey, name='survey'),
    path('survey/<int:num_question>/', surveyview, name='surveyview'),
    path('before-results/', before_results, name='before_results'),
    path('results/', profile_results_view, name='profile-results'),
]
