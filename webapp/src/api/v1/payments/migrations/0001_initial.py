# Generated by Django 4.2.3 on 2023-07-13 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tariffs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expire_at', models.DateTimeField()),
                ('purchased_at', models.DateTimeField(auto_now_add=True)),
                ('purchased_price', models.PositiveIntegerField()),
                ('tariff_title', models.CharField(max_length=100)),
                ('tariff_price', models.PositiveIntegerField()),
                ('tariff_discount_price', models.PositiveIntegerField()),
                ('tariff_day', models.PositiveSmallIntegerField()),
                ('tariff_advantages', models.TextField(default='')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tariff', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tariffs.tariff')),
            ],
        ),
    ]
