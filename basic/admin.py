from django.contrib import admin
from .models import Category, Quiz, Question, Choice, UserAnswer

# Register your models here.
admin.site.register(Category)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserAnswer)