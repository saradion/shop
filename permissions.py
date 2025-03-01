from rest_framework.permissions import BasePermission

class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_buyer

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_seller