# Generated by Django 5.0.2 on 2024-03-21 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sneakpeek', '0018_alter_returnrequest_order_alter_returnrequest_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='seller',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='earning',
            field=models.IntegerField(default=1),
        ),
    ]