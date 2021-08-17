# Generated by Django 3.2.6 on 2021-08-17 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_remove_student_dob_edited'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.CharField(help_text='Please mention the supporting document on basis of which the change was made. Ex: Admission Certificate', max_length=50)),
                ('student', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.student')),
            ],
        ),
    ]