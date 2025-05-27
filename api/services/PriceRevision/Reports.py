from ...models.Models import PriceRevision
from ...Core import db


class PriceRevisionReports():
    @staticmethod
    def list(start_date,end_date):

        query = """SELECT * FROM PriceRevision WHERE DOT between ? and ?"""

        params = [start_date,end_date]

        result = db.get_data(query=query,data=params)

        return result
    
    