from ..Settings.Settings import Settings
from  ...utils.helpers import get_past_date
from  ...Core import db


class UnregisteredEans:

    @classmethod
    def list(cls):

        query = "SELECT DISTINCT * FROM POS_Audit_EAN_NotRegistred order by MRP desc"

        result = db.get_data(query=query)

        return result

    @classmethod
    def count(cls):

        query = """SELECT COUNT(*) AS cnt FROM (SELECT DISTINCT * FROM POS_Audit_EAN_NotRegistred) AS subquery"""

        result = db.get_data(query=query)

        return result[0]['cnt'] if result else 0

