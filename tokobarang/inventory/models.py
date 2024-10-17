from django.db import models
from django.db.models.functions import Lower
from django_random_id_model import RandomIDModel
import time
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import make_aware


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    grade = models.CharField(max_length=30)
    good_qty = models.IntegerField(default=0)
    bad_qty = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        ordering = [Lower("name")]
    def __str__(self):
        return f'{self.name}_{self.grade}'


class StockHistory(models.Model):
    GOOD = "Baik"
    BAD = "Buruk"
    STAT_CHOICES = [
        (GOOD, "Baik"),
        (BAD, "Buruk"),
    ]
    
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='stockitem')
    name = models.CharField(max_length=30)
    grade = models.CharField(max_length=30)
    quantity = models.IntegerField(default=0)
    source = models.CharField(max_length=50, blank=True, null=True)
    stat = models.CharField(max_length=12, choices=STAT_CHOICES, default=GOOD)
    time = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

