# Generated by Django 4.0 on 2024-11-05 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='if_staff',
            field=models.BooleanField(default=False),
        ),
    ]
