from django.urls import path
from ..view.dashboard import GetSalesDetails,LastUpdatedDate

urlpatterns = [
    path('dashboard/sales-summery/', GetSalesDetails.as_view(), name='sales-total-summery'),
    path('dashboard/last-updated-date/', LastUpdatedDate.as_view(), name='sales-total-summery'),


]
