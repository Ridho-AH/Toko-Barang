from django.urls import path
from django.urls import include, re_path
from . import views

urlpatterns = [
    path('suppliers/', views.SupplierListView.as_view(), name='suppliers-list'),
    path('suppliers/new', views.SupplierCreateView.as_view(), name='new-supplier'),
    path('suppliers/debt_history', views.SupDebtHistoryView.as_view(), name='supdebt-history'),
    path('suppliers/<pk>/edit', views.SupplierUpdateView.as_view(), name='edit-supplier'),
    path('suppliers/<pk>/delete', views.SupplierDeleteView.as_view(), name='delete-supplier'),
    path('suppliers/<name>', views.SupplierView.as_view(), name='supplier'),
    path('suppliers/<pk>/delete_debt', views.SupDebtHistoryDeleteView.as_view(), name='delete-supdebthistory'),
    path('suppliers/<pk>/debt_payment', views.SupDebtPaymentView.as_view(), name='supdebt-payment'),
    
    path('customers/', views.CustomerListView.as_view(), name='customers-list'),
    path('customers/new', views.CustomerCreateView.as_view(), name='new-customer'),
    path('customers/debt_history', views.CusDebtHistoryView.as_view(), name='cusdebt-history'),
    path('customers/<pk>/edit', views.CustomerUpdateView.as_view(), name='edit-customer'),
    path('customers/<pk>/delete', views.CustomerDeleteView.as_view(), name='delete-customer'),
    path('customers/<name>', views.CustomerView.as_view(), name='customer'),
    path('customers/<pk>/delete_debt', views.CusDebtHistoryDeleteView.as_view(), name='delete-cusdebthistory'),
    path('customers/<pk>/debt_payment', views.CusDebtPaymentView.as_view(), name='cusdebt-payment'),

    path('purchases/', views.PurchaseView.as_view(), name='purchases-list'), 
    path('purchases/new', views.SelectSupplierView.as_view(), name='select-supplier'), 
    path('purchases/new/<pk>', views.PurchaseCreateView.as_view(), name='new-purchase'),    
    path('purchases/<pk>/delete', views.PurchaseDeleteView.as_view(), name='delete-purchase'),
    
    path('sales/', views.SaleView.as_view(), name='sales-list'),
    path('sales/new', views.SelectCustomerView.as_view(), name='select-customer'), 
    path('sales/new/<pk>', views.SaleCreateView.as_view(), name='new-sale'),
    path('sales/<pk>/delete', views.SaleDeleteView.as_view(), name='delete-sale'),

    path("purchases/<billno>", views.PurchaseBillView.as_view(), name="purchase-bill"),
    path("sales/<billno>", views.SaleBillView.as_view(), name="sale-bill"),
    path("cus_debt_pay/<pk>", views.CusDebtBillView.as_view(), name="cus-debt-bill"),
    path("sup_debt_pay/<pk>", views.SupDebtBillView.as_view(), name="sup-debt-bill"),
]