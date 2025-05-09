from datetime import datetime
from rest_framework.views import APIView
from ..services.Inventory.Items import Items
from ..utils.response import ResponseHandler
from ..services.Inventory.LiveSku import Sku
from ..services.Inventory.Groups import Group
from ..services.Inventory.Category import Category
from ..services.Inventory.DamegeCart import DamageCart
from ..services.Inventory.Vendors import Vendors
from ..services.Inventory.Brand import Brands
from ..services.Inventory.GroupNBrand import GroupNbrands




class GetCategoris(APIView):
    def get(self,request):

        category = Items.category()

        result = category.serialized_list()

        return ResponseHandler.success(data=result)

class GetSubGroups(APIView):
    def get(self,request):

        sub_groups = Items.sub_groups

        result = sub_groups.serialized_list()

        return ResponseHandler.success(data=result)

class GetGroups(APIView):
    def get(self,request):

        category = request.GET.get("category",None)

        result = Items.get_groups(category_code=category)

        return ResponseHandler.success(data=result)
    
class GetsubCategory(APIView):
    def get(self,request):

        sub_category = Items.sub_category()

        result = sub_category.serialized_list()

        return ResponseHandler.success(data=result)
    
class GetGoupNBrands(APIView):
    def get(self,request):

        group_n_brands = Items.group_n_brands()

        result = group_n_brands.serialized_filtered_list()

        # new_result = []

        # l_result = []

        # for res in result:
        #     if res['ProductGroupCode'] == 0 :
        #         new_result.append(res)
        #     else:
        #         l_result.append(res)

        return ResponseHandler.success(data=result)
    
class GetLiveSkus(APIView):
    def get(self,request):

        gr_code = request.GET.get('group')

        if not gr_code:
            return ResponseHandler.bad_request('group code required')
        
        result = Sku.get_group_skus(group_code=gr_code)

        return ResponseHandler.success(data=result)
    
class GetLiveSubSkus(APIView):
    def get(self,request):

        live_sub_sku = Items.live_sub_sku

        result = live_sub_sku.serialized_list()

        return ResponseHandler.success(data=result)
    
class GetSKuByCustomerLevels(APIView):
    def get(self,request):
        result = Items.get_cr_level_choises()

        # result = Sku.list()

        # result = len(result)

        return ResponseHandler.success(data=result)
    
class GetSkuDetails(APIView):
    def get(self,request):
        sku_code = request.GET.get('sku')
        if not sku_code:
            return ResponseHandler.bad_request("sku code required")
        
        sku = Sku.find_by_id(id=sku_code)

        if not sku:
            return ResponseHandler.not_found("Sku not found")
        
        result = sku.details()

        return ResponseHandler.success(data=result)
    
class GroupDetails(APIView):
    def get(self,request):
        group_code = request.GET.get('group')

class GetSkuByGroup(APIView):
    def get(self,request):

        gr_code = request.GET.get('group')

        if not gr_code:
            return ResponseHandler.bad_request('group code required')
        
        sku_list = Sku.get_grop_wise_sku(prGrCode=gr_code)

        result = []

        for sku in sku_list:

            sku_obj = Sku()

            sku_obj.code =sku['skuCode']

            detail = sku_obj.details()

            # print(detail)

            result.append(detail)

        # result = Items.groups.serialized_filtered_list(Code=28121109)

        return ResponseHandler.success(data=result)
    
class GetGroupNBRancdDetails(APIView):

    def get(Self,request):

        product_group_code = request.GET.get("productGpCode")

        brand_code = request.GET.get("productbrandCode",None)

        if not brand_code:
            result = Group.detail(product_group_code=product_group_code,brand_code=brand_code)
        else:
            result = GroupNbrands.detail(product_group_code=product_group_code,brand_code=brand_code)

        return ResponseHandler.success(data=result)


class GetBrandsOfGroup(APIView):
    def get(Self,request):

        product_group_code = request.GET.get('productGroup')

        result = Group.get_brands_by_productGroupCode(product_group_code=product_group_code)

        return ResponseHandler.success(data=result)
    

class GetCetegoryDetails(APIView):

    def get(Self,request):

        category_code = request.GET.get('category')

        category = Category.find_by_id(category_code)

        result = category.detail()

        return ResponseHandler.success(data=result)
        

class GetDamageCartSummery(APIView):
    def get(self,request):
        result = DamageCart.get_cart_summery_by_vendor()

        return ResponseHandler.success(data=result)
    
class GetDamageCartDetailsByVedor(APIView):
    def get(Self,request):
        vendor_code = request.GET.get('vendor')

        if not vendor_code:
            return ResponseHandler.bad_request('vendor code required')
        
        result = DamageCart.get_details_by_vendor_code(vendor_code=vendor_code)

        return ResponseHandler.success(data=result)
    
class GetRecentVendorsList(APIView):
    def get(self,request):

        result = Vendors.get_recent_vendors()

        return ResponseHandler.success(data=result)
    

class GetVendorDetails(APIView):
    def get(self,request):
        
        vendor_code = request.GET.get('vendor')

        if not vendor_code:
            return ResponseHandler.bad_request("vendor code required")
        
        result = Vendors.get_vendor_details(vendor_code=vendor_code)

        return ResponseHandler.success(data=result)
    
class GetGroupdetails(APIView):
    def get(self,request):



        pass    


class GetBrandDetails(APIView):
    def get(self,request):
        brand_code = request.GET.get("brand")

        result = Brands.get_details(brand_code=brand_code)

        return ResponseHandler.success(data=result)
    
