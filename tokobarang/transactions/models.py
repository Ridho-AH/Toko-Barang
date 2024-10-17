from django.db import models
from inventory.models import Stock
from django.db.models.functions import Lower
from django_random_id_model import RandomIDModel
import time
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import make_aware


class Supplier(models.Model):
    MALE = "Laki-laki"
    FEMALE = "Perempuan"
    GENDER_CHOICES = [
        (MALE, "Laki-laki"),
        (FEMALE, "Perempuan"),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    gender = models.CharField(max_length=12, choices=GENDER_CHOICES, default=MALE)
    phone = models.CharField(max_length=12, unique=True, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    npwp = models.CharField(max_length=16, unique=True, blank=True, null=True)
    t_debt = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        ordering = [Lower("name")]
    def __str__(self):
	    return self.name


class Customer(models.Model):
    MALE = "Laki-laki"
    FEMALE = "Perempuan"
    GENDER_CHOICES = [
        (MALE, "Laki-laki"),
        (FEMALE, "Perempuan"),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    gender = models.CharField(max_length=12, choices=GENDER_CHOICES, default=MALE)
    age = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=12, unique=True, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    npwp = models.CharField(max_length=16, unique=True, blank=True, null=True)
    t_debt = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        ordering = [Lower("name")]
    def __str__(self):
	    return self.name


class SupDebtHistory(models.Model):
    subject = models.ForeignKey(Supplier, on_delete = models.CASCADE, related_name='debtsupplier')
    name = models.CharField(max_length=150)
    total = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    remain = models.IntegerField(default=0)
    retur = models.IntegerField(default=0)
    stat = models.CharField(max_length=50, blank=True, null=True)
    time = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)


class CusDebtHistory(models.Model):
    subject = models.ForeignKey(Customer, on_delete = models.CASCADE, related_name='debtcustomer')
    name = models.CharField(max_length=150)
    total = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    remain = models.IntegerField(default=0)
    retur = models.IntegerField(default=0)
    stat = models.CharField(max_length=50, blank=True, null=True)
    time = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)


class PurchaseBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(default=timezone.now)
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE, related_name='purchasesupplier')

    def __str__(self):
	    return "Bill no: " + str(self.billno)
    
    def get_details(self):
        return PurchaseBillDetails.objects.filter(billno=self)
    
    def get_items_list(self):
        return PurchaseItem.objects.filter(billno=self)

    def get_total_price(self):
        purchaseitems = PurchaseItem.objects.filter(billno=self)
        total = 0
        for item in purchaseitems:
            total += item.totalprice
        return total


class PurchaseItem(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete = models.CASCADE, related_name='purchasebillno')
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='purchaseitem')
    quantity = models.IntegerField(default=1)
    perprice = models.IntegerField(default=1)
    totalprice = models.IntegerField(default=1)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno) + ", Item = " + self.stock.name


class PurchaseBillDetails(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete = models.CASCADE, related_name='purchasedetailsbillno')
    
    ppn = models.CharField(max_length=50, blank=True, null=True)    
    pph = models.CharField(max_length=50, blank=True, null=True)
    paid = models.CharField(max_length=50, blank=True, null=True)
    stat = models.CharField(max_length=50, blank=True, null=True)
    
    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    
    retur = models.CharField(max_length=50, blank=True, null=True)
    debt = models.CharField(max_length=50, blank=True, null=True)
    total = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno)


class SaleBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(default=timezone.now)

    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, related_name='salecustomer')

    def __str__(self):
	    return "Bill no: " + str(self.billno)
    
    def get_details(self):
        return SaleBillDetails.objects.filter(billno=self)
    
    def get_items_list(self):
        return SaleItem.objects.filter(billno=self)
        
    def get_total_price(self):
        saleitems = SaleItem.objects.filter(billno=self)
        total = 0
        for item in saleitems:
            total += item.totalprice
        return total


class SaleItem(models.Model):
    FRESH = "Standar"
    NOT_FRESH = "Ekonomis"
    CONDITION_CHOICES = [
        (FRESH, "Standar"),
        (NOT_FRESH, "Ekonomis"),
    ]
    
    billno = models.ForeignKey(SaleBill, on_delete = models.CASCADE, related_name='salebillno')
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='saleitem')
    condition = models.CharField(max_length=18, choices=CONDITION_CHOICES, default=FRESH)
    quantity = models.IntegerField(default=1)
    perprice = models.IntegerField(default=1)
    totalprice = models.IntegerField(default=1)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno) + ", Item = " + self.stock.name


class SaleBillDetails(models.Model):
    billno = models.ForeignKey(SaleBill, on_delete = models.CASCADE, related_name='saledetailsbillno')
    
    ppn = models.CharField(max_length=50, blank=True, null=True)    
    pph = models.CharField(max_length=50, blank=True, null=True)
    paid = models.CharField(max_length=50, blank=True, null=True)
    stat = models.CharField(max_length=50, blank=True, null=True)
    
    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    
    retur = models.CharField(max_length=50, blank=True, null=True)
    debt = models.CharField(max_length=50, blank=True, null=True)    
    total = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno)
