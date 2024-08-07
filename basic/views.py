from typing import Any
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView

from .models import Category, Quiz, Question, Choice, UserAnswer, Score

# Create your views here.
def index(request):
    quizlist = Quiz.objects.order_by('-created_at')[:10]
    return render(request, 'basic/index.html', {
        'list_of_quiz': quizlist
    })


def quizlistview(request):
    pass


# Quiz Detail: Show specific details of a quiz, including questions and options.
def quizdetailview(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    all_questions = quiz.question_set.all()
    num_ques = len(all_questions)
    return render(request, 'basic/quiz_detail.html', {
        'quiz': quiz,
        'num_ques': num_ques,
    })


# Take Quiz: Allow users to attempt a quiz and submit answers.
def takequizview(request, quiz_id):
    if request.method == 'GET':
        # load the quiz if it exists
        quiz = get_object_or_404(Quiz, pk=quiz_id)

        # Prepare quiz and question data for JSON serialization
        quiz_data = {
            'id': quiz.id,
            'title': quiz.title,
            # Add other quiz fields as needed
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
# User Profile: Show a user's quiz history and scores.