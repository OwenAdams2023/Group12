# Generated by Django 5.0.2 on 2024-03-20 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sneakpeek', '0014_rename_customer_orderitem_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='user',
            new_name='customer',
        ),
        migrations.AddField(
            model_name='order',
            name='card_number',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
    ]