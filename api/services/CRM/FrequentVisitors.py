from ...models.Models import Customers,ActiveCustomers
from .Ranking import RankedCustomers
from ...Core import db


class FrequentVisitors:

    Model = ActiveCustomers

    master_where_condition = "OCT <> 0 and  NOV <> 0 and DEC <> 0 and JAN <> 0  and FEB <> 0"

    @classmethod
    def list(cls,):
        rank_list  = RankedCustomers.list()
        result = []
        for customer in rank_list:
            if(customer['OCT'] !=0 and customer['NOV'] !=0 and customer['DEC'] !=0 and customer['JAN'] !=0 and customer['FEB'] !=0):
                result.append(customer)
        
        return result
        
        


    @classmethod
    def count(cls):
        query = f"""
            Select count(*) as count from ActiveCustomers where {cls.master_where_condition}
        """

        result = db.get_data(query=query)

        if not result:
            raise Exception("")

        return result[0]['count']
    
    @classmethod
    def monthly_visits(cls):
        query = """Select Sum(Jan),Sum(Feb),sum()"""
    



