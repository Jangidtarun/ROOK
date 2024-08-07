from django.urls import path
from . import views

app_name = "basic"
urlpatterns = [
    path('', views.index, name='index'),

    path('<int:quiz_id>/', views.quizdetailview, name='quiz_detail'),

    path('take_quiz/<int:quiz_id>/', views.takequizview, name='take_quiz'),
]