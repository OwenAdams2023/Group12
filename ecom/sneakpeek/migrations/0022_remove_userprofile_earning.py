# Generated by Django 5.0.2 on 2024-03-21 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sneakpeek', '0021_alter_userprofile_earning'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='earning',
        ),
    ]
