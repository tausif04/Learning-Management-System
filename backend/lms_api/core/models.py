from django.conf import settings
from django.db import models

class Course(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    instructor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='courses_taught')
    thumbnail=models.URLField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class Module(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='modules')
    title=models.CharField(max_length=200)
    order=models.PositiveIntegerField(default=0)
    class Meta: ordering=['order','id']

class Lesson(models.Model):
    module=models.ForeignKey(Module,on_delete=models.CASCADE,related_name='lessons')
    title=models.CharField(max_length=200)
    content=models.TextField(blank=True)
    video_url=models.URLField(blank=True)
    order=models.PositiveIntegerField(default=0)
    class Meta: ordering=['order','id']

class Enrollment(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='enrollments')
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='enrollments')
    enrolled_at=models.DateTimeField(auto_now_add=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['user','course'],name='unique_enrollment')]

class LessonProgress(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='lesson_progress')
    lesson=models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name='progress_records')
    completed=models.BooleanField(default=False)
    completed_at=models.DateTimeField(null=True,blank=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['user','lesson'],name='unique_lesson_progress')]
