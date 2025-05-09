from ...models.Models import Customers
from ...Core import db


class PriorityCustomers:

    Model = Customers

    @classmethod
    def list(cls,start_date=1,end_date = 5):
        
        query = """
        SELECT 
    c.code, c.Name, c.BillDaysFrom, c.BillDaysTo,c.NOB,c.ABV,c.Phone ,c.ABVMth,c.dot,
    COUNT(CASE WHEN s.GrossAmt > 1000 THEN 1 END) AS highValueSales
    FROM Customers c
    LEFT JOIN Sales s ON c.Code = s.CardHolderCode
    WHERE c.BillDaysFrom BETWEEN ? AND ? 
    GROUP BY c.Code, c.Name, c.BillDaysFrom, c.BillDaysTo,c.NOB,c.ABV,c.Phone,c.ABVMth,c.dot order by highValueSales DESC
        """
        
        data = [start_date,start_date+5]

        result = db.get_data(query=query,data=data)

        return result


    @classmethod
    def get_top_priority_count(cls):
        query = """
        Select count(*) as priorityCustomers from ActiveCustomers A WHERE ((A.AMOUNT) / 5) > 2000 
AND A.OCT > 0 
AND A.NOV > 0 
AND A.DEC > 0 
AND A.JAN > 0 
AND A.FEB > 0;
        """
        result = db.get_data(query=query)

        if not result:
            raise Exception("Result not found")
        
        return result[0]['priorityCustomers']


    @classmethod
    def get_individual_sales(cls,customer_code):
        query = """select * from sales where CardHolderCode = ? """

        param = [customer_code]

        result = db.get_data(query=query,data=param)

        return result
    
    @classmethod
    def get_top_priority_customers(cls):
        query = """SELECT C.Name, A.*
FROM ActiveCustomers A
JOIN Customers C ON A.CardHolderCode = C.Code

WHERE ((A.AMOUNT) / 5) > 2000 
AND A.OCT > 0 
AND A.NOV > 0 
AND A.DEC > 0 
AND A.JAN > 0 
AND A.FEB > 0
Order By A.AMount DESC
;"""
    

        result = db.get_data(query=query)

        return result

