from datetime import datetime
from rest_framework.views import APIView
from ..services.CRM.Customers import CRM,Customers
from ..services.CRM.PriorityCustomers import PriorityCustomers
from ..services.CRM.ActiveCustomers import ActiveCustomers
from ..services.CRM.Npc import NonPerformingCustomers
from ..services.CRM.Ranking import RankedCustomers
from ..services.CRM.FrequentVisitors import FrequentVisitors
from ..services.CRM.LiveCustomers import LiveCustomers

from ..services.CRM.InactiveCustomers import InActiveCustomers

from ..utils.response import ResponseHandler
from ..services.Dashboard.Reports import DashBoard
from ..utils.decorators import token_required


class CRMMatrices(APIView):
    def get(self,request):
        result = CRM.matrices_data()

        return ResponseHandler.success(data=result)
    

class PriorityCustomersList(APIView):
    def get(self,request):
        start_date = request.GET.get("startDate",1)

        start_date = int(start_date)
        result = PriorityCustomers.list(start_date=start_date)

        return ResponseHandler.success(data=result)
    
class CustomerDetails(APIView):
    def get(Self,request):
        customer_code = request.GET.get("code")

        if not customer_code:
            return ResponseHandler.bad_request("code required")

        details = CRM.customer_details(customer_code=customer_code)

        return ResponseHandler.success(data=details)
    
class CustomerSalesList(APIView):
    def get(Salef,request):
        customer_code = request.GET.get("customerCode")

        if not customer_code:
            return ResponseHandler.bad_request()
        
        customer = Customers.find_by_id(id=customer_code)

        if not customer:
            return ResponseHandler.not_found("Customer not found")
        
        sales_list = CRM.sales_list(customer=customer)

        return ResponseHandler.success(data=sales_list)
    
class CustomerMonthWiseSales(APIView):
    def get(self,request):
        year = request.GET.get('year')
        customer_code = request.GET.get('customer')

        if not customer_code:
            pass
        customer = Customers.find_by_id(id=customer_code)

        if not customer:
            return ResponseHandler.not_found("Customer not found")
        

class CrmSegmentMetricsData(APIView):
    def get(self,request):
        priority_customers = PriorityCustomers.count()
        frequent_visitors = FrequentVisitors.count()
        npc_customers = NonPerformingCustomers.count()
        inactive_customers = InActiveCustomers.count()

        result = {
            'priorityCustomers': priority_customers,
            'frequentVisitors': frequent_visitors,
            'npcCustomers': npc_customers,
            'inactiveCustomers': inactive_customers,
        }

        return ResponseHandler.success(data=result)
    


class CustomerRankings(APIView):
    def get(self,request):
        result = RankedCustomers.list()
        return ResponseHandler.success(data=result)
    


class FrequentCustomersList(APIView):

    def get(self,request):

        result = FrequentVisitors.list()

        return ResponseHandler.success(data=result)

class NonPerformingCustomersList(APIView):

    def get(Self,request):

        result = NonPerformingCustomers.list()

        return ResponseHandler.success(data=result)
    

class CustomerVD(APIView):
    def get(Self,request):
        result = CRM.value_distribution()
        return ResponseHandler.success(data=result)
    
class CustomerSalesTrend(APIView):
    def get(Self,request):

        result = CRM.sales_trend()

        return ResponseHandler.success(data=result)
    

class FrequentVIsitorsList(APIView):
    def get(self,request):
        result = FrequentVisitors.list()

        return ResponseHandler.success(data=result)
    
class InactiveCustomersList(APIView):
    def get(self,request):
        result = InActiveCustomers.list()

        return ResponseHandler.success(data=result)
    

    
    
class CRankings(APIView):

    def get(Self,request):
        result = LiveCustomers.levels()

        return ResponseHandler.success(data=result)
    




