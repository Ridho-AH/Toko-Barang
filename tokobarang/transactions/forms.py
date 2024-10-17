from django import forms
from django.forms import formset_factory
from .models import (
    Supplier, 
    Customer, 
    SupDebtHistory,
    CusDebtHistory,
    PurchaseBill, 
    PurchaseItem,
    PurchaseBillDetails, 
    SaleBill, 
    SaleItem,
    SaleBillDetails
)
from inventory.models import Stock


class SelectSupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.filter(is_deleted=False)
        self.fields['supplier'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        model = PurchaseBill
        fields = ['supplier']


class SelectCustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(is_deleted=False)
        self.fields['customer'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        model = SaleBill
        fields = ['customer']


class SupDebtHistoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Supplier.objects.filter(is_deleted=False)
        self.fields['subject'].widget.attrs.update({'class': 'textinput form-control', 'readonly': 'True'})
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'readonly': 'True'})
        self.fields['total'].widget.attrs.update({'class': 'textinput form-control', 'readonly': 'True'})
        self.fields['amount'].widget.attrs.update({'class': 'textinput form-control', 'min': '0', 'onchange': 'updet()'})
        self.fields['remain'].widget.attrs.update({'class': 'textinput form-control', 'min': '0', 'readonly': 'True'})
        self.fields['retur'].widget.attrs.update({'class': 'textinput form-control', 'min': '0', 'readonly': 'True'})
        self.fields['stat'].widget.attrs.update({'class': 'textinput form-control', 'readonly': 'True'})

    class Meta:
        model = SupDebtHistory
        fields = ['subject', 'name', 'total', 'amount', 'remain', 'retur', 'stat']
        labels = {
            'subject': ('Supplier'),
            'name': ('Nama'),
            'total': ('Jumlah Hutang'),
            'amount': ('Jumlah Pelunasan'),
            'remain': ('Sisa Hutang'),
            'retur': ('Kembalian'),
            'stat': ('Status'),
        }
        widgets = {'name': forms.HiddenInput()}


class CusDebtHistoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Customer.objects.filter(is_deleted=False)
        self.fields['subject'].widget.attrs.update({'class': 'textinput form-control', 'readonly': 'True'})
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'readonly': 'True'})
        self.fields['total'].widget.attrs.update({'class': 'textinput form-control', 'readonly': 'True'})
        self.fields['amount'].widget.attrs.update({'class': 'textinput form-control', 'min': '0', 'onchange': 'updet()'})
        self.fields['remain'].widget.attrs.update({'class': 'textinput form-control', 'min': '0', 'readonly': 'True'})
        self.fields['retur'].widget.attrs.update({'class': 'textinput form-control', 'min': '0', 'readonly': 'True'})
        self.fields['stat'].widget.attrs.update({'class': 'textinput form-control', 'readonly': 'True'})

    class Meta:
        model = CusDebtHistory
        fields = ['subject', 'name', 'total', 'amount', 'remain', 'retur', 'stat']
        labels = {
            'subject': ('Pembeli'),
            'name': ('Nama'),
            'total': ('Jumlah Hutang'),
            'amount': ('Jumlah Pembayaran'),
            'remain': ('Sisa Hutang'),
            'retur': ('Kembalian'),
            'stat': ('Status'),
        }
        widgets = {'name': forms.HiddenInput()}


class PurchaseItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})
    class Meta:
        model = PurchaseItem
        fields = ['stock', 'quantity', 'perprice']

PurchaseItemFormset = formset_factory(PurchaseItemForm, extra=1)


class PurchaseDetailsForm(forms.ModelForm):
    class Meta:
        model = PurchaseBillDetails
        fields = ['ppn', 'pph', 'paid', 'stat', 'cgst', 'sgst', 'igst', 'retur', 'debt', 'total']


class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only', 'required': 'true'})
        self.fields['gender'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '12', 'pattern' : '[0-9]+', 'title' : 'Numbers only'})
        self.fields['address'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['npwp'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '16', 'pattern' : '[A-Z0-9]+', 'title' : 'npwp Format Required'})
    class Meta:
        model = Supplier
        fields = ['name', 'gender', 'phone', 'address', 'email', 'npwp']
        widgets = {
            'address' : forms.Textarea(
                attrs = {
                    'class' : 'textinput form-control',
                    'rows'  : '4'
                }
            )
        }


class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only', 'required': 'true'})
        self.fields['gender'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['age'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '12', 'pattern' : '[0-9]+', 'title' : 'Numbers only'})
        self.fields['address'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['npwp'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '16', 'pattern' : '[A-Z0-9]+', 'title' : 'npwp Format Required'})
    class Meta:
        model = Customer
        fields = ['name', 'gender', 'age', 'phone', 'address', 'npwp']
        widgets = {
            'address' : forms.Textarea(
                attrs = {
                    'class' : 'textinput form-control',
                    'rows'  : '4'
                }
            )
        }


class SaleItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['condition'].widget.attrs.update({'class': 'textinput form-control setprice condition', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})
    class Meta:
        model = SaleItem
        fields = ['stock', 'condition', 'quantity', 'perprice']

SaleItemFormset = formset_factory(SaleItemForm, extra=1)


class SaleDetailsForm(forms.ModelForm):
    class Meta:
        model = SaleBillDetails
        fields = ['ppn', 'pph', 'paid', 'stat', 'cgst', 'sgst', 'igst', 'retur', 'debt', 'total']
