# Generated by Django 5.0.2 on 2024-03-21 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sneakpeek', '0023_userprofile_earning'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='earning',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
