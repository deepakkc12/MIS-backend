from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', include('MIS.api.urls.auth')),
    path('', include('MIS.api.urls.dashboard')),
    path('', include('MIS.api.urls.PriceRevisions')),
    path('', include('MIS.api.urls.crm')),
    path('', include('MIS.api.urls.general')),
    path('', include('MIS.api.urls.sales')),
    path('', include('MIS.api.urls.barcodes')),
    path('acc/', include('MIS.api.urls.Accountings')),
    path('', include('MIS.api.urls.Inventory')),
    path('', include('MIS.api.urls.salesLoss')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
