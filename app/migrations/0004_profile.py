# Generated by Django 5.2 on 2025-04-10 17:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_myuser_verify_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, verbose_name='نام')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='نام خانوادگی')),
                ('nationality_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='کد ملی')),
                ('personal_code', models.CharField(blank=True, max_length=5, verbose_name='کد نظام پزشکی')),
                ('date_of_birth', models.CharField(blank=True, max_length=8, verbose_name='تاریخ تولد')),
                ('city', models.CharField(blank=True, max_length=70, verbose_name='شهر')),
                ('address', models.CharField(blank=True, max_length=200, verbose_name='آدرس')),
                ('photo', models.ImageField(upload_to='face/', verbose_name='عکس')),
                ('nationality_photo', models.ImageField(upload_to='nationality/', verbose_name='عکس کارت ملی')),
                ('personal_photo', models.ImageField(upload_to='personal/', verbose_name='عکس کارت پرسنلی')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
