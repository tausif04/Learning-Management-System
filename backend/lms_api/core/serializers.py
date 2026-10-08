from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from rest_framework import serializers
from .models import UserProfile, Category, Course, Lesson, Material, Enrollment, LessonProgress, Question
User=get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role=serializers.SerializerMethodField()
    bio=serializers.SerializerMethodField()
    avatar_url=serializers.SerializerMethodField()
    def get_role(self,obj): return getattr(getattr(obj,'profile',None),'role','student')
    def get_bio(self,obj): return getattr(getattr(obj,'profile',None),'bio','')
    def get_avatar_url(self,obj): return getattr(getattr(obj,'profile',None),'avatar_url','')
    class Meta: model=User; fields=['id','username','email','first_name','last_name','role','bio','avatar_url']

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=6)
    role=serializers.ChoiceField(choices=['student','teacher'],default='student',write_only=True)
    class Meta: model=User; fields=['username','email','password','first_name','last_name','role']
    def create(self,validated_data):
        role=validated_data.pop('role','student'); user=User.objects.create_user(**validated_data); UserProfile.objects.create(user=user,role=role); return user

class ProfileSerializer(serializers.ModelSerializer):
    role=serializers.CharField(source='profile.role',required=False)
    bio=serializers.CharField(source='profile.bio',required=False,allow_blank=True)
    avatar_url=serializers.CharField(source='profile.avatar_url',required=False,allow_blank=True)
    class Meta: model=User; fields=['id','username','email','first_name','last_name','role','bio','avatar_url']; read_only_fields=['id','username']
    def update(self,instance,validated_data):
        profile_data=validated_data.pop('profile',{})
        for k,v in validated_data.items(): setattr(instance,k,v)
        instance.save()
        p,_=UserProfile.objects.get_or_create(user=instance)
        for k,v in profile_data.items(): setattr(p,k,v)
        p.save(); return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta: model=Category; fields=['id','name']

class InstructorSerializer(serializers.ModelSerializer):
    class Meta: model=User; fields=['id','username','first_name','last_name']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta: model=Material; fields=['id','title','lesson','file_url']

class LessonSerializer(serializers.ModelSerializer):
    completed=serializers.SerializerMethodField()
    materials=MaterialSerializer(many=True,read_only=True)
    def get_completed(self,obj):
        request=self.context.get('request')
        return bool(request and request.user.is_authenticated and LessonProgress.objects.filter(user=request.user,lesson=obj,completed=True).exists())
    class Meta: model=Lesson; fields=['id','title','course','content','video_url','order','duration_minutes','completed','materials']

class CourseSerializer(serializers.ModelSerializer):
    instructor=InstructorSerializer(read_only=True)
    category=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),required=False,allow_null=True)
    category_detail=CategorySerializer(source='category',read_only=True)
    enrolled=serializers.SerializerMethodField()
    progress=serializers.SerializerMethodField()
    lesson_count=serializers.SerializerMethodField()
    lessons=LessonSerializer(many=True,read_only=True)
    def get_lesson_count(self,obj): return obj.lessons.count()
    def get_enrolled(self,obj):
        r=self.context.get('request'); return bool(r and r.user.is_authenticated and Enrollment.objects.filter(user=r.user,course=obj).exists())
    def get_progress(self,obj):
        r=self.context.get('request')
        if not r or not r.user.is_authenticated:return 0
        total=obj.lessons.count()
        if not total:return 0
        done=LessonProgress.objects.filter(user=r.user,lesson__course=obj,completed=True).count()
        return round(done*100/total)
    class Meta: model=Course; fields=['id','title','description','category','category_detail','instructor','thumbnail','created_at','is_published','enrolled','progress','lesson_count','lessons']

class EnrollmentSerializer(serializers.ModelSerializer):
    course_detail=CourseSerializer(source='course',read_only=True)
    class Meta: model=Enrollment; fields=['id','user','course','course_detail','enrolled_at']; read_only_fields=['user']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta: model=Question; fields=['id','question_text','answer_text','course','user','created_at']; read_only_fields=['user']
