from ...models.Models import GroupNbrands as GroupNbrandsModel,LiveSku
from ...Core import db


class Brands():
    @classmethod
    def get_groups(cls,brand_code):

        query = """SELECT 
              G.Name, G.Code, 
              SUM(ST.GrossAmt) AS ThisMonthTotalSales, 
              SUM(ST.COGS) AS ThisMonthTotalCogs, 
              SUM(SP.GrossAmt) AS PrevMonthTotalSales, 
              SUM(SP.COGS) AS PrevMonthTotalCogs
           FROM ProductGroups G
           JOIN GroupNbrands GN ON G.Code = GN.ProductGroupCode
           JOIN skuSalesThisMonth ST ON ST.GroupNBrandCode = GN.Code
           JOIN skuSalesPrevMonth SP ON SP.GroupNBrandCode = GN.Code
           WHERE GN.BrandCode = ?
           GROUP BY G.Name, G.Code
"""

        data = [brand_code]

        result = db.get_data(query=query,data=data)

        return result
    

    @classmethod
    def recent_vendors(self, brand_code):
        query = """ 
            SELECT B.*, l.skuName 
            FROM StkBills B 
            LEFT JOIN LiveSku l ON l.Code = B.ItemCode 
            LEFT JOIN GroupNbrands gb ON gb.code = l.groupNbrandCode 
            WHERE gb.BrandCode = ?
        """
        
        params = [brand_code]  # Always filter by group_code

        result = db.get_data(query=query, data=params)  
        return result
    
    @classmethod
    def recent_paid_vendors(self, brand_code):
        query = """ 
            SELECT B.*, l.skuName 
            FROM StkPaidBills B 
            LEFT JOIN LiveSku l ON l.Code = B.ItemCode 
            LEFT JOIN GroupNbrands gb ON gb.code = l.groupNbrandCode 
            WHERE gb.BrandCode = ?
        """
        
        params = [brand_code]  # Always filter by group_code

        result = db.get_data(query=query, data=params)  
        return result
        
    @classmethod
    def get_details(cls,brand_code):
        result = {
            "groups":cls.get_groups(brand_code=brand_code),
             "Recentvendors":cls.recent_vendors(brand_code=brand_code),
            'recentVendorsWhoPaidWithouClearingStock':cls.recent_paid_vendors(brand_code=brand_code),
        }

        return result