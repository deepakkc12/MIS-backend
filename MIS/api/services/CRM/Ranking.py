from ...Core import db

class RankedCustomers():
    def list():
        query = """WITH TotalSales AS (
    SELECT
        SUM([AMOUNT]) AS totalSales
    FROM [ActiveCustomers]
),
CustomerSales AS (
    SELECT
        CardHolderCode,
        [AMOUNT],
        ([AMOUNT] / totalSales) * 100 AS contributionPercentage
    FROM ActiveCustomers  CROSS JOIN TotalSales
),
RankedCustomers AS (
    SELECT
        CardHolderCode,
       [AMOUNT],
        contributionPercentage,
        RANK() OVER (ORDER BY [AMOUNT] DESC) AS rank
    FROM CustomerSales
)
SELECT Customers.code,Customers.Name,Customers.Phone,Customers.ABV,Customers.ABVMth,
Customers.NOB, ActiveCustomers.OCT, ActiveCustomers.NOV, ActiveCustomers.DEC,ActiveCustomers.JAN,ActiveCustomers.FEB,
    ActiveCustomers.AMOUNT,
    contributionPercentage,
    CAST((100 - ((rank - 1) * 100.0 / COUNT(*) OVER ())) AS DECIMAL(18, 2)) AS rankOutOf100
FROM RankedCustomers,ActiveCustomers,Customers
where RankedCustomers.CardHolderCode=Customers.code and
ActiveCustomers.CardHolderCode=Customers.code
 order by contributionPercentage desc
    """
        result = db.get_data(query=query)

        return result
    



