from ...models.Models import GroupNbrands as GroupNbrandsModel,LiveSku,productCategory
from .Groups import Group
from .Items import Items
from ...Core import db

class Vendors():
    @classmethod
    def get_recent_item_wise_inwards(cls):
        query = """select * from stkBills"""

        result = db.get_data(query=query)

        return result
    

    @classmethod
    def get_recent_vendors(cls):

        query = """SELECT 
    SUM(S.INVOICEAMOUNT) AS PurchaseAmount,
    COUNT(S.INVOICEAMOUNT) AS CountOfPurchasingSkus,
    S.VENDOR AS VendorName,
    S.VENDORLEDGERCODE,
    ROUND(SUM(COALESCE(DC.purchaseAfter, 0)), 2) AS PurchasedAmountWithActiveDamages 
FROM stkBills S 
LEFT JOIN DamageCartSummary DC ON DC.vendorCode = S.VENDORLEDGERCODE
GROUP BY S.VENDOR, S.VENDORLEDGERCODE 
ORDER BY PurchaseAmount DESC;

"""

        result = db.get_data(query=query)

        return result
    

    
    @classmethod
    def get_inwards_paid_before_stock_clearance(cls):
        query = """select SUM(INVOICEAMOUNT) as PurchaseAmount,COunt(*) as CountOfPurchasingSkus,VENDOR as VendorName,VENDORLEDGERCODE from stkPaidBills Group by Vendor,VENDORLEDGERCODE ;"""

        result = db.get_data(query=query)

        return result
    

    @classmethod
    def get_vendor_groups(cls,vendor_code):

        query = """SELECT 
   DISTINCT pg.*
FROM StkBills sb
JOIN LiveSku ls ON sb.ItemCode = ls.Code
JOIN GroupNbrands gb ON ls.GroupNBrandCode = gb.Code
JOIN productGroups pg ON gb.ProductGroupCode = pg.Code
WHERE sb.VENDORLEDGERCODE = ?;

 """
        
        result = db.get_data(query=query,data=[vendor_code])

        return result
    
    @classmethod
    def get_vendor_brands(cls,vendor_code):
        query = """
SELECT 
   DISTINCT gb.BrandName,gb.BrandCode,gb.ProductGroupCode
FROM StkBills sb
JOIN LiveSku ls ON sb.ItemCode = ls.Code
JOIN GroupNbrands gb ON ls.GroupNBrandCode = gb.Code
JOIN productGroups pg ON gb.ProductGroupCode = pg.Code
WHERE sb.VENDORLEDGERCODE = ?;

"""
        result = db.get_data(query=query,data=[vendor_code])
        return result
    

    @classmethod
    def get_vendor_item_wise_purchaces(cls,vendor_code):

        query = """
                SELECT * FROM STKBILLs where VENDORLEDGERCODE = ?;
                """
        data = [vendor_code]

        result = db.get_data(data=data,query=query)

        return result
    
    @classmethod
    def get_sku_purchase_details(cls,vendor_code):
        
        query = """select l.SkuName	,l.code as SkuCode,l.cQty, SB.*  from LiveSku l Join StkBills SB ON l.Code = SB.ItemCode WHERE SB.VENDORLEDGERCODE = ?"""
        data = [vendor_code]

        result = db.get_data(data=data,query=query)

        return result
    
    @classmethod
    def get_vendor_damage_cart_summery(cls,vendor_code):
        query = """select * from DamageCart WHere vendorCode = ?"""
        data = [vendor_code]

        result = db.get_data(data=data,query=query)

        return result
    
    @classmethod
    def get_paid_with_pending_stock(cls,vendor_code):
        
        query = """select l.SkuName	,l.code as SkuCode,l.cQty, SB.*  from LiveSku l Join StkPaidBills SB ON l.Code = SB.ItemCode WHERE SB.VENDORLEDGERCODE = ?"""
        data = [vendor_code]

        result = db.get_data(data=data,query=query)

        return result




    @classmethod
    def get_vendor_details(cls,vendor_code):

        result = {
            'groups':cls.get_vendor_groups(vendor_code=vendor_code),
            'brands':cls.get_vendor_brands(vendor_code=vendor_code),
            'sku_recent_purchase_details':cls.get_sku_purchase_details(vendor_code=vendor_code),
            'paid_with_pending_sku_stock':cls.get_paid_with_pending_stock(vendor_code=vendor_code),
            'purchase_details_with_pending_damege_cart_entrys':cls.get_vendor_damage_cart_summery(vendor_code=vendor_code),


        }

        return result

