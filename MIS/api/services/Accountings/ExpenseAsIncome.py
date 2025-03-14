from ...models.Models import AccAuditCrNoteCashRefundSummary,AccAuditCrNoteCashRefundDetails,AccAuditExpAsIncome
from ...Core import db
from ..Settings.Settings import Settings

from ...utils.helpers import get_current_date,get_past_date

class ExpenseAsIncome:

    @classmethod
    def list(cls,range=7,end_date=Settings.last_updated,limit=None):

        range = int(range) - 1

        start_date = get_past_date(difference=range,date1=end_date)

        query = f"""SELECT * FROM AccAuditExpAsIncome WHERE dot BETWEEN ? AND ?"""

        data = [start_date,end_date]

        result = db.get_data(query=query,data=data)

        return result
    

    @classmethod
    def total_amount(cls,range=7,end_date=Settings.last_updated):

        range = int(range) - 1

        start_date = get_past_date(difference=range,date1=end_date)

        query = """select FORMAT(SUM(CrAmout), 'N2') as total from AccAuditExpAsIncome where dot between ? and ?"""

        params = [start_date,end_date]

        result = db.get_data(query=query,data=params)

        return result[0]['total'] if result else 0
    
    @classmethod
    def count(cls,range=7,end_date=Settings.last_updated):

        range = int(range) - 1

        start_date = get_past_date(difference=range,date1=end_date)

        query = """select Count(*) as cnt from AccAuditExpAsIncome where dot between ? and ?"""

        params = [start_date,end_date]
        result = db.get_data(query=query,data=params)

        return result[0]['cnt'] if result else 0

    
