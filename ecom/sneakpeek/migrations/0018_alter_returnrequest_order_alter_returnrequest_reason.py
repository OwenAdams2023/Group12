# Generated by Django 5.0.2 on 2024-03-21 05:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sneakpeek', '0017_rename_user_orderitem_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='returnrequest',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sneakpeek.orderitem'),
        ),
        migrations.AlterField(
            model_name='returnrequest',
            name='reason',
            field=models.TextField(max_length=500),
        ),
    ]
