from django.urls import path
from . import views

app_name = "basic"
urlpatterns = [
    path('', views.index, name='index'),

    path('<int:quiz_id>/', views.quizdetailview, name='quiz_detail'),

    path('take_quiz/<int:quiz_id>/', views.takequizview, name='take_quiz'),
    path('load_quiz_data/<int:quiz_id>/', views.load_quizdata_json, name='load_quiz_data'),
    path('results/<int:quiz_id>/', views.resultsview, name='results'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
]