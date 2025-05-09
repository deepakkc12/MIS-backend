from ...models.Models import GroupNbrands as GroupNbrandsModel,LiveSku
from ...Core import db

class Group(GroupNbrandsModel):

    def current_month_sales(self, product_group_code, brand_code=None):
        query = """ 
            SELECT Sm.*, s.SkuName as SkuName 
            FROM skuSalesPrevMonth SM 
            LEFT JOIN LiveSku S ON S.code = SM.UbDetailsCode  
            WHERE SM.GroupNBrandCode IN 
                (SELECT Code FROM GroupnBrands 
                WHERE productGroupCode = ? """

        params = [product_group_code]  # Initialize params with required value

        if brand_code:  # If brand_code is provided, add filtering
            query += " AND BrandCode = ?"
            params.append(brand_code)

        query += ")"  # Close the subquery

        return db.get_data(query=query, data=params)
    
    def previous_month_sales(self, product_group_code, brand_code=None):
        query = """ 
            SELECT Sm.*, s.SkuName as SkuName 
            FROM skuSalesPrevMonth SM 
            LEFT JOIN LiveSku S ON S.code = SM.UbDetailsCode  
            WHERE SM.GroupNBrandCode IN 
                (SELECT Code FROM GroupnBrands 
                WHERE productGroupCode = ? """

        params = [product_group_code]  # Initialize params with required value

        if brand_code:
            query += " AND BrandCode = ?"
            params.append(brand_code)

        query += ")"  # Close the subquery

        return db.get_data(query=query, data=params)

    @classmethod
    def sku_list(self,product_group_code,brand_code=None):

        query = """select L.*,SCM.GrossAmt as CurrentMonthSale,SCM.COGS CurrentMonthCogs,SPM.GrossAmt as PrevMonthSale,SPM.COGS PrevMonthCogs from LiveSku L Left Join SkuSalesThisMonth SCM on SCM.UbDetailsCode = L.Code Left Join skuSalesPrevMonth SPM on SPM.UbDetailsCode = L.Code Where L.GroupNBrandCode in (select code from groupNbrands where productGroupCode = ? """

        params = [product_group_code]

        if brand_code:
            query += " AND BrandCode = ?"
            params.append(brand_code)

        query += ")" 

        result = db.get_data(query=query,data=[product_group_code])

        return result
    
    def top_selled_product(self):

        query = """
            SELECT SUM(TMS.GrossAmt) AS SkutotalSales, S.SkuName AS Skuname
            FROM skuSalesThisMonth TMS
            LEFT JOIN LiveSku S ON S.GroupNBrandCode = TMS.GroupNBrandCode
            WHERE TMS.GroupNBrandCode = ?
            GROUP BY S.UbDetailsCode
            ORDER BY SkutotalSales DESC
        """
        data = [self.Code]
        result = db.get_data(query=query, data=data)
        return result
    
    @classmethod
    def get_brands_by_productGroupCode(cls,product_group_code):
    
        query = """ Select brandCode, BrandName from GroupNbrands Where ProductGroupCode = ? order by salesRank DESC"""

        result = db.get_data(query=query,data=[product_group_code])

        return result
    
    @classmethod
    def get_brands_by_product_ategory_code(cls,product_category_code):
    
        query = """ Select brandCode, BrandName from GroupNbrands Where ProductGroupCode in (select Code from productGroups where ProductCategoryCode = ? )"""

        result = db.get_data(query=query,data=[product_category_code])

        return result
    
    @classmethod
    def recent_vendors(self, group_code, brand_code=None):
        query = """ 
            SELECT B.*, l.skuName 
            FROM StkBills B 
            LEFT JOIN LiveSku l ON l.Code = B.ItemCode 
            LEFT JOIN GroupNbrands gb ON gb.code = l.groupNbrandCode 
            WHERE gb.productGroupCode = ?
        """
        
        params = [group_code]  # Always filter by group_code

        if brand_code:  # Only filter by brand_code if provided
            query += " AND gb.BrandCode = ?"
            params.append(brand_code)

        result = db.get_data(query=query, data=params)  
        return result
    
    @classmethod
    def recent_paid_vendors(self,group_code, brand_code=None):
        query = """ 
            SELECT B.*, l.skuName 
            FROM StkPaidBills B 
            LEFT JOIN LiveSku l ON l.Code = B.ItemCode 
            LEFT JOIN GroupNbrands gb ON gb.code = l.groupNbrandCode 
            WHERE gb.productGroupCode = ?
        """
        
        params = [group_code]  # Always filter by group_code

        if brand_code:  # Only filter by brand_code if provided
            query += " AND gb.BrandCode = ?"
            params.append(brand_code)

        result = db.get_data(query=query, data=params)  
        return result
    
    @classmethod
    def brands(Self,product_group_code):
        query = """Select brandCode as Code,  BrandName from GroupNbrands Where ProductGroupCode = ?"""
        data  = [product_group_code]

        return db.get_data(query=query,data=data)
    
    @classmethod
    def brand_sales_this_month(self,product_group_code):
        query = """select sum(SS.GrossAmt) as totalGrossAmt,sum(SS.COGS) as totalCogs,sum(ss.MRPTotal) as totalMRPTotal,sum(Qty) as TotalQtySold,gb.brandName,gb.brandCode,gb.code as groupbrandCode,gb.groupName from skuSalesThisMonth SS left join GroupNbrands gb ON gb.Code = SS.GroupNBrandCode Where gb.productGroupCode = ?
        Group By gb.brandName,gb.brandCode,gb.code,gb.groupName"""
        
        data = [product_group_code]

        result = db.get_data(data=data,query=query)

        return result

    @classmethod
    def brand_sales_prev_month(cls,product_group_Code):
        query = """select sum(SS.GrossAmt) as totalGrossAmt,sum(SS.COGS) as totalCogs,sum(ss.MRPTotal) as totalMRPTotal,sum(Qty) as TotalQtySold,gb.brandName,gb.brandCode,gb.code as groupbrandCode,gb.groupName from skuSalesPrevMonth SS left join GroupNbrands gb ON gb.Code = SS.GroupNBrandCode Where gb.productGroupCode = ?
        Group By gb.brandName,gb.brandCode,gb.code,gb.groupName"""
        
        data = [product_group_Code]

        result = db.get_data(data=data,query=query)

        return result
    
    @classmethod
    def get_brand_sales_data(cls, brands, prev_sales, this_month_sales):

        result = []
        for brand in brands:
            # Get previous month's sales for this brand
            prev_sale = next((s for s in prev_sales if s["brandCode"] == brand["Code"]), None)
            
            # Get current month's sales for this brand
            current_sale = next((s for s in this_month_sales if s["brandCode"] == brand["Code"]), None)

            # Structure the sales data
            result.append({
                "BrandCode": brand["Code"],
                "BrandName": brand["BrandName"],
                "PrevMonthSales": prev_sale["totalGrossAmt"] if prev_sale else 0,
                "PrevMonthTotalCogs": prev_sale["totalCogs"] if prev_sale else 0,
                "PrevMonthTotalQtySold": prev_sale["TotalQtySold"] if prev_sale else 0,
                "CurrentMonthSales": current_sale["totalGrossAmt"] if current_sale else 0,
                 "CurrentMonthTotalCogs": current_sale["totalCogs"] if prev_sale else 0,
                "CurrentMonthTotalQtySold": current_sale["TotalQtySold"] if prev_sale else 0,
            })

        return result

        
    @classmethod
    def get_basic_gp_info(cls,product_gp_code):
        query = """select * from ProductGroups Where Code = ?"""

        result = db.get_data(query=query,data=[product_gp_code])

        return result

    

    @classmethod
    def detail(cls,product_group_code,brand_code=None):
        brands = cls.brands(product_group_code=product_group_code)
        prev_sales = cls.brand_sales_prev_month(product_group_Code=product_group_code)
        cur_sales = cls.brand_sales_this_month(product_group_code=product_group_code)
        result = {
            "info":cls.get_basic_gp_info(product_gp_code=product_group_code),
            "Skus":cls.sku_list(product_group_code=product_group_code),
            "Recentvendors":cls.recent_vendors(group_code=product_group_code,brand_code=brand_code),
            'recentVendorsWhoPaidWithouClearingStock':cls.recent_paid_vendors(group_code=product_group_code,brand_code=brand_code),
            "brands":cls.get_brand_sales_data(brands=brands,prev_sales=prev_sales,this_month_sales=cur_sales),
                  }
        
        return result
    

    @classmethod
    def group_list(cls):
        query = """"""

    

