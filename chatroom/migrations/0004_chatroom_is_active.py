# Generated by Django 4.1.6 on 2023-03-09 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatroom', '0003_chatroom_is_group_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]