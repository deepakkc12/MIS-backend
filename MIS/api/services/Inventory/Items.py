from ...models.Models import LiveSku,LiveSubSKu,productCategory,productBrands,productGroups,productsubCategory,productSubGroup,GroupNbrands

from ...Core import db
class Items:

    category = productCategory
    live_sku = LiveSku
    live_sub_sku = LiveSubSKu
    brands = productBrands
    groups = productGroups
    sub_groups = productSubGroup
    sub_category = productsubCategory
    group_n_brands = GroupNbrands


    @classmethod
    def get_groups(cls,category_code=None):

        query = """SELECT * from productGroups"""
        data = []
        if category_code:
            query+=" WHERE ProductCategoryCode = ? And COde in (select ProductGroupCode from GroupNbrands)"
            data.append(category_code)
        result = db.get_data(query=query,data=data)

        return result

    @classmethod
    def get_live_sku(cls,group_code=None):

        query = """SELECT * from productGroups"""
        data = []
        if group_code:
            query+=" WHERE ProductCategoryCode = ?"
            data.append(group_code)
        result = db.get_data(query=query,data=data)

        return result

        
        

    @classmethod
    def get_live_skus(cls):
        query = """Select L.* from LiveSku L LeftJoin """


    @classmethod
    def get_cr_level_choises(cls):
        query = """select l.code,SkuName,gb.GroupName,gb.BrandName,L1ChoiceQty,L1Choice,L2ChoiceQty,L2Choice,
L3ChoiceQty,L3Choice,L4ChoiceQty,L4Choice
 from LiveSku l,GroupNbrands gb where l1choice>0
and gb.Code=l.GroupNBrandCode
 order by l1choice+L2choice desc, gb.GroupName """
        
        result = db.get_data(query=query)

        return result
    

    
    @classmethod
    def  get_group_wise_weakly_sales(cls,group_code):

        query = """select Sum(cuWSales) as cuWSales , Sum(pwSales) as pwSales From SkuStock
        Where ubDetailsCode IN (Select code from LiveSku WHere PrgrCode = ?) 
"""
        data = [group_code]

        result = db.get_data(query=query,data=data)

        return result
