from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View, 
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django_filters.views import FilterView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
    PurchaseBill, 
    Supplier, 
    Customer, 
    SupDebtHistory,
    CusDebtHistory,
    PurchaseItem,
    PurchaseBillDetails,
    SaleBill,  
    SaleItem,
    SaleBillDetails
)
from .forms import (
    SelectSupplierForm, 
    SelectCustomerForm, 
    SupDebtHistoryForm,
    CusDebtHistoryForm,
    PurchaseItemFormset,
    PurchaseDetailsForm, 
    SupplierForm, 
    CustomerForm, 
    SaleItemFormset,
    SaleDetailsForm
)
from inventory.models import Stock
from .filters import SupDebtHistoryFilter
from .filters import CusDebtHistoryFilter
import time
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import make_aware
from django.db.models import Sum

class SupplierListView(ListView):
    model = Supplier
    template_name = "suppliers/suppliers_list.html"
    queryset = Supplier.objects.filter(is_deleted=False)
    paginate_by = 10


class CustomerListView(ListView):
    model = Customer
    template_name = "customers/customers_list.html"
    queryset = Customer.objects.filter(is_deleted=False)
    paginate_by = 10


class SupplierCreateView(SuccessMessageMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/transactions/suppliers'
    success_message = "Supplier berhasil ditambahkan"
    template_name = "suppliers/edit_supplier.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Supplier Baru'
        context["savebtn"] = 'Tambah Supplier'
        return context     


class CustomerCreateView(SuccessMessageMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    success_url = '/transactions/customers'
    success_message = "Pembeli berhasil ditambahkan"
    template_name = "customers/edit_customer.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Pembeli Baru'
        context["savebtn"] = 'Tambah Pembeli'
        return context     


class SupplierUpdateView(SuccessMessageMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/transactions/suppliers'
    success_message = "Detil supplier berhasil diperbarui"
    template_name = "suppliers/edit_supplier.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Ubah Supplier'
        context["savebtn"] = 'Simpan Perubahan'
        context["delbtn"] = 'Hapus Supplier'
        return context


class CustomerUpdateView(SuccessMessageMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    success_url = '/transactions/customers'
    success_message = "Detil pembeli berhasil diperbarui"
    template_name = "customers/edit_customer.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Ubah Pembeli'
        context["savebtn"] = 'Simpan Perubahan'
        context["delbtn"] = 'Hapus Pembeli'
        return context


class SupplierDeleteView(View):
    template_name = "suppliers/delete_supplier.html"
    success_message = "Supplier berhasil dihapus"

    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        return render(request, self.template_name, {'object' : supplier})

    def post(self, request, pk):  
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.is_deleted = True
        supplier.save()                                               
        messages.success(request, self.success_message)
        return redirect('suppliers-list')


class CustomerDeleteView(View):
    template_name = "customers/delete_customer.html"
    success_message = "Pembeli berhasil dihapus"

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        return render(request, self.template_name, {'object' : customer})

    def post(self, request, pk):  
        customer = get_object_or_404(Customer, pk=pk)
        customer.is_deleted = True
        customer.save()                                               
        messages.success(request, self.success_message)
        return redirect('customers-list')


class SupplierView(View):
    def get(self, request, name):
        supplierobj = get_object_or_404(Supplier, name=name)
        bill_list = PurchaseBill.objects.filter(supplier=supplierobj).order_by('-time')
        page = request.GET.get('page', 1)
        paginator = Paginator(bill_list, 10)
        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)
        context = {
            'supplier'  : supplierobj,
            'bills'     : bills
        }
        return render(request, 'suppliers/supplier.html', context)


class CustomerView(View):
    def get(self, request, name):
        customerobj = get_object_or_404(Customer, name=name)
        bill_list = SaleBill.objects.filter(customer=customerobj).order_by('-time')
        page = request.GET.get('page', 1)
        paginator = Paginator(bill_list, 10)
        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)
        context = {
            'customer'  : customerobj,
            'bills'     : bills
        }
        return render(request, 'customers/customer.html', context)


class SupDebtPaymentView(View):
    model = SupDebtHistory
    form_class = SupDebtHistoryForm
    template_name = 'suppliers/debt_payment.html'
    success_url = '/bill/sup_debt_bill'
    success_message = "Data pelunasan berhasil ditambah"
    msg = "Data pelunasan gagal ditambahkan"
    
    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        context = {
            'title'    : 'Tambah Pelunasan Hutang',
            'savebtn'      : 'Tambah Pelunasan',
            'delbtn'    : 'Hapus Pelunasan',
            'form'      : self.form_class, 
            'object'     : supplier,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = self.form_class(request.POST) 
        prim = request.POST['subject']
        supplier = get_object_or_404(Supplier, pk=prim)
        
        qty = int(request.POST['amount'])
        if form.is_valid():
            supplier.t_debt -= qty 
            if supplier.t_debt<0:
                supplier.t_debt=0;
            np = form.save()
            supplier.save()
            messages.success(request, self.success_message)
            return redirect('sup-debt-bill', pk=np.pk)
        
        context = {
            'title'    : 'Tambah Pelunasan Hutang',
            'savebtn'      : 'Tambah Pelunasan',
            'delbtn'    : 'Hapus Pelunasan',
            'form'      : form,
            'object'     : supplier,
        }
        messages.info(request, self.msg)
        return render(request, self.template_name, context)


class CusDebtPaymentView(View):
    model = CusDebtHistory
    form_class = CusDebtHistoryForm
    template_name = 'customers/debt_payment.html'
    success_url = '/bill/cus_debt_bill'
    success_message = "Data pelunasan berhasil ditambah"
    msg = "Data pelunasan gagal ditambahkan"
    
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        context = {
            'title'    : 'Tambah Pelunasan Hutang ke Supplier',
            'savebtn'      : 'Tambah Pelunasan',
            'delbtn'    : 'Hapus Pelunasan',
            'form'      : self.form_class, 
            'object'     : customer,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = self.form_class(request.POST) 
        prim = request.POST['subject']
        customer = get_object_or_404(Customer, pk=prim)
        
        qty = int(request.POST['amount'])
        if form.is_valid():
            customer.t_debt -= qty 
            if customer.t_debt<0:
                customer.t_debt=0;
            np = form.save()
            customer.save()
            messages.success(request, self.success_message)
            return redirect('cus-debt-bill', pk=np.pk)
        
        context = {
            'title'    : 'Tambah Pelunasan Hutang dari Pembeli',
            'savebtn'      : 'Tambah Pelunasan',
            'delbtn'    : 'Hapus Pelunasan',
            'form'      : form,
            'object'     : customer,
        }
        messages.info(request, self.msg)
        return render(request, self.template_name, context)


class SupDebtHistoryView(FilterView):
    filterset_class = SupDebtHistoryFilter
    queryset = SupDebtHistory.objects.filter(is_deleted=False)
    template_name = 'suppliers/debt_history.html'
    ordering = ['-time']
    paginate_by = 10


class CusDebtHistoryView(FilterView):
    filterset_class = CusDebtHistoryFilter
    queryset = CusDebtHistory.objects.filter(is_deleted=False)
    template_name = 'customers/debt_history.html'
    ordering = ['-time']
    paginate_by = 10


class SupDebtHistoryDeleteView(View):
    template_name = "suppliers/delete_debt.html"
    success_message = "Riwayat pelunasan hutang berhasil dihapus"
    
    def get(self, request, pk):
        supplier = get_object_or_404(SupDebtHistory, pk=pk)
        return render(request, self.template_name, {'object' : supplier})

    def post(self, request, pk):  
        supplier = get_object_or_404(SupDebtHistory, pk=pk)
        supplier.is_deleted = True
        supplier.save()
        messages.success(request, self.success_message)
        return redirect('supdebt-history')


class CusDebtHistoryDeleteView(View):
    template_name = "customers/delete_debt.html"
    success_message = "Riwayat pelunasan hutang berhasil dihapus"
    
    def get(self, request, pk):
        customer = get_object_or_404(CusDebtHistory, pk=pk)
        return render(request, self.template_name, {'object' : customer})

    def post(self, request, pk):  
        customer = get_object_or_404(CusDebtHistory, pk=pk)
        customer.is_deleted = True
        customer.save()
        messages.success(request, self.success_message)
        return redirect('cusdebt-history')


class PurchaseView(ListView):
    model = PurchaseBill
    template_name = "purchases/purchases_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10


class SelectSupplierView(View):
    form_class = SelectSupplierForm
    template_name = 'purchases/select_supplier.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            supplierid = request.POST.get("supplier")
            supplier = get_object_or_404(Supplier, id=supplierid)
            return redirect('new-purchase', supplier.pk)
        return render(request, self.template_name, {'form': form})


class SelectCustomerView(View):
    form_class = SelectCustomerForm
    template_name = 'sales/select_customer.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            customerid = request.POST.get("customer")
            customer = get_object_or_404(Customer, id=customerid)
            return redirect('new-sale', customer.pk)
        return render(request, self.template_name, {'form': form})


class PurchaseCreateView(View):                                                 
    template_name = 'purchases/new_purchase.html'

    def get(self, request, pk):
        formset = PurchaseItemFormset(request.GET or None)
        supplierobj = get_object_or_404(Supplier, pk=pk)
        context = {
            'formset'   : formset,
            'supplier'  : supplierobj,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        formset = PurchaseItemFormset(request.POST)
        supplierobj = get_object_or_404(Supplier, pk=pk)
        if formset.is_valid():
            
            billobj = PurchaseBill(supplier=supplierobj)
            billobj.save()
            
            billdetailsobj = PurchaseBillDetails(billno=billobj)
            billdetailsobj.save()
            for form in formset:
                
                billitem = form.save(commit=False)
                billitem.billno = billobj
                
                stock = get_object_or_404(Stock, name=billitem.stock.name, grade=billitem.stock.grade, is_deleted=False)
                
                billitem.totalprice = billitem.perprice * billitem.quantity
                
                stock.good_qty += billitem.quantity
                
                stock.save()
                billitem.save()
            messages.success(request, "Informasi barang yang dibeli berhasil disimpan")
            return redirect('purchase-bill', billno=billobj.billno)
        formset = PurchaseItemFormset(request.GET or None)
        context = {
            'formset'   : formset,
            'supplier'  : supplierobj
        }
        return render(request, self.template_name, context)


class PurchaseDeleteView(SuccessMessageMixin, DeleteView):
    model = PurchaseBill
    template_name = "purchases/delete_purchase.html"
    success_url = '/transactions/purchases'
    success_message = "Nota pembelian berhasil dihapus"
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = PurchaseItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity -= item.quantity
                stock.save()
        messages.success(request, self.success_message)
        return super(PurchaseDeleteView, self).delete(*args, **kwargs)




class SaleView(ListView):
    model = SaleBill
    template_name = "sales/sales_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10


class SaleCreateView(View):                                                      
    template_name = 'sales/new_sale.html'
    errq = "Jumlah penjualan melebihi stok yang tersedia"
    def get(self, request, pk):
        formset = SaleItemFormset(request.GET or None)
        customerobj = get_object_or_404(Customer, pk=pk)
        stocks = Stock.objects.filter(is_deleted=False)
        context = {
            'formset'   : formset,
            'customer'  : customerobj,
            'stocks'    : stocks
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        formset = SaleItemFormset(request.POST)
        customerobj = get_object_or_404(Customer, pk=pk)
        if formset.is_valid(): 
            
            billobj = SaleBill(customer=customerobj)
            billobj.save()
            
            billdetailsobj = SaleBillDetails(billno=billobj)
            billdetailsobj.save()
            for form in formset:
                
                billitem = form.save(commit=False)
                billitem.billno = billobj
                con = billitem.condition
                stock = get_object_or_404(Stock, name=billitem.stock.name, grade=billitem.stock.grade, is_deleted=False)      
                
                billitem.totalprice = billitem.perprice * billitem.quantity
                if con == 'Standar':
                    stock.good_qty -= billitem.quantity
                else:
                    stock.bad_qty -= billitem.quantity
                stock.save()
                billitem.save()
            messages.success(request, "Informasi barang yang dijual berhasil disimpan")
            return redirect('sale-bill', billno=billobj.billno)
        formset = SaleItemFormset(request.GET or None)
        context = {
            'formset'   : formset,
            'customer'  : customerobj,
        }
        return render(request, self.template_name, context)


class SaleDeleteView(SuccessMessageMixin, DeleteView):
    model = SaleBill
    template_name = "sales/delete_sale.html"
    success_url = '/transactions/sales'
    success_message = "Nota penjualan berhasil dihapus"
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = SaleItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity += item.quantity
                stock.save()
        messages.success(request, self.success_message)
        return super(SaleDeleteView, self).delete(*args, **kwargs)



class PurchaseBillView(View):
    model = PurchaseBill
    template_name = "bill/purchase_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        context = {
            'bill'          : PurchaseBill.objects.get(billno=billno),
            'items'         : PurchaseItem.objects.filter(billno=billno),
            'billdetails'   : PurchaseBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = PurchaseDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = PurchaseBillDetails.objects.get(billno=billno)
            bill = PurchaseBill.objects.get(billno=billno)
            billobj = PurchaseBill(billno=billno)
            supplierobj = get_object_or_404(Supplier, name=bill.supplier)
            debt = int(request.POST.get("debt"))
            if debt>0:
                supplierobj.t_debt+=debt
                supplierobj.save()
            billdetailsobj.ppn = request.POST.get("ppn")    
            billdetailsobj.paid = request.POST.get("paid")
            billdetailsobj.stat = request.POST.get("stat")
            billdetailsobj.retur = request.POST.get("retur")
            billdetailsobj.debt = request.POST.get("debt")
            billdetailsobj.total = request.POST.get("total")

            billdetailsobj.save()
            messages.success(request, "Detil nota pembelian berhasil diubah")
        context = {
            'bill'          : PurchaseBill.objects.get(billno=billno),
            'items'         : PurchaseItem.objects.filter(billno=billno),
            'billdetails'   : PurchaseBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)


class SaleBillView(View):
    model = SaleBill
    template_name = "bill/sale_bill.html"
    bill_base = "bill/bill_base.html"
    
    def get(self, request, billno):
        context = {
            'bill'          : SaleBill.objects.get(billno=billno),
            'items'         : SaleItem.objects.filter(billno=billno),
            'billdetails'   : SaleBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = SaleDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = SaleBillDetails.objects.get(billno=billno)
            bill = SaleBill.objects.get(billno=billno)
            billobj = SaleBill(billno=billno)
            customerobj = get_object_or_404(Customer, name=bill.customer)
            debt = int(request.POST.get("debt"))
            if debt>0:
                customerobj.t_debt+=debt
                customerobj.save()
            billdetailsobj.ppn = request.POST.get("ppn")    
            billdetailsobj.paid = request.POST.get("paid")
            billdetailsobj.stat = request.POST.get("stat")
            billdetailsobj.retur = request.POST.get("retur")
            billdetailsobj.debt = request.POST.get("debt")
            billdetailsobj.total = request.POST.get("total")

            billdetailsobj.save()
            messages.success(request, "Detil nota penjualan berhasil diubah")
        context = {
            'bill'          : SaleBill.objects.get(billno=billno),
            'items'         : SaleItem.objects.filter(billno=billno),
            'billdetails'   : SaleBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)


class CusDebtBillView(View):
    template_name = "bill/cus_debt_bill.html"
    bill_base = "bill/bill_base.html"
    def get(self, request, pk):
        context = {
            'bill'          : CusDebtHistory.objects.get(pk=pk),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

class SupDebtBillView(View):
    template_name = "bill/sup_debt_bill.html"
    bill_base = "bill/bill_base.html"
    def get(self, request, pk):
        context = {
            'bill'          : SupDebtHistory.objects.get(pk=pk),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)
