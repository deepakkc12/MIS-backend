from django.urls import path
from ..view.Crm import CRMMatrices,PriorityCustomersList,CustomerDetails,CustomerSalesList,CrmSegmentMetricsData,CustomerRankings,FrequentCustomersList,NonPerformingCustomersList,CustomerVD,CustomerSalesTrend,FrequentVIsitorsList,InactiveCustomersList,CRankings,LiveCustomerList,GETTOPPriorityCustomers,GEtNewMonthCustomers

urlpatterns = [

    path('crm/metrics/', CRMMatrices.as_view(), name='crm-matrices'),
    path('crm/pr-customers-list/', PriorityCustomersList.as_view(), name='priority-customers-list'),
    path('crm/inactive-customers-list/', InactiveCustomersList.as_view(), name='incative-customers-list'),
    path('crm/frequent-customers-list/', FrequentVIsitorsList.as_view(), name='frequent-customers-list'),
    path('crm/customer-details/', CustomerDetails.as_view(), name='customer-details'),
    path('crm/customer-sales-list/', CustomerSalesList.as_view(), name='customer-sales-details'),
    path('crm/segment-metrics/', CrmSegmentMetricsData.as_view(), name='segment-metrics-data'),
    path('crm/rankings/', CustomerRankings.as_view(), name='Customer-ranking-list'),
    path('crm/frequent-visitors-list/', FrequentCustomersList.as_view(), name='frequent-visitors-list'),
    path('crm/npc-list/', NonPerformingCustomersList.as_view(), name='non-performing-visitors-list'),
    path('crm/cvd/', CustomerVD.as_view(), name='customer-value-distribution'),
    path('crm/sales-trend/', CustomerSalesTrend.as_view(), name='customer-sales-trend'),
    path('crm/live-levels/', CRankings.as_view(), name='rankings'),
    path('crm/live-customer-list/', LiveCustomerList.as_view(), name='rankings'),
    path('crm/top-priors/', GETTOPPriorityCustomers.as_view(), name='rankings'),
    path('crm/new-month-customers/', GEtNewMonthCustomers.as_view(), name='rankings'),

]