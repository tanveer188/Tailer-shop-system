# Generated by Django 4.2.1 on 2023-05-21 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Owner', '0017_organization_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Owner.organization'),
        ),
    ]
