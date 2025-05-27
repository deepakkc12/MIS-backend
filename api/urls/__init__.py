from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', include('api.urls.auth')),
    path('', include('api.urls.dashboard')),
    path('', include('api.urls.PriceRevisions')),
    path('', include('api.urls.crm')),
    path('', include('api.urls.general')),
    path('', include('api.urls.sales')),
    path('', include('api.urls.barcodes')),
    path('acc/', include('api.urls.Accountings')),
    path('', include('api.urls.Inventory')),
    path('', include('api.urls.salesLoss')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
