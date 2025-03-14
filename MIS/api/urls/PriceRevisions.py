from django.urls import path
from ..view.PriceRevisions import GetPriceRevisions
urlpatterns = [
    path('price-revisions/', GetPriceRevisions.as_view(), name='price-revision-reports'),

]
