# Generated by Django 4.2.6 on 2023-11-23 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0012_alter_purchasebill_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cusdebthistory',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='purchasebill',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='salebill',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='supdebthistory',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
