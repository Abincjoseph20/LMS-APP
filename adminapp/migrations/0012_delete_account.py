# Generated by Django 5.1.6 on 2025-03-05 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0011_account_first_name_account_last_name_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Account',
        ),
    ]
