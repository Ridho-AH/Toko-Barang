from django.shortcuts import render
from django.views.generic import View, TemplateView
from inventory.models import Stock
from transactions.models import SaleBill, PurchaseBill
from django.db.models import Sum
from django.template import loader

class HomeView(View):
    template_name = "home.html"
    def get(self, request):        
        labels = []
        data = []
        labels2 = []
        data2 = []
        
        stockqueryset = Stock.objects.filter(is_deleted=False).annotate(qty=Sum('good_qty')).order_by('name')
        for item in stockqueryset:
            nm = item.name
            gd = item.grade
            lb = nm+"_"+gd
            labels.append(lb)
            data.append(item.qty)
        stockqueryset2 = Stock.objects.filter(is_deleted=False).annotate(qty=Sum('bad_qty')).order_by('name')
        for item in stockqueryset2:
            bn = item.name+"_buruk"
            labels2.append(bn)
            data2.append(item.qty)
        sales = SaleBill.objects.order_by('-time')[:3]
        purchases = PurchaseBill.objects.order_by('-time')[:3]
        context = {
            'labels'    : labels,
            'data'      : data,
            'labels2'    : labels2,
            'data2'      : data2,
            'sales'     : sales,
            'purchases' : purchases,
        }
        return render(request, self.template_name, context)

class GuideView(TemplateView):
    template_name = "guide.html"