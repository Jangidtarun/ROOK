from django.urls import path
from . import views

app_name = "basic"
urlpatterns = [
    path('', views.index, name='index'),

    path('quizzes/', views.QuizListView.as_view(), name='quiz_list'),
    
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz_details'),   ]
