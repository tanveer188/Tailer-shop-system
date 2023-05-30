# Generated by Django 4.2.1 on 2023-05-27 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Owner', '0023_alter_work_worker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='billno',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Owner.member'),
        ),
    ]