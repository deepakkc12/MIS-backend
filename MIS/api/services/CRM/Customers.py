from enum import Enum
import logging
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from django.http import HttpRequest
from ...Core import db
from ...models.Models import Customers
from .InactiveCustomers import InActiveCustomers
from .PriorityCustomers import PriorityCustomers
from ...utils.exceptions import AuthenticationError, InternalServerError
from ...utils.contexts import propagate_errors
from ...utils.helpers import get_current_date,get_past_date
from ..Settings.Settings import Settings


class CRM:

    model = Customers

    last_synced_date = Settings.last_updated

    @classmethod
    def get_totla_customers(cls):
        query = """SELECT COUNT(*) AS TotalCustomers FROm Customers"""

        result = db.get_data(query=query)

        return result[0].get("TotalCustomers") if result else 0
    
    @classmethod
    def matrices_data(cls):

        current_date = get_current_date()

        prv_month_end_date = get_past_date(30)
        prv_month_start_date = get_past_date(60)



        query = """SELECT 
                COUNT(*) AS totalCustomers,
                SUM(ABVMth) * 1.0 / COUNT(*) AS avgABV,
                
                SUM(CASE WHEN dot BETWEEN ? AND ? THEN 1 ELSE 0 END) AS CurrentMCustomers,
                SUM(CASE WHEN dot BETWEEN ? AND ? THEN 1 ELSE 0 END) AS PrevMCustomers

            FROM Customers;

            """
        
        data = [prv_month_end_date,current_date,prv_month_start_date,prv_month_end_date]

        result = db.get_data(query=query,data=data)


        result = result[0] if result else None

        if not result:
            return

        current = result["CurrentMCustomers"]

        prev = result['PrevMCustomers']

        abv = result['avgABV']

        abv = round(abv,2)

        result['avgABV'] = abv

        trend = ((current - prev) / prev) * 100

        trend = round(trend, 2)

        result['customerTrend']= trend

        return result
    
    @classmethod
    def get_segments_count(cls):

        result = {
            "InactiveCustomers":0,
            "priorityCustomers":0,
            "frequentVisitors":0,
            "nonPerformingCustomers":0
        }

        inactive_customers = InActiveCustomers.count()

        priority_customers = PriorityCustomers.count()


    @classmethod
    def get_final_bill_details(cls,customer:Customers):
        query = """select Sum(GrossAmt) totAMt from sales where dot = ? and CardHolderCode = ? """
        params = [customer.LastSalesDate,customer.Code]

        result = db.get_data(query=query,data=params)

        return result[0]['totAMt'] if result else 0
    
    @classmethod
    def get_total_sales_summery(cls,customer:Customers):
        query = """select sum(GrossAmt) as totalAmt from sales where CardHolderCode = ?"""

        param = [customer.Code]

        result = db.get_data(query=query,data=param)

        return result[0]['totalAmt'] if result else 0
    

    @classmethod
    def get_primary_buy_days_summery (cls,customer:Customers):
        query = """SELECT SUM(GrossAmt) AS totalAmt 
                FROM sales 
                WHERE CardHolderCode = ? 
                AND DAY(dot) BETWEEN ? AND ?
                """
        
        param = [customer.Code,customer.BillDaysFrom,customer.BillDaysTo]

        result = db.get_data(query=query,data=param)

        return result[0]['totalAmt'] if result else 0 


    @classmethod
    def customer_best_sale(cls,customer:Customers):
        query = """SELECT TOP 1 * 
            FROM Sales 
            WHERE CardHolderCode = ? 
            ORDER BY GrossAmt DESC;
            """

        param = [customer.Code]

        result = db.get_data(query=query,data=param)

        return result[0] if result else {}


    @classmethod
    def customer_details(cls,customer_code):
        customer = cls.model.find_by_id(customer_code)

        total_sales_amt = cls.get_total_sales_summery(customer=customer)

        final_sale_amount = cls.get_final_bill_details(customer=customer)

        primary_days_sales = cls.get_primary_buy_days_summery(customer=customer)

        result = customer.serialize()

        result['TotalSales'] = total_sales_amt

        result['FinalSaleAmt'] = final_sale_amount

        result['primaryDaySales'] = primary_days_sales

        result['bestSale'] = cls.customer_best_sale(customer=customer)

        return result
    
    @classmethod
    def sales_list(cls,customer:Customers):
        query = """SELECT * from Sales WHere CardHolderCode = ? Order by dot DESC"""
        param = [customer.Code]

        result = db.get_data(query=query,data=param)

        return result
    

    def highest_month_details(cls,customer:Customers):
        query = """SELECT """


    def month_wise_sales(cls,customer:Customers,year):

        query = """SELECT 
    CASE MONTH(DOT)
        WHEN 1 THEN 'Jan'
        WHEN 2 THEN 'Feb'
        WHEN 3 THEN 'Mar'
        WHEN 4 THEN 'Apr'
        WHEN 5 THEN 'May'
        WHEN 6 THEN 'Jun'
        WHEN 7 THEN 'Jul'
        WHEN 8 THEN 'Aug'
        WHEN 9 THEN 'Sep'
        WHEN 10 THEN 'Oct'
        WHEN 11 THEN 'Nov'
        WHEN 12 THEN 'Dec'
    END AS month,
    SUM(GrossAmt) AS amount
FROM 
    dmMIS
WHERE 
    CardHolderCode = ?
    AND DOT BETWEEN ? AND ?
GROUP BY 
    MONTH(DOT)
ORDER BY 
    MONTH(DOT);"""
        
        param = [customer.Code]

        result = db.get_data(query=query,data=param)

        return result
    
    @classmethod
    def year_wise_sales(cls,customer:Customers):

        query = """SELECT 
            YEAR(DOT) AS year,
            SUM(GrossAmt) AS amount
        FROM 
            Sales 
        WHERE
            GrossAmt IS NOT NULL
            AND DOT IS NOT NULL
        GROUP BY
            YEAR(DOT)
        ORDER BY 
            YEAR(DOT)"""
        
        result = db.get_data(query=query)

        return result


    @classmethod
    def value_distribution(cls):

        end_date = cls.last_synced_date

        start_date = get_past_date(30,end_date)

        query = """WITH CustomerTotalSales AS (
    -- Calculate the total sales amount for each customer
    SELECT 
        c.CardHolderCode AS CustomerCode,
        SUM(s.GrossAmt) AS TotalSpend
    FROM 
        ActiveCustomers c
    LEFT JOIN 
        Sales s ON c.CardHolderCode = s.CardHolderCode where dot between ? and ?
    GROUP BY 
        c.CardHolderCode
),
CustomerValueCategories AS (
    -- Categorize customers based on their total spend
    SELECT 
        CASE 
            WHEN TotalSpend IS NULL OR TotalSpend < 1000 THEN '0-999'
            WHEN TotalSpend >= 1000 AND TotalSpend < 5000 THEN '1000-4999'
            WHEN TotalSpend >= 5000 AND TotalSpend < 10000 THEN '5000-9999'
            WHEN TotalSpend >= 10000 THEN '10000+'
        END AS Category,
        COUNT(*) AS Customers
    FROM 
        CustomerTotalSales
    GROUP BY 
        CASE 
            WHEN TotalSpend IS NULL OR TotalSpend < 1000 THEN '0-999'
            WHEN TotalSpend >= 1000 AND TotalSpend < 5000 THEN '1000-4999'
            WHEN TotalSpend >= 5000 AND TotalSpend < 10000 THEN '5000-9999'
            WHEN TotalSpend >= 10000 THEN '10000+'
        END
)
-- Final result with ORDER BY in the main query instead of the CTE
SELECT 
    category,
    customers
FROM 
    CustomerValueCategories
ORDER BY 
    CASE 
        WHEN Category = '0-999' THEN 1
        WHEN Category = '1000-4999' THEN 2
        WHEN Category = '5000-9999' THEN 3
        WHEN Category = '10000+' THEN 4
        ELSE 5
    END;"""
        
        data = [start_date,end_date]
        
        result = db.get_data(query=query,data=data)

        return result
    

    @classmethod
    def sales_trend(cls):

        query = """SELECT 
    DATEPART(YEAR, s.DOT) AS Year,
    DATENAME(MONTH, s.DOT) AS month,
    COUNT(DISTINCT s.CardHolderCode) AS customers,
    SUM(s.GrossAmt) AS revenue
FROM 
    Sales s WITH (NOLOCK)
WHERE 
    s.DOT IS NOT NULL
    AND s.DOT >= DATEADD(MONTH, -11, ?)
GROUP BY 
    DATEPART(YEAR, s.DOT),
    DATENAME(MONTH, s.DOT),
    DATEPART(MONTH, s.DOT)
ORDER BY 
    DATEPART(YEAR, s.DOT),
    DATEPART(MONTH, s.DOT);"""
        

        # raise Exception("ec")

        param = [cls.last_synced_date]

        result = db.get_data(query=query,data=param)

        # print(result)

        return result
