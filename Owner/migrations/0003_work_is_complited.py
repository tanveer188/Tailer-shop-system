# Generated by Django 4.2 on 2023-04-12 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Owner', '0002_owner_db_email_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='is_complited',
            field=models.BooleanField(default=False),
        ),
    ]
