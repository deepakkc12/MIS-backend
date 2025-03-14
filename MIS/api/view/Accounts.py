from datetime import datetime
from rest_framework.views import APIView
from ..services.Accountings.crNoteCashRefund import CrNoteCashRefund
from ..services.Accountings.RangeException import AccAuditRange
from ..services.Accountings.ExpenseAsIncome import ExpenseAsIncome
from ..utils.response import ResponseHandler
from ..services.Accountings.BackDatedEntries import BackDatedEntries


class GetAccountMatrics(APIView):
    def get(self, request):
        date_range = request.GET.get('range', 7)

        total_refund = CrNoteCashRefund.get_total_amount(range=date_range)
        total_refund_entries = CrNoteCashRefund.count(range=date_range)

        range_exceptions = AccAuditRange.count(range=date_range)
        range_exceptions_amount = AccAuditRange.total_amount(range=date_range)

        total_pending_refund_amount = CrNoteCashRefund.pending_amount(range=date_range)
        total_pending_refund_entries = CrNoteCashRefund.pendings_count(range=date_range)

        expense_as_income_total = ExpenseAsIncome.total_amount(range=date_range)
        expense_as_income_entries = ExpenseAsIncome.count(range=date_range)

        total_backdated_amount = BackDatedEntries.total_amount(range=date_range)
        total_backdated_entries = BackDatedEntries.count(range=date_range)

        result = {
            "total_refund": total_refund,
            "total_refund_entries": total_refund_entries,
            "range_exceptions": range_exceptions,
            "range_exceptions_amount": range_exceptions_amount,
            "total_pending_refund_amount": total_pending_refund_amount,
            "total_pending_refund_entries": total_pending_refund_entries,
            "expense_as_income_total": expense_as_income_total,
            "expense_as_income_entries": expense_as_income_entries,
            "total_backdated_amount":total_backdated_amount,
            "total_backdated_entries":total_backdated_entries
        }

        return ResponseHandler.success(data=result)
    

class GetExpenseAsIncomes(APIView):
    def get(self,request):

        date_range = request.GET.get('range', 900)


        limit = request.GET.get('limit',10)


        list = ExpenseAsIncome.list(range=date_range)

        return ResponseHandler.success(data=list)


class GetPendingCrNoteLsit(APIView):
    def get(self,request):
        date_range = request.GET.get('range', 900)

        list = CrNoteCashRefund.pending_list(range=date_range)

        return ResponseHandler.success(data=list)
    
class GetCrNotRefundSummery(APIView):
    def get(self,request):
        date_range = request.GET.get('range',900)

        list = CrNoteCashRefund.get_summery(range=date_range)

        return ResponseHandler.success(data=list)
    
class GetCrNoteRefundDetails(APIView):
    def get(self,request):
        dot = request.GET.get('dot')

        if not dot:
            return ResponseHandler.bad_request("Dot required")

        result = CrNoteCashRefund.get_details(dot=dot)

        return ResponseHandler.success(data=result)

class GetRangeAudits(APIView):
    def get(self,request):

        date_range = request.GET.get('range',900)

        list = AccAuditRange.list(range=date_range)

        return ResponseHandler.success(data=list)
    
class GetBackDatedEntries(APIView):
    def get(Self,request):

        date_range = request.GET.get('range',900)

        list = BackDatedEntries.list(range=date_range)

        return ResponseHandler.success(data=list)

    

