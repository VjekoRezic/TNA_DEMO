# Generated by Django 4.1.5 on 2023-02-12 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tna_system', '0007_alter_record_record_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='event_id',
            new_name='event',
        ),
        migrations.RenameField(
            model_name='record',
            old_name='user_id',
            new_name='user',
        ),
    ]
