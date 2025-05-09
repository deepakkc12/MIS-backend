from ...utils.helpers import get_current_date,get_past_date
from ...Core import db

from ..Settings.Settings import Settings
from ..Accountings.TrialBalance import Last2MonthTrailBalance



class SalesServices():
    last_synced_date = Settings.last_updated


    @classmethod
    def get_last_2_month_sales_vs_opex(cls):
        result = Last2MonthTrailBalance.sales_opex_comparison()
        return result
    
    @classmethod
    def get_day_wise_sales_target(cls,date_range = 7):

        date_range = date_range -1

        last_synced_date = cls.last_synced_date

        start_date = get_past_date(date_range,date1=last_synced_date)

        end_Date = last_synced_date


        query = """SELECT * from salesTarget
                    WHERE DOT BETWEEN ? AND ?  
                    GROUP BY DOT  
                    ORDER BY DOT;
                    """
        
        current_params = [start_date,end_Date]

        result = db.get_data(query=query,data=current_params)

        return result
    
    @classmethod
    def get_month_wise_targets(cls,year=2025):
        query = """SELECT 
    FORMAT(DOT, 'MMM') AS month, 
    SUM(Amount) AS grossAmount
     FROM SalesTarget
WHERE YEAR(DOT) =?
GROUP BY FORMAT(DOT, 'MMM'), YEAR(DOT), MONTH(DOT)
ORDER BY monthNumber; """

    @classmethod
    def get_day_wise_sales(cls,date_range=7):

        date_range = date_range -1

        last_synced_date = cls.last_synced_date

        start_date = get_past_date(date_range,date1=last_synced_date)

        end_Date = last_synced_date

        previous_start_date = get_past_date(date_range+date_range+2,date1=last_synced_date)

        previous_end_date = get_past_date(1,start_date)

        query = """SELECT DOT as date,SUM(GrossAmt) AS grossAmount, COUNT(*) as nob  
                    FROM Sales  
                    WHERE DOT BETWEEN ? AND ?  
                    GROUP BY DOT  
                    ORDER BY DOT;
                    """
        
        current_params = [start_date,end_Date]
        previous_params = [previous_start_date,previous_end_date]

        current_result = db.get_data(query=query,data=current_params)
        previous_result = db.get_data(query=query,data=previous_params)

        print(len(current_result),len(previous_result))

        return {"current":current_result,"previous":previous_result}
    
    
    @classmethod
    def get_monthly_sales(cls,year=2025):
        query = """
           SELECT 
    FORMAT(DOT, 'MMM') AS month, 
    SUM(GrossAmt) AS grossAmount, 
    COUNT(InvoiceNo) AS nob,
    YEAR(DOT) AS year,
    MONTH(DOT) AS monthNumber
FROM Sales
WHERE YEAR(DOT) =?
GROUP BY FORMAT(DOT, 'MMM'), YEAR(DOT), MONTH(DOT)
ORDER BY monthNumber;

                """
        
        param = [year]

        result = db.get_data(query=query,data=param)

        return result
    
    @classmethod
    def get_yearly_sales(cls):
        query = """
        SELECT 
            SUM(GrossAmt) AS grossAmount, 
            COUNT(InvoiceNo) AS nob,
            YEAR(DOT) AS year
        FROM Sales
        GROUP BY YEAR(DOT)
        ORDER BY YEAR(DOT);
        """

        result = db.get_data(query=query)

        return result


    @classmethod
    def get_sales_target(cls):
        query = """select * from SalesTarget"""

        result = db.get_data(query=query)

        return result

        