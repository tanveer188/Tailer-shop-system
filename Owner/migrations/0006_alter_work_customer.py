# Generated by Django 4.2.1 on 2023-05-05 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0002_remove_customers_measurement_measurement_customers'),
        ('Owner', '0005_alter_work_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.customers'),
        ),
    ]
