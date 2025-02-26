from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, ProductViewSet, CartViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'products', ProductViewSet)
router.register(r'carts', CartViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
