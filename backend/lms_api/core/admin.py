from django.contrib import admin
from .models import UserProfile,Category,Course,Lesson,Material,Enrollment,LessonProgress,Question
admin.site.register([UserProfile,Category,Course,Lesson,Material,Enrollment,LessonProgress,Question])
