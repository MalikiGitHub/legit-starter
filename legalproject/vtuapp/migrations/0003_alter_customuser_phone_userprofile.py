# Generated by Django 5.1.4 on 2025-01-23 10:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vtuapp', '0002_referal_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='Phone',
            field=models.CharField(blank=True, max_length=14),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('location', models.CharField(blank=True, max_length=50)),
                ('dob', models.DateField(blank=True, null=True)),
                ('profile_image', models.ImageField(blank=True, upload_to='profile/')),
                ('facebook', models.URLField(blank=True)),
                ('Account_name', models.CharField(blank=True, max_length=30, null=True)),
                ('Account_number', models.CharField(blank=True, max_length=10, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
