from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View,
    CreateView, 
    UpdateView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Stock
from .models import StockHistory
from .forms import StockForm
from .forms import StockHistoryForm
from django_filters.views import FilterView
from .filters import StockFilter
from .filters import StockHistoryFilter
import time
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import make_aware


class StockListView(FilterView):
    filterset_class = StockFilter
    queryset = Stock.objects.filter(is_deleted=False)
    template_name = 'inventory.html'
    paginate_by = 10


class StockCreateView(SuccessMessageMixin, CreateView):
    model = Stock
    form_class = StockForm
    template_name = "edit_stock.html"
    success_url = '/inventory'
    success_message = "Jenis stok berhasil ditambahkan"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Jenis Stok Baru'
        context["savebtn"] = 'Tambahkan ke Gudang'
        return context       


class StockEditView(SuccessMessageMixin, UpdateView):
    model = Stock
    form_class = StockForm
    template_name = "edit_stock.html"
    success_url = '/inventory'
    success_message = "Pengaturan stok berhasil diubah"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Ubah Pengaturan Stok'
        context["savebtn"] = 'Ubah Pengaturan'
        context["delbtn"] = 'Hapus Stok'
        return context


class StockDeleteView(View):
    template_name = "delete_stock.html"
    success_message = "Stok berhasil dihapus"
    
    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        return render(request, self.template_name, {'object' : stock})

    def post(self, request, pk):  
        stock = get_object_or_404(Stock, pk=pk)
        stock.is_deleted = True
        stock.save()                                               
        messages.success(request, self.success_message)
        return redirect('inventory')


class StockHistoryDeleteView(View):
    template_name = "delete_stockhistory.html"
    success_message = "Riwayat stok berhasil dihapus"
    
    def get(self, request, pk):
        stock = get_object_or_404(StockHistory, pk=pk)
        return render(request, self.template_name, {'object' : stock})

    def post(self, request, pk):  
        stock = get_object_or_404(StockHistory, pk=pk)
        stock.is_deleted = True
        stock.save()
        messages.success(request, self.success_message)
        return redirect('history')


class StockUpdateView(View):
    model = StockHistory
    form_class = StockHistoryForm
    template_name = 'update_stock.html'
    success_url = '/inventory'
    success_message = "Data stok berhasil ditambah"
    msg = "Data stok gagal ditambahkan"
    errq = "Tidak dapat menambahkan barang buruk, karena stok masih kosong"
    
    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        context = {
            'title'    : 'Tambah Data Stok',
            'savebtn'      : 'Tambah Data',
            'delbtn'    : 'Hapus Stok',
            'form'      : self.form_class, 
            'object'     : stock,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = self.form_class(request.POST) 
        prim = request.POST['stock']
        stock = get_object_or_404(Stock, pk=prim)
        
        stt = request.POST['stat']
        qty = int(request.POST['quantity'])
        if form.is_valid():
            if stt == "Buruk":
                stock.good_qty -= qty 
                if stock.good_qty<=0:
                    context = {
                        'title'    : 'Tambah Data Stok',
                        'savebtn'      : 'Tambah Data',
                        'delbtn'    : 'Hapus Stok',
                        'form'      : form,
                        'object'     : stock,
                    }
                    messages.info(request, self.errq)
                    return render(request, self.template_name, context)
                stock.bad_qty += qty 
            else:
                stock.good_qty += qty 
            form.save()
            stock.save()
            messages.success(request, self.success_message)
            return redirect('inventory')
        
        context = {
            'title'    : 'Tambah Data Stok',
            'savebtn'      : 'Tambah Data',
            'delbtn'    : 'Hapus Stok',
            'form'      : form,
            'object'     : stock,
        }
        messages.info(request, self.msg)
        return render(request, self.template_name, context)


class StockUpView(View):
    model = StockHistory
    form_class = StockHistoryForm
    template_name = 'update_stock.html'
    success_url = '/inventory'
    success_message = "Data stok berhasil ditambah"
    msg = "Data stok gagal ditambahkan"
    errq = "Tidak dapat menambahkan barang buruk, karena stok masih kosong"
    
    def get(self, request):
        context = {
            'title'    : 'Tambah Data Stok',
            'savebtn'      : 'Tambah Data',
            'delbtn'    : 'Hapus Stok',
            'form'      : self.form_class, 
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST) 
        prim = request.POST['stock']
        stock = get_object_or_404(Stock, pk=prim)
        
        stt = request.POST['stat']
        qty = int(request.POST['quantity'])
        if form.is_valid():
            if stt == "Buruk":
                stock.good_qty -= qty 
                if stock.good_qty<=0:
                    context = {
                        'title'    : 'Tambah Data Stok',
                        'savebtn'      : 'Tambah Data',
                        'delbtn'    : 'Hapus Stok',
                        'form'      : form,
                        'object'     : stock,
                    }
                    messages.info(request, self.errq)
                    return render(request, self.template_name, context)
                stock.bad_qty += qty 
            else:
                stock.good_qty += qty 
            form.save()
            stock.save()
            messages.success(request, self.success_message)
            return redirect('inventory')
        
        context = {
            'title'    : 'Tambah Data Stok',
            'savebtn'      : 'Tambah Data',
            'delbtn'    : 'Hapus Stok',
            'form'      : form,
            'object'     : stock,
        }
        messages.info(request, self.msg)
        return render(request, self.template_name, context)


class StockHistoryView(FilterView):
    filterset_class = StockHistoryFilter
    queryset = StockHistory.objects.filter(is_deleted=False)
    template_name = 'history.html'
    ordering = ['-time']
    paginate_by = 10
