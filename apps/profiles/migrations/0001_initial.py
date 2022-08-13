# Generated by Django 3.2.14 on 2022-08-13 19:05

import apps.utils.function
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, max_length=500, verbose_name='uid')),
                ('pseudo', models.CharField(blank=True, max_length=48, unique=True, verbose_name='pseudo')),
                ('bio', models.CharField(blank=True, max_length=360, verbose_name='bio')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='birth date')),
                ('profile_picture', models.ImageField(blank=True, default='default/profilePic.jpg', null=True, upload_to=apps.utils.function.rename_img_profile, verbose_name='profile picture')),
                ('cover_picture', models.ImageField(blank=True, default='default/coverPic.jpg', null=True, upload_to=apps.utils.function.rename_img_profile, verbose_name='cover picture')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='update date')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('following', models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
                'ordering': ('-created',),
            },
        ),
    ]
