from django.urls import path
from ..view.Sales import DailySalesChart,MonthlySalesChart,YearlySalesChart,GetSalsVsOpex,GetSalesTargets

urlpatterns = [
    path('sales/day-wise/', DailySalesChart.as_view(), name='sales-daily-wise-sales-chart'),
    path('sales/targets/', GetSalesTargets.as_view(), name='sales-daily-wise-sales-chart'),
    path('sales/month-wise/', MonthlySalesChart.as_view(), name='sales-month-wise-sales-chart'),
    path('sales/year-wise/', YearlySalesChart.as_view(), name='sales-year-wise-sales-chart'),
    path('sales/opex-comparison/', GetSalsVsOpex.as_view(), name='sales-year-wise-sales-chart'),
]