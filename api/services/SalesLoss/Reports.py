from ...Core import db

class SalesLossReports():


    # @classmethod
    # def summery(cls):
    #     query = """Select code,SkuName,CQTY,GroupName,pwSales,D7,D6,D5,D4,D3,D2,D1,cuWSales,pwSQty,cwSQty from StkZeroStockSku Order by pwSales DESC"""
    #     result = db.get_data(query=query)
    #     return result
    
    @classmethod
    def summery(cls):
        query = """SELECT
    AvgaSalesPerDay,
    (
        CASE WHEN D7 = 0 THEN AvgaSalesPerDay ELSE 0 END +
        CASE WHEN D6 = 0 THEN AvgaSalesPerDay ELSE 0 END +
        CASE WHEN D5 = 0 THEN AvgaSalesPerDay ELSE 0 END +
        CASE WHEN D4 = 0 THEN AvgaSalesPerDay ELSE 0 END +
        CASE WHEN D3 = 0 THEN AvgaSalesPerDay ELSE 0 END +
        CASE WHEN D2 = 0 THEN AvgaSalesPerDay ELSE 0 END +
        CASE WHEN D1 = 0 THEN AvgaSalesPerDay ELSE 0 END
    ) AS SalesLossInWeek,
    SkuName,
    
    Code,
    GroupName,
    cuWSales,
    pwSQty,
    cwSQty,
    D1, D2, D3, D4, D5, D6, D7
FROM (
    SELECT
        SUM(pwSales) / 7 AS AvgaSalesPerDay,
        D1, D2, D3, D4, D5, D6, D7,
        SkuName,
        Code,
        GroupName,
        cuWSales,
        pwSQty,
        cwSQty
    FROM StkZeroStockSku
    GROUP BY D1, D2, D3, D4, D5, D6, D7,
        Code,
        SkuName,
        GroupName,
        cuWSales,
        pwSQty,
        cwSQty
) AS SalesData
ORDER BY SalesLossInWeek DESC;
 """
        result = db.get_data(query=query)

        return result

    @classmethod
    def current_zero_stock_items(cls):
        query = """select * from StkZeroStockSku WHere D1 = 0 Order by pwSales"""

        result = db.get_data(query=query)

        return result
    
    @classmethod
    def current_zero_stock_items_count(cls):
        query = """select Count(*) as cnt from StkZeroStockSku WHere D1 = 0"""

        result = db.get_data(query=query)

        return result
    
    def this_weak_total_opertunity_loss(cls):
        query = """Select """
    