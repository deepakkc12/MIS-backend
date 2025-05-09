from django.urls import path
from ..view.Inventory import (
    GetCategoris,
    GetSubGroups,
    GetGroups,
    GetsubCategory,
    GetGoupNBrands,
    GetLiveSkus,
    GetLiveSubSkus,
 GetSKuByCustomerLevels,
 GetSkuDetails,
 GetSkuByGroup,
 GetGroupNBRancdDetails,
 GetDamageCartSummery,
 GetDamageCartDetailsByVedor,
 GetBrandsOfGroup,
 GetCetegoryDetails,
 GetRecentVendorsList,
 GetVendorDetails,
GetBrandDetails
)

urlpatterns = [
    path("inventory/categories/", GetCategoris.as_view(), name="get-categories"),
    path("inventory/sub-groups/", GetSubGroups.as_view(), name="get-sub-groups"),
    path("inventory/groups/", GetGroups.as_view(), name="get-groups"),
    path("inventory/sub-category/", GetsubCategory.as_view(), name="get-sub-category"),
    path("inventory/group-brands/", GetGoupNBrands.as_view(), name="get-group-brands"),
    path("inventory/live-skus/", GetLiveSkus.as_view(), name="get-live-skus"),
    path("inventory/live-sub-skus/", GetLiveSubSkus.as_view(), name="get-live-sub-skus"),
    path("inventory/cLevel-choises/", GetSKuByCustomerLevels.as_view(), name="get-customer-Level-choises"),
    path("inventory/sku-details/", GetSkuDetails.as_view(), name="get-sku-details"),
    path("inventory/group-details/", GetGroupNBRancdDetails.as_view(), name="get-sku-details"),
    path("inventory/category-details/", GetCetegoryDetails.as_view(), name="get-sku-details"),
    path("inventory/sku-list/", GetSkuByGroup.as_view(), name="get-sku-list"),
    path("inventory/brands/", GetBrandsOfGroup.as_view(), name="get-sku-list"),

    path("inventory/damage-cart-summery/", GetDamageCartSummery.as_view(), name="get-sku-list"),
    path("inventory/damage-cart-details/", GetDamageCartDetailsByVedor.as_view(), name="get-sku-list"),
    path("inventory/recent-vendors/", GetRecentVendorsList.as_view(), name="get-sku-list"),
    path("inventory/vendor-details/", GetVendorDetails.as_view(), name="get-sku-list"),
    path("inventory/brand-details/", GetBrandDetails.as_view(), name="get-sku-list"),

    # path("inventory/group-details/", GetGroupdetails.as_view(), name="get-sku-list"),



    

    # path("inventory/sku-list/", GetSkuByGroup.as_view(), name="get-sku-list"),

]
