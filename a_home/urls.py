from django.urls import path
from .views import *

urlpatterns = [
    # path('', home_view, name='home'),
    path('', home, name='home'),
    # path('', add_participant, name='add_participant'),
    # path('quiz', quiz, name='quiz'),
    # path('submit', submit, name='submit'),
    path('questions', questions, name='questions'),
    # path('results', show_results, name='show_results'),
]
