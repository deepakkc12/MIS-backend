from django.urls import path
from ..view.Accounts import GetAccountMatrics,GetExpenseAsIncomes,GetPendingCrNoteLsit,    GetCrNotRefundSummery,    GetCrNoteRefundDetails,    GetRangeAudits,GetBackDatedEntries

urlpatterns = [

    path('metrics/', GetAccountMatrics.as_view(), name='accountings-matrices'),
   path('expense-as-incomes/', GetExpenseAsIncomes.as_view(), name='expense-as-incomes'),
    path('pending-cr-note-list/', GetPendingCrNoteLsit.as_view(), name='pending-cr-note-list'),
    path('cr-note-refund-summary/', GetCrNotRefundSummery.as_view(), name='cr-note-refund-summary'),
    path('cr-note-refund-details/', GetCrNoteRefundDetails.as_view(), name='cr-note-refund-details'),
    path('range-audits/', GetRangeAudits.as_view(), name='range-audits'),
    path('back-dated-entreis/', GetBackDatedEntries.as_view(), name='back-dated-entries-list'),
    
]