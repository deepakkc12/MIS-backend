from ...models.Models import AccAuditCrNoteCashRefundSummary,AccAuditCrNoteCashRefundDetails,AccAuditExpAsIncome,BackDatedAccounts
from ...Core import db
from ..Settings.Settings import Settings

from ...utils.helpers import get_current_date,get_past_date

class BackDatedEntries:
    @classmethod
    def list(cls,range=7,end_date=Settings.last_updated):

        range = int(range) - 1

        start_date = get_past_date(difference=range,date1=end_date)

#         query = """SELECT M.CODE,M.DOT,M.EntryDate, M.VoucherNo,M.Description,TRTY.Name TransName,LEMA.Name,DayDiff(Day,M.DOT,M.EntryDate)
#   CASE WHEN MODE=1 THEN DABODE.Amount ELSE 0 END Dr,CASE WHEN MODE=2 THEN DABODE.Amount ELSE 0 END Cr,CA.Alias,ca.code caCode where DOT between ? and ?
# """

        query = """SELECT *, DATEDIFF(DAY, Dot, EntryDate) AS DaysDiff 
                FROM BackDatedAccounts 
                WHERE DOT BETWEEN ? AND ? 
                ORDER BY DaysDiff DESC
                """

        data = [start_date,end_date]


        result = db.get_data(query=query,data=data)
        
        return result
    
    @classmethod
    def total_amount(cls,range=7,end_date=Settings.last_updated):

        range = int(range) - 1

        start_date = get_past_date(difference=range,date1=end_date)

        query = """select SUM(Dr + Cr) as total from BackDatedAccounts where dot between ? and ?"""

        params = [start_date,end_date]

        result = db.get_data(query=query,data=params)

        print(result)

        return result[0]['total'] if result else 0
    
    @classmethod
    def count(cls,range=7,end_date=Settings.last_updated):

        range = int(range) - 1

        start_date = get_past_date(difference=range,date1=end_date)

        query = """select Count(*) as cnt from BackDatedAccounts where dot between ? and ?"""

        params = [start_date,end_date]
        result = db.get_data(query=query,data=params)

        return result[0]['cnt'] if result else 0
    
