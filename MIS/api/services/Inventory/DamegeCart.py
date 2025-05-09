
from ...Core import db


class DamageCart():
    @classmethod
    def get_cart_summery_by_vendor(cls):
        query = """select * from DamageCartSummary Order By purchaseAfter DESC"""

        result = db.get_data(query=query)

        return result
    

    @classmethod
    def get_details_by_vendor_code(cls,vendor_code):
        query = """select * from DamageCart Where VendorCode = ?"""

        data = [vendor_code]

        result = db.get_data(query=query,data=data)

        return result
    