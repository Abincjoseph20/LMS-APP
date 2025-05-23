# Generated by Django 5.1.6 on 2025-04-10 09:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0014_lessons'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_type', models.CharField(choices=[('Note', 'Note'), ('PDF', 'PDF'), ('PPT', 'PPT')], max_length=10)),
                ('title', models.CharField(max_length=500)),
                ('file', models.FileField(default='path/to/default/file.pdf', upload_to='course_resources/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.course')),
            ],
        ),
    ]
