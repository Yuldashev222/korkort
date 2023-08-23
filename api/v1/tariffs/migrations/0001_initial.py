# Generated by Django 4.2.3 on 2023-08-23 10:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('discounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TariffInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='tariffs/images/')),
                ('desc', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('price', models.PositiveIntegerField()),
                ('tariff_discount_amount', models.FloatField(default=0)),
                ('student_discount_amount', models.FloatField(default=0)),
                ('student_discount', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='discounts.tariffdiscount')),
                ('tariff_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tariffs.tariffinfo')),
            ],
        ),
    ]
