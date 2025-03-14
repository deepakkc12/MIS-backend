from ...models.Models import LiveCustomerData
from ...Core import db

class LiveCustomers:
    model = LiveCustomerData

    @classmethod
    def levels(cls):
        query = """SELECT CustomerLevel, COUNT(*) as count
                    FROM LiveCustomerData 
                    GROUP BY CustomerLevel;
                    """
        result = db.get_data(query=query)
        return result