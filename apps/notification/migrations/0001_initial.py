# Generated by Django 4.1.2 on 2022-11-27 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(blank=True, max_length=64, unique=True)),
                ('type_notif', models.CharField(choices=[('Add_Post', 'Add Post'), ('Like_Post', 'Like Post'), ('Add_Comment', 'Add Comment'), ('Like_Comment', 'Like Comment'), ('Follow_Or_Unfollow', 'Follow Unfollow')], max_length=30, verbose_name='type_notif')),
                ('seen', models.BooleanField(default=False)),
                ('read', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('comment_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notif_comment_post', to='comment.comment')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notif_from', to=settings.AUTH_USER_MODEL)),
                ('like_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notif_like_comment', to='comment.likecomment')),
                ('like_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notif_like_post', to='post.likepost')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notif_post', to='post.post')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notif_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated'],
            },
        ),
    ]
