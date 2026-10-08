from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from lms_api.core.views import *
router=DefaultRouter(); router.register('courses',CourseViewSet,basename='course')
urlpatterns=[path('admin/',admin.site.urls),path('api/auth/token/',TokenObtainPairView.as_view()),path('api/auth/token/refresh/',TokenRefreshView.as_view()),path('api/auth/signup/',SignupView.as_view()),path('api/profile/',ProfileView.as_view()),path('api/enrollments/',EnrollmentView.as_view()),path('api/lessons/<int:pk>/complete/',LessonCompleteView.as_view()),path('api/',include(router.urls))]
