# Generated by Django 4.2 on 2023-04-17 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customers',
            name='measurement',
        ),
        migrations.AddField(
            model_name='measurement',
            name='customers',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Customer.customers'),
        ),
    ]
