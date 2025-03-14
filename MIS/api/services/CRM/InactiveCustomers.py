from ...models.Models import Customers
from ...Core import db

class InActiveCustomers:
    model =Customers

    @classmethod
    def list(cls):

        query = """SELECT * from Customers where NOB = 0;"""

        result = db.get_data(query=query)

        return result
        
    @classmethod
    def count(cls):
        query = """SELECT Count(*) as count FROM Customers WHERE NOB=0;"""
        result = db.get_data(query=query)

        return result[0]['count']
    