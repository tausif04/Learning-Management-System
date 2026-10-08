from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from lms_api.core.models import UserProfile, Category, Course, Lesson, Material
User=get_user_model()
class Command(BaseCommand):
    help='Create demo LMS data for local development.'
    def handle(self,*args,**kwargs):
        teacher,_=User.objects.get_or_create(username='instructor',defaults={'email':'instructor@example.com','first_name':'Demo','last_name':'Instructor'})
        if not teacher.has_usable_password(): teacher.set_password('password123'); teacher.save()
        UserProfile.objects.get_or_create(user=teacher,defaults={'role':'teacher'})
        samples=[('Python','Python for Beginners','Build a strong Python foundation from syntax to functions and practical problem solving.'),('Web Development','Modern Web Development','Learn the fundamentals of building responsive web applications.'),('Data Science','Data Science Foundations','Understand the workflow from data preparation to basic analysis.')]
        for cat_name,title,desc in samples:
            cat,_=Category.objects.get_or_create(name=cat_name)
            course,_=Course.objects.get_or_create(title=title,defaults={'description':desc,'category':cat,'instructor':teacher})
            if course.category_id!=cat.id: course.category=cat; course.save(update_fields=['category'])
            for i,lesson_title in enumerate(['Introduction','Core concepts','Practical exercise'],1):
                lesson,_=Lesson.objects.get_or_create(course=course,order=i,defaults={'title':lesson_title,'content':f'{lesson_title} for {course.title}. Work through the material and mark this lesson complete when finished.','duration_minutes':20})
                Material.objects.get_or_create(lesson=lesson,title='Lesson notes',defaults={'file_url':'https://example.com/'})
        self.stdout.write(self.style.SUCCESS('Demo LMS data created. Instructor login: instructor / password123'))
