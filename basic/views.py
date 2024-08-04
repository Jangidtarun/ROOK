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


# Quiz Listing: Display a list of available quizzes.
class QuizListView(ListView):
    model = Quiz
    ordering = ['-created_at']
    template_name = 'basic/quiz_list.html'
    context_object_name = 'quizzes'


# Quiz Detail: Show specific details of a quiz, including questions and options.
class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'basic/quiz_detail.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.filter(quiz=self.object).order_by('order')
        total_time = sum(question.time_limit for question in questions)

        context['questions'] = []  # Initially empty list
        context['time_limit'] = total_time
        context['instructions'] = self.object.instructions
        context['difficulty_level'] = self.object.difficulty_level
        return context
    
    # def post()

# Take Quiz: Allow users to attempt a quiz and submit answers.
# Results: Display quiz results and scores.
# User Profile: Show a user's quiz history and scores.