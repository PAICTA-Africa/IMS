# Generated by Django 4.1.7 on 2023-03-21 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0003_employee_postal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='ip_address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='employee',
            name='mac_address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='employee',
            name='postal',
            field=models.CharField(max_length=255),
        ),
    ]
