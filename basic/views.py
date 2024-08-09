from typing import Any
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse


from .models import Quiz, Choice, User

# Create your views here.
def index(request):
    quizlist = Quiz.objects.order_by('-created_at')[:10]
    return render(request, 'basic/index.html', {
        'list_of_quiz': quizlist
    })


def quizlistview(request):
    pass


# Quiz Detail: Show specific details of a quiz, including questions and options.
@login_required
def quizdetailview(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    all_questions = quiz.question_set.all()
    num_ques = len(all_questions)
    return render(request, 'basic/quiz_detail.html', {
        'quiz': quiz,
        'num_ques': num_ques,
    })


# Take Quiz: Allow users to attempt a quiz and submit answers.
@login_required
def takequizview(request, quiz_id):
    if request.method == 'GET':
        # load the quiz if it exists
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        questions = quiz.question_set.all()
        return render(request, 'basic/take_quiz.html', {
            'quiz': quiz,
            'questions': questions,
        })

           

def load_quizdata_json(request, quiz_id):
    if request.method == 'GET':
        # load the quiz if it exists
        quiz = get_object_or_404(Quiz, pk=quiz_id)

        # Prepare quiz and question data for JSON serialization
        quiz_data = {
            'id': quiz.id,
            'title': quiz.title,
        }

        questions_data = [
            {
                'id': question.id,
                'text': question.question_text,
                'time_limit': question.time_limit,

                'options': [
                    {'id': option.id, 'text': option.choice_text, 'is_correct': option.is_correct}
                    for option in question.choice_set.all()
                ]
            }
            for question in quiz.question_set.all()
        ]

        return JsonResponse({
            'quiz': quiz_data,
            'questions': questions_data,
        })

# Results: Display quiz results and scores.
def resultsview(request, quiz_id):
    if request.method == 'POST':
  

        score = 0
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        all_questions = quiz.question_set.all()
        num_questions = all_questions.count()

        for question in all_questions:
            selected_choice = request.POST.get(f'option-{question.id}')
            try:
                choice = Choice.objects.get(pk=selected_choice, question=question, is_correct=True)
                if choice:
                    score += 1
            except Choice.DoesNotExist:
                pass

        user = request.user
        user.score += score
        user.attempts += 1
        user.save()
        
        percentage = (score / num_questions) * 100
        context = {
            'score': score,
            'total_questions': num_questions,
            'percentage': percentage
        }
        return render(request, 'basic/results.html', context)
    # else:



def login_view(req):
    if req.method == "POST":

        # Attempt to sign user in
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(req, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(req, user)
            return redirect('index')
        else:
            return render(req, "basic/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(req, "basic/login.html")


def logout_view(req):
    logout(req)
    return HttpResponseRedirect(reverse(login_view))


def register(req):
    if req.method == "POST":
        username = req.POST["username"]

        # Ensure password matches confirmation
        password = req.POST["password"]
        confirmation = req.POST["confirmation"]
        if password != confirmation:
            return render(req, "basic/register.html", {
                "message": "Passwords must match."
            })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username=username, 
                password=password,
            )
            user.save()
        except IntegrityError:
            return render(req, "basic/register.html", {
                "message": "Username already taken."
            })
        login(req, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(req, "basic/register.html")

@login_required
def user_profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'basic/user_profile.html', context)
