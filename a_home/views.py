from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from a_home.models import Question,MBTIResponse,MBTIResult
from django.contrib.auth.models import User
from django.utils import timezone
import json
from django.utils.dateparse import parse_datetime
from django.db.models import QuerySet
from django.core.paginator import Paginator
from itertools import chain
import random


def get_random_questions(mbtidic_value: str, get_number: int) -> QuerySet:
    return Question.objects.filter(is_active=True, mbtidic=mbtidic_value).order_by('?')[:get_number]

# Fetching 5 random questions for each MBTI dimension




# @login_required
def home(request):
    return render(request, "a_home/index.html")

@login_required
def survey(request):
    # print(request.user.id)
    # request.session['user_id'] = request.user.id
    return render(request, 'a_home/survey.html')

@login_required
def surveyview(request, num_question):
    random_questions_EI = get_random_questions("EI", num_question)
    random_questions_SN = get_random_questions("SN", num_question)
    random_questions_TF = get_random_questions("TF", num_question)
    random_questions_JP = get_random_questions("JP", num_question)
    combined_questions = list(chain(random_questions_EI, random_questions_SN, random_questions_TF, random_questions_JP))    
    random.shuffle(combined_questions)

    paginator = Paginator(combined_questions, 1)
    page_number = request.GET.get('page', 1)
    print(page_number)
    
    page_obj = paginator.get_page(page_number)
    print(page_obj)

    if request.method == 'POST':
        current_page_number = request.POST.get('page', page_number)

        question_id = request.POST.get('question_id')
        current_question = Question.objects.get(id=question_id)
        print(current_question.mbtidic)
        response = request.POST.get('response')
        MBTIResponse.objects.create(question=current_question)
        # Answer.objects.create(survey=survey, question=current_question, chosen_answer=response)

        # Attempt to go to the next page
        page_obj = paginator.get_page(current_page_number)
        print(page_obj)
        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()
            return HttpResponseRedirect(f'?page={next_page_number}')
        else:
            del request.session['survey_id']
            return redirect('survey_complete')

    else:
        page_obj = paginator.get_page(page_number)

    return render(request, 'a_home/surveyview.html', {'page_obj': page_obj, 'num_question': num_question})
