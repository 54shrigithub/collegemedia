# Generated by Django 4.2 on 2023-06-20 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("appscoop", "0021_post_req_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="iibca",
            name="student",
        ),
        migrations.RemoveField(
            model_name="iiibca",
            name="student",
        ),
        migrations.RemoveField(
            model_name="staff",
            name="staff",
        ),
        migrations.DeleteModel(
            name="IBCA",
        ),
        migrations.DeleteModel(
            name="IIBCA",
        ),
        migrations.DeleteModel(
            name="IIIBCA",
        ),
        migrations.DeleteModel(
            name="STAFF",
        ),
    ]