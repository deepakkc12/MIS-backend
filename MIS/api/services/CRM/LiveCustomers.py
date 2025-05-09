from ...models.Models import LiveCustomerData
from ...Core import db

class LiveCustomers:
    model = LiveCustomerData

    @classmethod
    def levels(cls):
        query = """SELECT CustomerLevel, COUNT(*) as count
                    FROM LiveCustomerData 
                    GROUP BY CustomerLevel
                    Order by CustomerLevel;
                    """
        result = db.get_data(query=query)
        return result
    
    @classmethod
    def list(cls,level=None):

        if not level:
            return cls.model.serialized_list()
        
        return cls.model.serialized_filtered_list(CustomerLevel=level)