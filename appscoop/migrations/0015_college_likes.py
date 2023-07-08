# Generated by Django 4.2 on 2023-05-10 16:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appscoop", "0014_inbox"),
    ]

    operations = [
        migrations.AddField(
            model_name="college",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="liked_post", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]