# Generated by Django 5.1.6 on 2025-03-10 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0022_account_address_alter_account_roles'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Account',
        ),
    ]
