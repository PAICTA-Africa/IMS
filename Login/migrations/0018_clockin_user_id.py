# Generated by Django 4.1.7 on 2023-04-19 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0017_alter_employee_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='clockin',
            name='user_id',
            field=models.IntegerField(default=None, max_length=255),
        ),
    ]
