# Generated by Django 4.1.5 on 2023-01-24 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_is_staff_user_is_superuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_superadmin',
        ),
    ]
