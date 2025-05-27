from django.urls import path
from ..view.auth import Login, Logout, ValidateToken, GetLoginedBranchDetails

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    # path('logout/', Logout.as_view(), name='logout'),
    # path('validate-token/', ValidateToken.as_view(), name='validate-token'),
    # path('session-branch-details/', GetLoginedBranchDetails.as_view(), name='validate-token'),
]
