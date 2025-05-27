from ...models.Models import AccAuditCrNoteCashRefundSummary,AccAuditCrNoteCashRefundDetails
from ...Core import db
from ..Settings.Settings import Settings

from ...utils.helpers import get_current_date,get_past_date


class AccAuditRange:


    @classmethod
    def list(cls,range=7,end_date=Settings.last_updated):

        range = int(range) - 1

        start_date = get_past_date(difference=range,date1=end_date)

        query = """SELECT A.* ,R.AmountFrom,R.AmountTo
FROM AccAuditRange A
LEFT JOIN v_TransRange R ON R.ledgerCode = A.LedgerCode
WHERE DOT BETWEEN ? AND ? 
ORDER BY DOT DESC, Mode DESC, Name DESC
"""

        params = [start_date,end_date]
        result = db.get_data(query=query,data=params)

        return result
    
    @classmethod
    def count(cls,range=7,end_date=Settings.last_updated):

        range = int(range) - 1

        start_date = get_past_date(difference=range,date1=end_date)

        query = """select Count(*) as cnt from AccAuditRange where dot between ? and ?"""

        params = [start_date,end_date]
        result = db.get_data(query=query,data=params)
        result = result[0]['cnt'] if result else 0

        return result

    @classmethod
    def total_amount(cls,range=7,end_date=Settings.last_updated):

        range = int(range) - 1

        start_date = get_past_date(difference=range,date1=end_date)

        query = """select FORMAT(SUM(Amount), 'N2') as total from AccAuditRange where dot between ? and ?"""

        params = [start_date,end_date]
        result = db.get_data(query=query,data=params)

        result = result[0]['total'] if result else 0

        return result if result else 0 