from django.conf import settings
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    ROLE_CHOICES=[('student','Student'),('teacher','Teacher')]
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')
    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default='student')
    bio=models.TextField(blank=True)
    avatar_url=models.URLField(blank=True)
    def __str__(self): return f'{self.user.username} profile'

class Category(models.Model):
    name=models.CharField(max_length=120,unique=True)
    def __str__(self): return self.name

class Course(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name='courses')
    instructor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='courses_taught')
    thumbnail=models.URLField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_published=models.BooleanField(default=True)
    def __str__(self): return self.title

class Lesson(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='lessons')
    title=models.CharField(max_length=200)
    content=models.TextField(blank=True)
    video_url=models.URLField(blank=True)
    order=models.PositiveIntegerField(default=0)
    duration_minutes=models.PositiveIntegerField(default=0)
    class Meta: ordering=['order','id']
    def __str__(self): return self.title

class Material(models.Model):
    lesson=models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name='materials')
    title=models.CharField(max_length=200)
    file_url=models.URLField()
    def __str__(self): return self.title

class Enrollment(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='enrollments')
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='enrollments')
    enrolled_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['user','course'],name='unique_user_course')]

class LessonProgress(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='lesson_progress')
    lesson=models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name='progress_records')
    completed=models.BooleanField(default=False)
    completed_at=models.DateTimeField(null=True,blank=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['user','lesson'],name='unique_user_lesson_progress')]

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='questions')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='questions')
    question_text=models.TextField()
    answer_text=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
