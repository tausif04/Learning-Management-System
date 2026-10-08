from django.contrib import admin
from .models import Course,Module,Lesson,Enrollment,LessonProgress
admin.site.register([Course,Module,Lesson,Enrollment,LessonProgress])
