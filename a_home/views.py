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
    user = User.objects.get(username=request.user)
    if MBTIResult.objects.filter(user=user, type_code="MBTI").exists():
        MBTIResult.objects.filter(user=user).delete()
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
    
    
    page_obj = paginator.get_page(page_number)
    
    if request.method == 'POST':
        current_page_number = request.POST.get('page', page_number)
        user = User.objects.get(username=request.user)  
        mbti_result, created = MBTIResult.objects.get_or_create(
            user=user, 
            type_code="MBTI"
        )
        print(mbti_result, created)
        question_id = request.POST.get('question_id')
        current_question = Question.objects.get(id=question_id)
        
        response = request.POST.get('response')
        MBTIResponse.objects.create(question=current_question, mbtiresult=mbti_result , answer=response)
        # Answer.objects.create(survey=survey, question=current_question, chosen_answer=response)

        # Attempt to go to the next page
        page_obj = paginator.get_page(current_page_number)
        
        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()
            return HttpResponseRedirect(f'?page={next_page_number}')
        else:
            return redirect('before_results')

    else:
        page_obj = paginator.get_page(page_number)

    return render(request, 'a_home/surveyview.html', {'page_obj': page_obj, 'num_question': num_question})



@login_required
def before_results(request):
    user = request.user
    user = User.objects.get(username=request.user)
    results = MBTIResult.objects.filter(user=user, type_code="MBTI")
    
    mbti_summary = {}

    for result in results:
        # Get all responses related to the result
        responses = MBTIResponse.objects.filter(mbtiresult=result)
        
        # Initialize counts for each MBTI dimension
        dimension_count = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}

        # Count each type of response
        for response in responses:
            if response.answer in dimension_count:
                dimension_count[response.answer] += 1
        
        # Calculate dominant type for each dimension
        ei = 'E' if dimension_count['E'] >= dimension_count['I'] else 'I'
        sn = 'S' if dimension_count['S'] >= dimension_count['N'] else 'N'
        tf = 'T' if dimension_count['T'] >= dimension_count['F'] else 'F'
        jp = 'J' if dimension_count['J'] >= dimension_count['P'] else 'P'

        # Combine into a full MBTI type
        full_mbti_type = ei + sn + tf + jp
        
        # Store the results in the summary dict using the result ID as key
        mbti_summary[result.id] = {
            'MBTI': full_mbti_type,
            'detail': dimension_count
        }

    # MBTIResult.objects.update(user=user, type_code=full_mbti_type)

    return render(request, "a_home/before_results.html", {'mbti_summary': mbti_summary})




import plotly.express as px
import plotly.io as pio
from collections import Counter

@login_required
def profile_results_view(request):
    # Fetch all MBTI results
    results = MBTIResult.objects.all()

    # Count occurrences of each type_code
    type_counts = Counter(result.type_code for result in results)

    # Data for the pie chart
    labels = list(type_counts.keys())
    values = list(type_counts.values())

    # Create a pie chart
    fig = px.pie(names=labels, values=values, title="Distribution of MBTI Types")


 
    # Convert the figure to html
    graphJSON = pio.to_html(fig, full_html=False)

    return render(request, "a_home/result.html", {'graphJSON': graphJSON})