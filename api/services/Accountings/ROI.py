from ...models.Models import AccAuditCrNoteCashRefundSummary,AccAuditCrNoteCashRefundDetails,AccAuditExpAsIncome,BackDatedAccounts
from ...Core import db
from ..Settings.Settings import Settings


class ROI:
    @classmethod
    def get(cls,):
        query = """SELECT 
    FORMAT(r.dot, 'yyyy-MMM') AS Month,  -- Extracts Year-Month from 'dot'
    SUM(r.Amount) AS ReceivedAmount,  -- Total received amount from ROI table
    SUM(rt.Amount) AS TargetAmount  -- Total target amount from ROITarget table
FROM ROI r
LEFT JOIN ROITarget rt ON FORMAT(r.dot, 'yyyy-MM') = FORMAT(rt.dot, 'yyyy-MM')  -- Join based on month-year
GROUP BY FORMAT(r.dot, 'yyyy-MMM')
ORDER BY Month DESC;"""
        
        result = db.get_data(query=query)
        return result
        pass