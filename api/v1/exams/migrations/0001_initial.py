# Generated by Django 4.2.3 on 2023-08-17 10:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chapters', '0001_initial'),
        ('lessons', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty_level', models.PositiveSmallIntegerField(choices=[['easy', 1], ['average', 2], ['difficult', 3]], default=1)),
                ('for_lesson', models.BooleanField(default=False)),
                ('sorting_number', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('text_swe', models.CharField(blank=True, max_length=300, verbose_name='Swedish')),
                ('text_en', models.CharField(blank=True, max_length=300, verbose_name='English')),
                ('text_easy_swe', models.CharField(blank=True, max_length=300, verbose_name='Easy Swedish')),
                ('video_swe', models.FileField(blank=True, null=True, upload_to='')),
                ('video_eng', models.FileField(blank=True, null=True, upload_to='')),
                ('video_easy_swe', models.FileField(blank=True, null=True, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chapter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='chapters.chapter')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lessons.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='WrongQuestionStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_correct', models.BooleanField(default=False)),
                ('text_swe', models.CharField(blank=True, max_length=300, verbose_name='Swedish')),
                ('text_en', models.CharField(blank=True, max_length=300, verbose_name='English')),
                ('text_easy_swe', models.CharField(blank=True, max_length=300, verbose_name='Easy Swedish')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.question')),
            ],
        ),
        migrations.CreateModel(
            name='SavedQuestionStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]