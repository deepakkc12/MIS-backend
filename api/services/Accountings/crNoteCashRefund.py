from ...models.Models import AccAuditCrNoteCashRefundSummary,AccAuditCrNoteCashRefundDetails
from ...Core import db
from ..Settings.Settings import Settings

from ...utils.helpers import get_current_date,get_past_date

class CrNoteCashRefund:

    @classmethod
    def get_summery(cls,range=7,end_date=Settings.last_updated):

        range = int(range) - 1

        start_date = get_past_date(difference=range,date1=end_date)

        query = """select *,Termina as Terminal from AccAuditCrNoteCashRefundSummary where dot between ? and ? order by dot Desc"""

        params = [start_date,end_date]
        result = db.get_data(query=query,data=params)

        return result
    

    @classmethod
    def get_total_amount(cls,range=7,end_date=Settings.last_updated):

        range = int(range) - 1

        start_date = get_past_date(difference=range,date1=end_date)

        query = """SELECT FORMAT(SUM(Amount), 'N2') AS Total
            FROM AccAuditCrNoteCashRefundSummary
            WHERE dot BETWEEN ? AND ?
            """

        params = [start_date,end_date]
        result = db.get_data(query=query,data=params)

        return result[0]['Total'] if result else 0
    

    @classmethod
    def count(cls,range=7,end_date=Settings.last_updated):

        range = int(range) - 1

        start_date = get_past_date(difference=range,date1=end_date)

        query = """select Count(*) as cnt from AccAuditCrNoteCashRefundDetails where dot between ? and ? """

        params = [start_date,end_date]
        result = db.get_data(query=query,data=params)

        return result[0]['cnt'] if result else 0
    

    @classmethod
    def pendings_count(cls,range=7,end_date=Settings.last_updated):

        range = int(range) - 1

        start_date = get_past_date(difference=range,date1=end_date)

        query = """select Count(*) as cnt from AccAuditCrNotePendings where dot between ? and ? """

        params = [start_date,end_date]
        result = db.get_data(query=query,data=params)

        result =result[0]['cnt'] if result else 0

        return result if result else 0
    
    @classmethod
    def get_details(cls,dot):
        query= """SELECT * from AccAuditCrNoteCashRefundDetails where dot = ?"""
        param = [dot]

        result = db.get_data(query=query,data=param)

        return result
    

    def get_pending_list(cls,range=7,end_date=Settings.last_updated):

        range = int(range) - 1

        start_date = get_past_date(difference=range,date1=end_date)

        query = """select * from AccAuditCrNotePendings where dot between ? and ?"""

        params = [start_date,end_date]
        result = db.get_data(query=query,data=params)

        return result
    
    @classmethod
    def pending_list(cls,range=7,end_date=Settings.last_updated):

        range = int(range) - 1

        start_date = get_past_date(difference=range,date1=end_date)

        query = """select * from AccAuditCrNotePendings where dot between ? and ?"""

        params = [start_date,end_date]
        result = db.get_data(query=query,data=params)

        return result
    

    @classmethod
    def pending_amount(cls,range=7,end_date=Settings.last_updated):

        range = int(range) - 1

        start_date = get_past_date(difference=range,date1=end_date)

        query = """SELECT FORMAT(SUM(Amount), 'N2') AS Total
            FROM AccAuditCrNotePendings
            WHERE dot BETWEEN ? AND ?
            """

        params = [start_date,end_date]
        result = db.get_data(query=query,data=params)

        return result[0]['Total'] if result else 0
    