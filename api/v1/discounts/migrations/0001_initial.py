# Generated by Django 4.2.3 on 2023-08-14 09:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('discount_value', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('is_percent', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TariffDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('discount_value', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('is_percent', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('valid_from', models.DateTimeField(blank=True, null=True)),
                ('valid_to', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='tariffdiscount',
            constraint=models.UniqueConstraint(fields=('discount_value', 'is_percent'), name='unique discounts'),
        ),
    ]
