from datetime import datetime
from rest_framework.views import APIView
from ..services.PriceRevision.Reports import PriceRevisionReports

from ..utils.response import ResponseHandler
from ..services.Dashboard.Reports import DashBoard
from ..utils.decorators import token_required

class GetPriceRevisions(APIView):
    def get(Self,request):
        start_date = request.GET.get('startDate')
        end_date = request.GET.get('endDate')

        if not start_date or not end_date:
            return ResponseHandler.bad_request("Start date and end date are required")

        result = PriceRevisionReports.list(start_date=start_date,end_date=end_date)

        return ResponseHandler.success(data=result)



