# Generated by Django 4.1.7 on 2023-04-16 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0012_employee_id_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='id_number',
            field=models.CharField(max_length=13, unique=True),
        ),
    ]
