# Generated by Django 4.1.5 on 2023-01-24 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tna_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='updated_at',
            field=models.DateTimeField(null=True, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='record',
            name='out_time',
            field=models.DateTimeField(null=True, verbose_name='OUT'),
        ),
    ]
