# Generated by Django 3.2.6 on 2021-08-17 07:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("student", "0007_supportdocument"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supportdocument",
            name="document",
            field=models.CharField(
                help_text="Please mention the supporting document on basis of which the change was made. Ex: admission register / birth certificate / etc",
                max_length=50,
            ),
        ),
    ]
