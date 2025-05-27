from datetime import datetime
from rest_framework.views import APIView

from ..services.TypedBarcodes.BrowsedEANitems import BrowsedEanItems
from ..services.TypedBarcodes.BrowsedPrivateLabels import BrowsedPrivateLabels
from ..services.TypedBarcodes.BrowsedRepackItems import BrowsedRepackItems
from ..services.TypedBarcodes.ManualEntryBarcodes import ManuallyEnteredBArcodes
from ..services.TypedBarcodes.UnregisteredEans import UnregisteredEans


from ..utils.response import ResponseHandler



class GetTYpedBarcodeMetrics(APIView):
    def get(self,requset):

        result = {
            "eanItems":0,
            "privateLabels":0,
            "repackItems":0,
            'manuallyEntryBarcodes':0,
            'UnregisteredEans':0
        }

        result["eanItems"]=BrowsedEanItems.count()
        result["manuallyEntryBarcodes"] = ManuallyEnteredBArcodes.count()
        result["privateLabels"] = BrowsedPrivateLabels.count()
        result["repackItems"] = BrowsedRepackItems.count()
        result["UnregisteredEans"] = UnregisteredEans.count()

        return ResponseHandler.success(data=result)
    
class GetBrowsedEanItems(APIView):
    def get(self,request):
        result = BrowsedEanItems.list()
        return ResponseHandler.success(data=result)
    
class GetManuallyEnteredBArcodes(APIView):
    def get(self,request):
        result = ManuallyEnteredBArcodes.list()
        return ResponseHandler.success(data=result)
    
class GetBrowsedPrivateLabels(APIView):
    def get(self,request):
        result = BrowsedPrivateLabels.list()
        return ResponseHandler.success(data=result)
    
class GetBrowsedRepackItems(APIView):
    def get(self,request):
        result = BrowsedRepackItems.list()
        return ResponseHandler.success(data=result)

class GetUnregisteredEans(APIView):
    def get(self,request):
        result = UnregisteredEans.list()
        return ResponseHandler.success(data=result)



