from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial=True
    dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
        migrations.CreateModel(name='Course',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('title',models.CharField(max_length=200)),('description',models.TextField()),('thumbnail',models.URLField(blank=True)),('created_at',models.DateTimeField(auto_now_add=True)),('instructor',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='courses_taught',to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name='Module',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('title',models.CharField(max_length=200)),('order',models.PositiveIntegerField(default=0)),('course',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='modules',to='core.course'))]),
        migrations.CreateModel(name='Lesson',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('title',models.CharField(max_length=200)),('content',models.TextField(blank=True)),('video_url',models.URLField(blank=True)),('order',models.PositiveIntegerField(default=0)),('module',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='lessons',to='core.module'))]),
        migrations.CreateModel(name='Enrollment',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('enrolled_at',models.DateTimeField(auto_now_add=True)),('course',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='enrollments',to='core.course')),('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='enrollments',to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name='LessonProgress',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('completed',models.BooleanField(default=False)),('completed_at',models.DateTimeField(blank=True,null=True)),('lesson',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='progress_records',to='core.lesson')),('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='lesson_progress',to=settings.AUTH_USER_MODEL))]),
        migrations.AddConstraint(model_name='enrollment',constraint=models.UniqueConstraint(fields=('user','course'),name='unique_enrollment')),
        migrations.AddConstraint(model_name='lessonprogress',constraint=models.UniqueConstraint(fields=('user','lesson'),name='unique_lesson_progress')),
    ]
