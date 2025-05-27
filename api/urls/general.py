from django.urls import path
from ..view.general import ( DbTableData,)
from ..view.setttings import GetSettings

urlpatterns = [
    path('dbtable/', DbTableData.as_view(), name='db-tabledata'),
    path('settings/', GetSettings.as_view(), name='db-tabledata'),


]