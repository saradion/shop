from rest_framework import serializers
from .models import UserProfile, Product, Cart, CartItem, Order, OrderItem

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'is_seller', 'is_buyer', 'wallet_balance', 'bank_info']

class ProductSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'name', 'picture', 'description', 'price', 'earnest', 'discount', 'discount_end', 'daily_discount',
            'daily_discount_end', 'product_type', 'age', 'sex', 'weight', 'stock',
            'created_at', 'updated_at', 'final_price'
        ]
    def get_final_price(self, obj): #محاسبه قیمت نهایی بعد از اعمال تخفیف ها
        return obj.final_price


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'buyer', 'items', 'created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'buyer', 'items', 'total_price', 'earnest', 'created_at']


class SellerProfileSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'is_seller', 'is_buyer', 'wallet_balance', 'products']


class BuyerProfileSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'is_seller', 'is_buyer', 'wallet_balance', 'cart', 'orders']