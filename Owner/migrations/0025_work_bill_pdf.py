# Generated by Django 4.2.1 on 2023-05-28 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Owner', '0024_alter_work_billno_alter_work_worker'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='bill_pdf',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]