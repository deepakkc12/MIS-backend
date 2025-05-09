from ...utils.helpers import get_current_date,get_past_date
from ...Core import db

from ..Settings.Settings import Settings


class Last2MonthTrailBalance():

    @classmethod
    def get_total_opex(cls,):
        query = """select Sum(M1Dr) as Mont1Debit, Sum(M1Cr) as Mont1Credit, Sum(M2Dr) as Mont2Debit, Sum(M2Cr) as Mont2Credit from TrailBalance2Mths

        where OpexCapex ='opex' """     
        result =db.get_data(query=query)

        return result[0]
    
    @classmethod
    def get_last_2_month_sales(cls):
        query = """select Sum(Jan) as M1TotalSales, Sum(FEB) as M2TotalSales From ActiveCustomers """
        result = db.get_data(query=query)

        return result[0]
    
    @classmethod
    def sales_opex_comparison(cls):
        opex = cls.get_total_opex()
        sales = cls.get_last_2_month_sales()

        result = {"opex":opex,"sales":sales}

        return result
    
    @classmethod
    def get_recievables_of_last_two_month(cls):

        query = """select * from TrailBalance2Mths  where PaymentTrack = 'Receivable' """

        result = db.get_data(query=query)

        return result
    
    @classmethod
    def get_payables_of_last_two_month(cls):

        query = """select * from TrailBalance2Mths  where PaymentTrack = 'Payable'"""

        result = db.get_data(query=query)

        return result


    @classmethod
    def get_opex_list(cls):

        query = """select code,Name,AccHead,Dr as TotalDr,Cr as TotalCr,M1Dr,m1Cr,M2Cr,M2Dr,PaymentTrack from TrailBalance2Mths  where OpexCapex = 'opex'"""

        result = db.get_data(query=query)

        return result

    

    
