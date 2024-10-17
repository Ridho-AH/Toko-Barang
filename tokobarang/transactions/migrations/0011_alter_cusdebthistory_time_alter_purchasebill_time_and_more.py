# Generated by Django 4.2.6 on 2023-11-23 05:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0010_alter_cusdebthistory_time_alter_purchasebill_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cusdebthistory',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='purchasebill',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='salebill',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='supdebthistory',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
