from datetime import datetime
from rest_framework.views import APIView
from ..services.Sales.Sales import SalesServices
from ..services.CRM.PriorityCustomers import PriorityCustomers

from ..utils.response import ResponseHandler
from ..services.Dashboard.Reports import DashBoard
from ..utils.decorators import token_required


class DailySalesChart(APIView):
    def get(self,request):

        type = request.GET.get('type')

        date_range = request.GET.get("range",7)

        if not date_range:
            return ResponseHandler.success("range required")



        result = SalesServices.get_day_wise_sales(date_range=int(date_range))

        return ResponseHandler.success(data=result)
    
class MonthlySalesChart(APIView):
    def get(self,request):
        year = request.GET.get("year",2025)


        result = SalesServices.get_monthly_sales(year=year)

        return ResponseHandler.success(data=result)

class YearlySalesChart(APIView):

    def get(Self,request):

        result = SalesServices.get_yearly_sales()

        return ResponseHandler.success(data=result)
    


        
class GetSalsVsOpex(APIView):
    def get(self,request):
        result = SalesServices.get_last_2_month_sales_vs_opex()

        return ResponseHandler.success(data=result)
    
    
class GetSalesTargets(APIView):
    def get(self,request):
        result = SalesServices.get_sales_target()

        return ResponseHandler.success(data=result)