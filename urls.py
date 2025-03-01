from django.urls import path
from .views import (
    ProductListAPIView, CartAPIView, OrderAPIView, SellerProductAPIView, SellerProfileAPIView, BuyerProfileAPIView, DiscountAPIView, DailyDiscountAPIView
)

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('order/', OrderAPIView.as_view(), name='order'),
    path('seller/products/', SellerProductAPIView.as_view(), name='seller-products'),
    path('seller/profile/', SellerProfileAPIView.as_view(), name='seller-profile'),
    path('buyer/profile/', BuyerProfileAPIView.as_view(), name='buyer-profile'),
    path('admin/set-regular-discount/<int:product_id>/', DiscountAPIView.as_view(), name='set-regular-discount'),
    path('admin/set-daily-discount/<int:product_id>/', DailyDiscountAPIView.as_view(), name='set-daily-discount'),
]
