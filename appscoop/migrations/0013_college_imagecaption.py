# Generated by Django 4.2 on 2023-05-09 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appscoop", "0012_rename_post_req_ibca_post_req"),
    ]

    operations = [
        migrations.AddField(
            model_name="college",
            name="imagecaption",
            field=models.CharField(default="", max_length=200),
        ),
    ]