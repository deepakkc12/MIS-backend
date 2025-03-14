from datetime import datetime
from rest_framework.views import APIView

from ..services.TypedBarcodes.BrowsedEANitems import BrowsedEanItems
from ..services.TypedBarcodes.BrowsedPrivateLabels import BrowsedPrivateLabels
from ..services.TypedBarcodes.BrowsedRepackItems import BrowsedRepackItems
from ..services.TypedBarcodes.ManualEntryBarcodes import ManuallyEnteredBArcodes
from ..services.TypedBarcodes.UnregisteredEans import UnregisteredEans


from ..utils.response import ResponseHandler



class GetTYpedBarcodeMAtrics(APIView):
    def get(self,requset):

        result = {
            "eanItems":0,
            "privateLabels":0,
            "repackItems":0,
            'manuallyEntryBarcodes':0,
            'UnregisteredEans':0
        }

        result["eanItems"]=



