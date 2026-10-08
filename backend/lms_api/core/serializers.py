from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from .models import Course,Module,Lesson,Enrollment,LessonProgress
User=get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta: model=User; fields=['id','username','email','first_name','last_name']
class SignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=6)
    class Meta: model=User; fields=['username','email','password','first_name','last_name']
    def create(self,v): return User.objects.create_user(**v)
class LessonSerializer(serializers.ModelSerializer):
    completed=serializers.SerializerMethodField()
    def get_completed(self,obj):
        u=self.context['request'].user
        return LessonProgress.objects.filter(user=u,lesson=obj,completed=True).exists()
    class Meta: model=Lesson; fields=['id','title','content','video_url','order','completed']
class ModuleSerializer(serializers.ModelSerializer):
    lessons=LessonSerializer(many=True,read_only=True)
    class Meta: model=Module; fields=['id','title','order','lessons']
class CourseListSerializer(serializers.ModelSerializer):
    instructor=UserSerializer(read_only=True); progress=serializers.SerializerMethodField(); enrolled=serializers.SerializerMethodField()
    def get_enrolled(self,obj): return Enrollment.objects.filter(user=self.context['request'].user,course=obj).exists()
    def get_progress(self,obj):
        total=Lesson.objects.filter(module__course=obj).count()
        if not total:return 0
        done=LessonProgress.objects.filter(user=self.context['request'].user,lesson__module__course=obj,completed=True).count()
        return round(done*100/total)
    class Meta: model=Course; fields=['id','title','description','instructor','thumbnail','progress','enrolled']
class CourseDetailSerializer(CourseListSerializer):
    modules=ModuleSerializer(many=True,read_only=True)
    class Meta(CourseListSerializer.Meta): fields=CourseListSerializer.Meta.fields+['modules']
