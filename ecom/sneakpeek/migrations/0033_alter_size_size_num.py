# Generated by Django 5.0.2 on 2024-04-12 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sneakpeek', '0032_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='size',
            name='size_num',
            field=models.CharField(max_length=5),
        ),
    ]