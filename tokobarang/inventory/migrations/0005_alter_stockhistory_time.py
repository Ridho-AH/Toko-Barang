# Generated by Django 4.2.6 on 2023-11-23 05:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_remove_stock_quantity_remove_stock_source_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockhistory',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 23, 5, 36, 58, 877963, tzinfo=datetime.timezone.utc)),
        ),
    ]
