from ...models.Models import LiveSku,skuSalesPrevMonth,skuSalesThisMonth,SkuStock,LiveSubSKu,purchasePriceValidation,SalesPriceValidation
from ...Core import db

class Sku(LiveSku):

    @classmethod
    def serialized_list(cls, connection=db):
        return super().serialized_list(connection)
    
    def prev_month_sales(self):
        sales = skuSalesPrevMonth.serialized_filtered_list(UbDetailsCode=self.code)
        return sales if sales else {}
    
    def current_month_sales(self):
        sales = skuSalesThisMonth.serialized_filtered_list(UbDetailsCode=self.code)

        return sales[0] if sales else {}
    
    def sub_sku_list(self):
        list = LiveSubSKu.serialized_filtered_list(skuCode=self.code)
        return list
    
    def purchase_price_validations(self):
        validations = purchasePriceValidation.serialized_filtered_list(SkuName=self.SkuName)
        return validations[0] if validations else {}
    
    def sales_price_validations(self):
        validations = SalesPriceValidation.serialized_filtered_list(SkuName=self.SkuName)

        return validations[0] if validations else None
    
    def stock_details(self):
        details = SkuStock.serialized_filtered_list(ubDetailsCode=self.code)
        return details[0] if details else None


    def serialize(self):
        query = """select L.*, G.GroupName,G.BrandName From LiveSKu L Left Join GroupNbrands G On G.Code  = L.GroupNBrandCode Where L.Code = ?"""
        param = [self.code]
        result = db.get_data(query=query,data=param)

        return result[0] if result else None


    def details(self):
        result = {
            "info":self.serialize(),
            "prevMonthSales":self.prev_month_sales(),
            "curMonthSale":self.current_month_sales(),
            "weakStockDetails":self.stock_details(),
            # "purchasePriceValidations":None,
            # "salesPriceValidations":None,
            "subSkuList":self.sub_sku_list()
        }
        return result
    
    def summer_details(self):
        result = {
            "info":self.serialize(),
            # "prevMonthSales":self.prev_month_sales(),
            "curMonthSale":self.current_month_sales(),
            "weakStockDetails":self.stock_details(),

        }
        return result

    
    @classmethod
    def get_group_skus(cls,group_code):
        list = cls.serialized_filtered_list(prgrCode=group_code)
        return list
    

    @classmethod
    def get_grop_wise_sku(cls,prGrCode):
        query = """SELECT pg.code, pg.name, l.SkuName, l.code as skuCode, SUM(tm.GrossAmt) as TotalSales
FROM GroupNbrands gb
JOIN productGroups pg ON gb.ProductGroupCode = pg.Code
JOIN LiveSku l ON l.GroupNBrandCode = gb.Code
JOIN skuSalesThisMonth tm ON tm.UbDetailsCode = l.code
WHERE gb.ProductGroupCode = ?
GROUP BY l.code, l.SkuName, pg.code, pg.name"""
        
        result = db.get_data(query=query,data=[prGrCode])

        return result

