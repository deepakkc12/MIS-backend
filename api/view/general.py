from datetime import datetime
from rest_framework.views import APIView
from ..services.CRM.Customers import CRM

from ..utils.response import ResponseHandler
from ..services.Dashboard.Reports import DashBoard
from ..utils.decorators import token_required
from ..Core import db


class DbTableData (APIView):
    def get(self,request):
        # querry  =  """EXEC sp_columns salesorderdetails"""
        querry  = """SELECt t.name From sys.tables T order by name"""

        tables = db.get_data(query=querry)

        for table in tables:
            querry2  =  f"""EXEC sp_columns {table['name']}"""
            columns = db.get_data(query=querry2)
            table["cloumns"] = columns


        return ResponseHandler.success(data=tables)