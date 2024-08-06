from typing import Any
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
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
    return render(request, 'basic/quiz_detail.html', {
        'quiz': quiz
    })



# Take Quiz: Allow users to attempt a quiz and submit answers.
# Results: Display quiz results and scores.
# User Profile: Show a user's quiz history and scores.