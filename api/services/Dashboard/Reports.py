from enum import Enum
import logging
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from django.http import HttpRequest
from ...Core import db
from ...utils.exceptions import AuthenticationError, InternalServerError
from ...utils.contexts import propagate_errors
from ...utils.helpers import get_current_date



class DashBoard:


    @classmethod
    def get_total_revnue(cls):
        
        query = """SELECT SUM(GrossAmt) as TotalRevenue
                    FROM SALES WITH (NOLOCK)"""
        
        result = db.get_data(query=query,data=[])

        return result
    
    @classmethod
    def get_profit_details(cls):

        query = """ SELECT 
        SUM(GrossAmt) as TotalRevenue,
        Count(*) as Nob
        FROM Sales WITH (NOLOCK) """

        result = db.get_data(query=query)

        return result[0]

    @classmethod
    def get_zero_stock_sku(cls,date):

        date = get_current_date()
        
        query = """select Count(*) FROM ZeroStockSKU WHERE DOT = ? AND PhysicalStock = 0"""

        result = db.get_data(query=query,data=[date])

        return result
    

    def get_last_weak_customer_trend(cls):
        query = """
                SELECT 
                    COUNT(DISTINCT Code) AS TTEND
                FROM 
                    Customers
                WHERE 
                    LastVisited >= DATEADD(DAY, -7, CAST(GETDATE() AS DATE)) 
                    AND LastVisited < CAST(GETDATE() AS DATE);
                """
        
        

    @classmethod
    def get_sales_opertunity_loss(cls,date):

        date = get_current_date

        query = """SELECT 
    s.Code as SKUCode,
    s.Name as ProductName,
    sl.Reason,
    sl.DateFrom,
    sl.DateTo,
    sl.ASM,
    sl.ASPD,
    -- Calculate days between dates
    DATEDIFF(day, sl.DateFrom, CASE 
        WHEN sl.DateTo > GETDATE() THEN GETDATE() 
        ELSE sl.DateTo 
    END) as DaysLost,
    -- Calculate total loss: Days × Average Sales Per Day × Average Sales Margin
    DATEDIFF(day, sl.DateFrom, CASE 
        WHEN sl.DateTo > GETDATE() THEN GETDATE() 
        ELSE sl.DateTo 
    END) * sl.ASPD * sl.ASM as EstimatedLoss
FROM SalesLoss sl
JOIN SKU s ON sl.SKUCode = s.Code
WHERE sl.IsActive = 1"""