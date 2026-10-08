from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, UserAuthView, ProfileView, CategoryViewSet, CourseViewSet, LessonViewSet, MaterialViewSet, EnrollmentViewSet, QuestionViewSet, LessonCompleteView, ProgressView
router=DefaultRouter()
router.register('categories',CategoryViewSet,basename='category')
router.register('courses',CourseViewSet,basename='course')
router.register('lessons',LessonViewSet,basename='lesson')
router.register('materials',MaterialViewSet,basename='material')
router.register('enrollments',EnrollmentViewSet,basename='enrollment')
router.register('questions',QuestionViewSet,basename='question')
urlpatterns=[
    path('user/auth/',UserAuthView.as_view()), path('user/register/',RegisterView.as_view()),
    path('user/profile/',ProfileView.as_view()), path('user/profile/student/',ProfileView.as_view()), path('user/profile/teacher/',ProfileView.as_view()),
    path('lessons/<int:pk>/complete/',LessonCompleteView.as_view()), path('progress/',ProgressView.as_view()),
    path('',include(router.urls)),
]
