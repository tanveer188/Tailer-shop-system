# Generated by Django 4.2.1 on 2023-05-21 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Owner', '0019_alter_work_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='workDone',
        ),
        migrations.RemoveField(
            model_name='work',
            name='worker',
        ),
    ]
