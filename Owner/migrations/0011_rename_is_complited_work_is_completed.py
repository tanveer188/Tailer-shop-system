# Generated by Django 4.2.1 on 2023-05-05 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Owner', '0010_alter_owner_db_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='work',
            old_name='is_complited',
            new_name='is_completed',
        ),
    ]
