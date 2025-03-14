from ...models.Models import SalesLoss
from ...Core import db

class SalesLossReports():

    @staticmethod
    def list(is_active=None):
        
        query = """SELECT * FROM SaleLoss Where IsActive = ?"""

        pass

    