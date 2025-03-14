
from  ...Core import db


class BrowsedPrivateLabels:

    @classmethod
    def list(cls):

        query = f"""SELECT * FROM POS_Audit_BrowsedPrivateLabels"""

        result = db.get_data(query=query)

        return result

    @classmethod
    def count(cls):

        query = """select Count(*) as cnt from POS_Audit_BrowsedPrivateLabels"""

        result = db.get_data(query=query)

        return result[0]['cnt'] if result else 0

