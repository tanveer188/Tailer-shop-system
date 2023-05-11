# Generated by Django 4.2.1 on 2023-05-07 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Owner', '0011_rename_is_complited_work_is_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='aster_status',
        ),
        migrations.RemoveField(
            model_name='work',
            name='piku_status',
        ),
        migrations.AlterField(
            model_name='work',
            name='is_astar',
            field=models.CharField(choices=[('1', 'No Need'), ('2', 'Need'), ('3', 'Fulfilled'), ('4', 'Provided')], default='1', max_length=30),
        ),
        migrations.AlterField(
            model_name='work',
            name='is_piku',
            field=models.CharField(choices=[('1', 'No Need'), ('2', 'Need'), ('3', 'Fulfilled')], default='1', max_length=30),
        ),
        migrations.AlterField(
            model_name='work',
            name='purchaser',
            field=models.BooleanField(default=False),
        ),
    ]