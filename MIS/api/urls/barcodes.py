from django.urls import path
from ..view.TypedBarcodes import (
    GetTYpedBarcodeMetrics,
    GetBrowsedEanItems,
    GetManuallyEnteredBArcodes,
    GetBrowsedPrivateLabels,
    GetBrowsedRepackItems,
    GetUnregisteredEans
)

urlpatterns = [
    path("barcode/metrics/", GetTYpedBarcodeMetrics.as_view(), name="typed-barcode-metrics"),
    path("barcode/ean-items/", GetBrowsedEanItems.as_view(), name="browsed-ean-items"),
    path("barcode/manually-entered/", GetManuallyEnteredBArcodes.as_view(), name="manually-entered-barcodes"),
    path("barcode/private-labels/", GetBrowsedPrivateLabels.as_view(), name="browsed-private-labels"),
    path("barcode/repack-items/", GetBrowsedRepackItems.as_view(), name="browsed-repack-items"),
    path("barcode/unregistered-eans/", GetUnregisteredEans.as_view(), name="unregistered-eans"),
]
