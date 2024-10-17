from django import forms
from .models import Stock
from .models import StockHistory

class StockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['grade'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['good_qty'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})
        self.fields['bad_qty'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})

    class Meta:
        model = Stock
        fields = ['name', 'grade', 'good_qty', 'bad_qty']


class StockHistoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control', 'onchange': 'updet(this)'})
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'readonly': 'True'})
        self.fields['grade'].widget.attrs.update({'class': 'textinput form-control', 'readonly': 'True'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})
        self.fields['source'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['stat'].widget.attrs.update({'class': 'textinput form-control'})

    class Meta:
        model = StockHistory
        fields = ['stock', 'name', 'grade', 'quantity', 'source', 'stat']
        labels = {
            'stock': ('Stok'),
            'name': ('Nama'),
            'grade': ('Grade'),
            'quantity': ('Jumlah'),
            'source': ('Sumber'),
            'stat': ('Kondisi'),
        }
