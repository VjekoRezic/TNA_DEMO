# Generated by Django 4.1.5 on 2023-02-12 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_user_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='card_id',
            field=models.CharField(max_length=20, null=True, unique=True, verbose_name='Card ID'),
        ),
    ]