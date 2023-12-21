from django.urls import path
from VMS_app import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('vendors/', views.CreateVendorList.as_view()),
    path('vendor_details/<int:pk>/', views.UpdateVendor.as_view()),
    path('vendors/delete/<int:pk>/', views.DeleteVendor.as_view()),
    path('purchase_orders/', views.CreatePurchaseOrderList.as_view()),
    path('purchase_orders/<int:pk>/', views.UpdatePurchaseOrder.as_view()),
    path('purchase_orders/delete/<int:pk>/', views.DeletePurchaseOrder.as_view()),
    path('purchase_orders/<int:pk>/acknowledge/', views.AcknowledgeUpdate.as_view()),
    path('vendors/<int:pk>/performance/', views.VendorPerformance.as_view()),
    path('apitoken/', obtain_auth_token),

]