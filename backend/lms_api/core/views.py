from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserProfile, Category, Course, Lesson, Material, Enrollment, LessonProgress, Question
from .serializers import UserSerializer, RegisterSerializer, ProfileSerializer, CategorySerializer, CourseSerializer, LessonSerializer, MaterialSerializer, EnrollmentSerializer, QuestionSerializer
User=get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all(); serializer_class=RegisterSerializer; permission_classes=[permissions.AllowAny]
    def create(self,request,*args,**kwargs):
        s=self.get_serializer(data=request.data); s.is_valid(raise_exception=True); u=s.save(); return Response(UserSerializer(u).data,status=status.HTTP_201_CREATED)
class UserAuthView(generics.ListCreateAPIView):
    queryset=User.objects.all()
    def get_permissions(self): return [permissions.AllowAny()] if self.request.method=='POST' else [permissions.IsAuthenticated()]
    def get_serializer_class(self): return RegisterSerializer if self.request.method=='POST' else UserSerializer
    def create(self,request,*args,**kwargs):
        s=self.get_serializer(data=request.data); s.is_valid(raise_exception=True); u=s.save(); return Response(UserSerializer(u).data,status=status.HTTP_201_CREATED)
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    def get_object(self):
        UserProfile.objects.get_or_create(user=self.request.user); return self.request.user
    def post(self,request,*args,**kwargs): return self.update(request,*args,**kwargs)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all().order_by('name'); serializer_class=CategorySerializer
    def get_permissions(self): return [permissions.IsAuthenticated()]
class CourseViewSet(viewsets.ModelViewSet):
    queryset=Course.objects.select_related('instructor','category').prefetch_related('lessons__materials').filter(is_published=True); serializer_class=CourseSerializer
    def perform_create(self,serializer): serializer.save(instructor=self.request.user)
    @action(detail=True,methods=['post'])
    def enroll(self,request,pk=None):
        course=self.get_object(); Enrollment.objects.get_or_create(user=request.user,course=course); return Response({'message':'User enrolled successfully'})
class LessonViewSet(viewsets.ModelViewSet):
    queryset=Lesson.objects.select_related('course').prefetch_related('materials').all(); serializer_class=LessonSerializer
    def get_queryset(self):
        qs=super().get_queryset(); course=self.request.query_params.get('course')
        return qs.filter(course_id=course) if course else qs
class MaterialViewSet(viewsets.ModelViewSet):
    queryset=Material.objects.all(); serializer_class=MaterialSerializer
class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class=EnrollmentSerializer
    def get_queryset(self): return Enrollment.objects.filter(user=self.request.user).select_related('course','course__instructor','course__category').prefetch_related('course__lessons')
    def create(self,request,*args,**kwargs):
        course_id=request.data.get('course');
        if not course_id:return Response({'course':['This field is required.']},status=400)
        e,_=Enrollment.objects.get_or_create(user=request.user,course_id=course_id); return Response(EnrollmentSerializer(e,context={'request':request}).data,status=201)
    @action(detail=False,methods=['post'])
    def enroll(self,request): return self.create(request)
class ProgressView(generics.ListAPIView):
    serializer_class=LessonSerializer
    def get_queryset(self): return Lesson.objects.filter(progress_records__user=self.request.user,progress_records__completed=True).prefetch_related('materials')
class LessonCompleteView(generics.GenericAPIView):
    queryset=Lesson.objects.all(); serializer_class=LessonSerializer
    def post(self,request,pk):
        lesson=self.get_object()
        if not Enrollment.objects.filter(user=request.user,course=lesson.course).exists(): return Response({'detail':'Enroll in this course first.'},status=403)
        p,_=LessonProgress.objects.get_or_create(user=request.user,lesson=lesson); p.completed=True; p.completed_at=timezone.now(); p.save(); return Response(LessonSerializer(lesson,context={'request':request}).data)
    def delete(self,request,pk):
        lesson=self.get_object(); LessonProgress.objects.filter(user=request.user,lesson=lesson).update(completed=False,completed_at=None); return Response(status=204)
class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class=QuestionSerializer
    def get_queryset(self):
        qs=Question.objects.select_related('user','course').order_by('-created_at'); c=self.request.query_params.get('course'); return qs.filter(course_id=c) if c else qs
    def perform_create(self,serializer): serializer.save(user=self.request.user)
