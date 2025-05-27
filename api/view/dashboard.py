from datetime import datetime
from rest_framework.views import APIView
from ..services.CRM.Customers import CRM

from ..utils.response import ResponseHandler
from ..services.Dashboard.Reports import DashBoard
from ..utils.decorators import token_required
from ..services.Settings.Settings import Settings


class GetSalesDetails(APIView):
    def get(Self,request):
        
        sales_datails = DashBoard.get_profit_details()

        result = sales_datails

        total_customers = CRM.get_totla_customers()

        result["TotalCustomers"] = total_customers

        return ResponseHandler.success(data=result)
    
class LastUpdatedDate(APIView):
    def get(self,request):
        
        date = Settings.last_updated

        return ResponseHandler.success(data=date)
