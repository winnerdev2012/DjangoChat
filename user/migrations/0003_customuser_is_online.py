# Generated by Django 4.1.6 on 2023-03-27 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_customuser_gender_customuser_profile_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_online',
            field=models.BooleanField(default=False),
        ),
    ]
