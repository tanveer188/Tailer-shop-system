# Generated by Django 4.2.1 on 2023-05-05 07:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Owner', '0007_remove_owner_db_user_owner_db_mobileno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner_db',
            name='mobileNo',
            field=models.IntegerField(blank=True, null=True, unique=True, validators=[django.core.validators.MaxValueValidator(9999999999), django.core.validators.MinValueValidator(1111111111)]),
        ),
    ]
