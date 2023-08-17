# Generated by Django 4.2.3 on 2023-08-17 06:23

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_swe', models.CharField(blank=True, max_length=300)),
                ('title_en', models.CharField(blank=True, max_length=300)),
                ('title_easy_swe', models.CharField(blank=True, max_length=300)),
                ('desc_swe', ckeditor.fields.RichTextField(blank=True, verbose_name='Swedish')),
                ('desc_en', ckeditor.fields.RichTextField(blank=True, verbose_name='English')),
                ('desc_easy_swe', ckeditor.fields.RichTextField(blank=True, verbose_name='Easy Swedish')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('chapter_hour', models.PositiveSmallIntegerField(default=0, editable=False)),
                ('chapter_minute', models.PositiveSmallIntegerField(default=0, editable=False)),
            ],
        ),
    ]
