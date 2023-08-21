# Generated by Django 4.2.3 on 2023-08-21 12:18

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chapters', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_open', models.BooleanField(default=False)),
                ('lesson_time', models.PositiveSmallIntegerField(help_text='in minute', validators=[django.core.validators.MinValueValidator(1)])),
                ('ordering_number', models.PositiveSmallIntegerField(default=1, unique=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('title_swe', models.CharField(blank=True, max_length=300)),
                ('title_en', models.CharField(blank=True, max_length=300)),
                ('title_easy_swe', models.CharField(blank=True, max_length=300)),
                ('text_swe', ckeditor.fields.RichTextField(blank=True, max_length=700, verbose_name='Swedish')),
                ('text_en', ckeditor.fields.RichTextField(blank=True, max_length=700, verbose_name='English')),
                ('text_easy_swe', ckeditor.fields.RichTextField(blank=True, max_length=700, verbose_name='Easy Swedish')),
                ('video_swe', models.FileField(blank=True, null=True, upload_to='lesson/videos')),
                ('video_en', models.FileField(blank=True, null=True, upload_to='lesson/videos')),
                ('video_easy_swe', models.FileField(blank=True, null=True, upload_to='lesson/videos')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chapters.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='LessonWordInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('info', models.TextField(max_length=500)),
                ('lessons', models.ManyToManyField(to='lessons.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='LessonSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500)),
                ('link', models.URLField()),
                ('lessons', models.ManyToManyField(to='lessons.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='LessonStudentStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_date', models.DateField(auto_now_add=True)),
                ('lesson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lessons.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('lesson', 'student')},
            },
        ),
        migrations.CreateModel(
            name='LessonStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_completed', models.BooleanField(default=False)),
                ('ball', models.PositiveSmallIntegerField(default=0)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('lesson', 'student')},
            },
        ),
    ]
