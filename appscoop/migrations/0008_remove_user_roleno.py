# Generated by Django 4.2 on 2023-05-06 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("appscoop", "0007_alter_user_first_name_post_req_ibca"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="roleno",
        ),
    ]
