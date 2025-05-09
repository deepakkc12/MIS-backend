from datetime import datetime
from rest_framework.views import APIView
from ..services.Sales.Sales import SalesServices
from ..services.CRM.PriorityCustomers import PriorityCustomers

from ..utils.response import ResponseHandler
from ..services.SalesLoss.Reports import SalesLossReports
from ..services.Dashboard.Reports import DashBoard
from ..utils.decorators import token_required

class GetSalesLossSummery(APIView):
    def get(self,request):

        summery = SalesLossReports.summery()

        return ResponseHandler.success(data=summery)
    
class GetActiveStockouts(APIView):
    def get(self,requst):

        list = SalesLossReports.current_zero_stock_items()

        return ResponseHandler.success(data=list)
    


        
