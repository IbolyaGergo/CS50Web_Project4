# Generated by Django 4.1.5 on 2023-06-16 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_remove_user_liking_post_liker'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='liker',
            new_name='likers',
        ),
    ]