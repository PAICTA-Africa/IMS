# Generated by Django 4.1.7 on 2023-03-21 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0004_alter_employee_ip_address_alter_employee_mac_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=255),
        ),
    ]
