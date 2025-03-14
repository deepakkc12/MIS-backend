from datetime import datetime
from rest_framework.views import APIView
from ..services.Settings.Settings import Settings


from ..services.CRM.InactiveCustomers import InActiveCustomers

from ..utils.response import ResponseHandler

from ..utils.decorators import token_required


class GetSettings(APIView):
    def get(self,request):
        lastUpdated = Settings.last_updated

        return ResponseHandler.success({'lastUpdated':lastUpdated})