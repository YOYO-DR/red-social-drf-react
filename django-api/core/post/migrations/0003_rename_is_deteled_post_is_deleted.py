# Generated by Django 4.0 on 2024-04-14 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_post', '0002_post_is_deteled'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='is_deteled',
            new_name='is_deleted',
        ),
    ]
