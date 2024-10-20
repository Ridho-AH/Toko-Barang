# Generated by Django 4.2.6 on 2023-11-10 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_customer_purchaseitem_grade_saleitem_grade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salebill',
            name='address',
        ),
        migrations.RemoveField(
            model_name='salebill',
            name='name',
        ),
        migrations.RemoveField(
            model_name='salebill',
            name='npwp',
        ),
        migrations.RemoveField(
            model_name='salebill',
            name='phone',
        ),
        migrations.AddField(
            model_name='salebill',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='salecustomer', to='transactions.customer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='t_debt',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customer',
            name='npwp',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='t_debt',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='npwp',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
