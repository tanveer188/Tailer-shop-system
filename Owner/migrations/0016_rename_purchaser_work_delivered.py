# Generated by Django 4.2.1 on 2023-05-07 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Owner', '0015_alter_work_billno'),
    ]

    operations = [
        migrations.RenameField(
            model_name='work',
            old_name='purchaser',
            new_name='delivered',
        ),
    ]
