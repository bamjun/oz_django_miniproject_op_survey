from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Question, Quiz
from django.contrib.auth.models import User
from django.utils import timezone
import json
from django.utils.dateparse import parse_datetime

# @login_required
def home(request):
    return render(request, "a_home/index.html")


# @login_required
# def home1(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         age = request.POST.get("age")
#         gender = request.POST.get("gender")

#         # Check if the participant exists and update or create accordingly
#         participant, created = User.objects.update_or_create(
#             user=request.user,  # Check for existing participant of this user
#             defaults={
#                 'name': name,
#                 'age': int(age),  # Ensure age is an integer
#                 'gender': gender
#             }
#         )
        
#         # Redirect to the home page which will now display the edit page
#         return redirect('home')
    

    
    # # Check if a Participant instance exists for the user
    # try:
    #     participant = Participant.objects.get(user=request.user)
    #     # Participant exists, show the edit page
    #     return render(request, "a_home/edit_index.html", {"participant": participant})
    # except Participant.DoesNotExist:
    #     # No Participant exists, show the registration page
    #     return render(request, "a_home/index.html")



# def home(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         age = request.POST.get("age")
#         gender = request.POST.get("gender")

#         # Create new Participant object and save it
#         new_participant = Participant(
#             user=request.user,
#             name=name,
#             age=int(age),  # Ensure age is an integer
#             gender=gender,
#         )
#         new_participant.save()
        
#         # Redirect to the same page after saving the participant
#         return redirect('home')
    
#     try:
#         participant = Participant.objects.get(user=request.user)
#         # Redirect to edit page if participant exists
#         return render(request, "a_home/edit_index.html", {"participant": participant})
#     except Participant.DoesNotExist:
#         # Render the normal index page if no participant exists
#         return render(request, "a_home/index.html")


    



# def home_view(request):
#     return render(request, 'home.html')

# def home(request):
#     return render(request, "a_home/index.html")

# @require_http_methods(["POST"])
# def add_participant(request):
#     data = json.loads(request.body)
#     new_participant = Participant(
#         name=data["name"], age=data["age"], gender=data["gender"], created_at=timezone.now()
#     )
#     new_participant.save()
#     return JsonResponse({
#         "redirect": reverse("quiz"),
#         "participant_id": new_participant.id
#     })

def quiz(request):
    participant_id = request.COOKIES.get("participant_id")
    if not participant_id:
        return redirect("home")
    questions = Question.objects.all()
    questions_list = [question.content for question in questions]
    return render(request, "a_home/quiz.html", {"questions": questions_list})

@require_http_methods(["POST"])
def submit(request):
    participant_id = request.COOKIES.get("participant_id")
    if not participant_id:
        return JsonResponse({"error": "Participant ID not found"}, status=400)

    data = json.loads(request.body)
    quizzes = data.get("quizzes", [])
    for quiz in quizzes:
        question_id = quiz["question_id"]
        chosen_answer = quiz["chosen_answer"]
        new_quiz_entry = Quiz(
            participant_id=participant_id,
            question_id=question_id,
            chosen_answer=chosen_answer,
        )
        new_quiz_entry.save()
    return JsonResponse({
        "message": "Quiz answers submitted successfully.",
        "redirect": reverse("show_results"),
    })

def questions(request):
    questions = Question.objects.filter(is_active=True).order_by('order_num')
    questions_list = [
        {"id": question.id, "content": question.content, "order_num": question.order_num}
        for question in questions
    ]
    return JsonResponse({"questions": questions_list})

def show_results(request):
    # Implementation would depend on further requirements, possibly including data aggregation and plotting
    pass

# Admin-related views can be handled with Django's built-in admin
