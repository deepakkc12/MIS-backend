
from  ...Core import db


class BrowsedRepackItems:

    @classmethod
    def list(cls):

        query = f"""SELECT * FROM POS_Audit_BrowsedRepackItems"""

        result = db.get_data(query=query)

        return result

    @classmethod
    def count(cls):

        query = """select Sum(cnt) as cnt from POS_Audit_BrowsedRepackItems"""

        result = db.get_data(query=query)

        return result[0]['cnt'] if result else 0

