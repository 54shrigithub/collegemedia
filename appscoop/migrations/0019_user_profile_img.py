# Generated by Django 4.2 on 2023-05-17 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appscoop", "0018_inbox"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="profile_img",
            field=models.ImageField(
                default="/static/images/default.jpg", upload_to="profile_images/"
            ),
        ),
    ]
