# Generated by Django 5.1.6 on 2025-04-23 16:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0004_payment'),
        ('teacher', '0022_teacher_profilepermission_create_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='user_course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teacher.usercourses'),
        ),
    ]
