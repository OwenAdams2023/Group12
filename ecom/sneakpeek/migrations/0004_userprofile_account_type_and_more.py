# Generated by Django 5.0.2 on 2024-03-12 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sneakpeek', '0003_rename_type_account_account_type_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='account_type',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
