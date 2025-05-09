from ...models.Models import GroupNbrands as GroupNbrandsModel, LiveSku, productCategory
from .Groups import Group
from .Items import Items
from ...Core import db

class Category(productCategory):

    def recent_vendors(self, groups):
        codes_tuple = list(d["Code"] for d in groups)

        if not codes_tuple:
            return []  # Return empty list if no codes are available

        # For SQL Server, we need to use parentheses around the placeholders
        placeholders = ", ".join(["?"] * len(codes_tuple))

        query = f"""SELECT B.*, l.skuName 
                FROM StkBills B 
                LEFT JOIN LiveSku l ON l.Code = B.ItemCode 
                LEFT JOIN GroupNbrands gb ON gb.code = l.groupNbrandCode 
                WHERE gb.productGroupCode IN ({placeholders})"""

        data = codes_tuple
        result = db.get_data(query=query, data=data)

        return result
    
    def recent_paid_vendors(self, groups):
        codes_tuple = list(d["Code"] for d in groups)

        if not codes_tuple:
            return []  # Return empty list if no codes are available

        # Add parentheses around the placeholders
        placeholders = ", ".join(["?"] * len(codes_tuple))
        query = f"""SELECT B.*, l.skuName 
                FROM StkPaidBills B 
                LEFT JOIN LiveSku l ON l.Code = B.ItemCode 
                LEFT JOIN GroupNbrands gb ON gb.code = l.groupNbrandCode 
                WHERE gb.productGroupCode IN ({placeholders})"""

        data = codes_tuple
        result = db.get_data(query=query, data=data)

        return result
    
    def get_cm_sales(self, groups):
        codes_tuple = list(d["Code"] for d in groups)

        if not codes_tuple:
            return []  # Return empty list if no codes are available

        # Add parentheses around the placeholders
        placeholders = ", ".join(["?"] * len(codes_tuple))

        query = f"""SELECT 
                    SUM(SS.GrossAmt) AS totalGrossAmt,
                    SUM(SS.COGS) AS totalCogs,
                    SUM(SS.MRPTotal) AS totalMRPTotal,
                    SUM(Qty) AS TotalQtySold,
                    gb.brandName,
                    gb.code AS groupbrandCode,
                    gb.groupName,
                    gb.ProductGroupCode 
                FROM skuSalesThisMonth SS 
                LEFT JOIN GroupNbrands gb ON gb.Code = SS.GroupNBrandCode 
                WHERE gb.productGroupCode IN ({placeholders})
                GROUP BY gb.brandName, gb.code, gb.groupName, gb.ProductGroupCode"""

        data = codes_tuple
        result = db.get_data(query=query, data=data) 

        return result
        
    def get_prev_m_sales(self, groups):
        codes_tuple = list(d["Code"] for d in groups)

        if not codes_tuple:
            return []  # Return empty list if no codes are available

        # Parentheses were already correct in this function
        placeholders = ", ".join(["?"] * len(codes_tuple))

        query = f"""SELECT 
                    SUM(SS.GrossAmt) AS totalGrossAmt, 
                    SUM(SS.COGS) AS totalCogs, 
                    SUM(SS.MRPTotal) AS totalMRPTotal, 
                    SUM(Qty) AS TotalQtySold, 
                    gb.brandName, 
                    gb.code AS groupbrandCode, 
                    gb.groupName, 
                    gb.ProductGroupCode 
                FROM skuSalesPrevMonth SS 
                LEFT JOIN GroupNbrands gb ON gb.Code = SS.GroupNBrandCode 
                WHERE gb.productGroupCode IN ({placeholders}) 
                GROUP BY gb.brandName, gb.code, gb.groupName, gb.ProductGroupCode"""

        data = codes_tuple
        print("Executing Query:", query)
        print("With Data:", data)

        result = db.get_data(query=query, data=data)

        return result

    def detail(self):

        result = self.serialize()
        result['groups'] = Items.get_groups(category_code=self.Code)
        result['brands'] = Group.get_brands_by_product_ategory_code(product_category_code=self.Code)
        result['recentVendors'] = self.recent_vendors(groups=result['groups'])
        result['recentVendorsWhoPaidWithouClearingStock'] = self.recent_paid_vendors(groups=result['groups'])
        result['GroupNbrandWiseSalesThisMonth'] = self.get_cm_sales(groups=result['groups'])
        result['GroupNbrandWiseSalesPrevMonth'] = self.get_prev_m_sales(groups=result['groups'])

        return result