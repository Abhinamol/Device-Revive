# Generated by Django 4.2.5 on 2023-11-04 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0011_technician_is_active_technician_is_admin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
