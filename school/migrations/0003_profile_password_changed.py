# Generated by Django 3.2.6 on 2021-08-19 18:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("school", "0002_profile_complete"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="password_changed",
            field=models.BooleanField(default=False),
        ),
    ]
