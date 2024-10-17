from django.urls import path
from django.urls import include, re_path
from . import views

urlpatterns = [
    path('', views.StockListView.as_view(), name='inventory'),
    path('new', views.StockCreateView.as_view(), name='new-stock'),
    path('stock/<pk>/edit', views.StockEditView.as_view(), name='edit-stock'),
    path('stock/<pk>/delete', views.StockDeleteView.as_view(), name='delete-stock'),
    path('stock/<pk>/deletehist', views.StockHistoryDeleteView.as_view(), name='delete-stockhistory'),
    path('stock/<pk>/update', views.StockUpdateView.as_view(), name='update-stock'),
    path('stock/update', views.StockUpView.as_view(), name='up-stock'),
    path('history', views.StockHistoryView.as_view(), name='history'),
]