# Generated by Django 5.0.2 on 2024-04-06 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sneakpeek', '0025_userprofile_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='approved',
            field=models.BooleanField(null=True),
        ),
    ]
