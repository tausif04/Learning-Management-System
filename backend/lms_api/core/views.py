from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics,permissions,status,viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Course,Enrollment,Lesson,LessonProgress
from .serializers import *
User=get_user_model()
class SignupView(generics.CreateAPIView): permission_classes=[permissions.AllowAny]; serializer_class=SignupSerializer
    
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Course.objects.select_related('instructor').prefetch_related('modules__lessons').all(); permission_classes=[permissions.IsAuthenticated]
    def get_serializer_class(self): return CourseDetailSerializer if self.action=='retrieve' else CourseListSerializer
    @action(detail=True,methods=['post'])
    def enroll(self,request,pk=None):
        course=self.get_object(); Enrollment.objects.get_or_create(user=request.user,course=course); return Response({'detail':'Enrolled successfully.'})
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class=UserSerializer
    def get_object(self): return self.request.user
class EnrollmentView(generics.ListAPIView):
    serializer_class=CourseListSerializer
    def get_queryset(self): return Course.objects.filter(enrollments__user=self.request.user).select_related('instructor').distinct()
class LessonCompleteView(generics.GenericAPIView):
    def post(self,request,pk):
        lesson=Lesson.objects.get(pk=pk)
        if not Enrollment.objects.filter(user=request.user,course=lesson.module.course).exists(): return Response({'detail':'Enroll in the course first.'},status=403)
        p,_=LessonProgress.objects.get_or_create(user=request.user,lesson=lesson); p.completed=not p.completed; p.completed_at=timezone.now() if p.completed else None; p.save()
        return Response({'completed':p.completed})
