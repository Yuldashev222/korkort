# Generated by Django 4.2.3 on 2023-08-23 10:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestBall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
    ]
