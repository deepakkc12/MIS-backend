from django.urls import path
from ..view.salesLoss import (
   GetSalesLossSummery,GetActiveStockouts
)

urlpatterns = [
    path("sales-loss/summery/", GetSalesLossSummery.as_view(), name="sales-loss-summery"),
    path("stock/active/", GetActiveStockouts.as_view(), name="sales-loss-summery"),
]