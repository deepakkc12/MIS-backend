
from ...Core import db
from ...models.Models import ActiveCustomers
from .Ranking import RankedCustomers


class NonPerformingCustomers:

    model = ActiveCustomers


    def count():
        query = """SELECT COunt(*) as totalNpc from ActiveCustomers where JAN = 0 and FEB = 0"""

        result = db.get_data(query=query)

        if not result:
            raise Exception("Count not got")
        
        return result[0]['totalNpc']
    

    def list():

        ranked_list = RankedCustomers.list()

        result = []

        for customer in ranked_list:
            if(customer['JAN']==0 and customer['FEB']==0):
                result.append(customer)

        return result