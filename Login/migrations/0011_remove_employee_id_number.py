# Generated by Django 4.1.7 on 2023-04-15 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0010_employee_id_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='id_number',
        ),
    ]
