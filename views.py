from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import UserProfile, Product, Cart, CartItem, Order, OrderItem
from .serializers import (
    UserProfileSerializer, ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer, SellerProfileSerializer, BuyerProfileSerializer
)
from .permissions import IsBuyer, IsSeller
from datetime import datetime, timedelta

class DiscountAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'محصول یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        discount = request.data.get('discount')
        discount_end = request.data.get('discount_end')
        if discount is None or discount_end is None:
            return Response({'error': 'به درستی وارد کنید.'}, status=status.HTTP_400_BAD_REQUEST)

        product.discount = discount
        product.discount_end = discount_end
        product.save()
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class DailyDiscountAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'محصول یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        daily_discount = request.data.get('daily_discount')
        if daily_discount is None:
            return Response({'error': 'درست وارد کنید.'}, status=status.HTTP_400_BAD_REQUEST)

        today = datetime.now() # انقضای روزانه
        end_of_day = datetime(today.year, today.month, today.day, 23, 59, 59)
        product.daily_discount = daily_discount
        product.daily_discount_end = end_of_day
        product.save()
        serializer = ProductSerializer(product)
        return Response(serializer.data)

# ویوی پروفایل فروشنده
class SellerProfileAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def get(self, request):
        user = request.user
        serializer = SellerProfileSerializer(user)
        return Response(serializer.data) 

# ویوی پروفایل خریدار
class BuyerProfileAPIView(APIView):
    
    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):
        user = request.user
        serializer = BuyerProfileSerializer(user)
        return Response(serializer.data)


class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class CartAPIView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]
 
    def get(self, request):
        cart, created = Cart.objects.get_or_create(buyer=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        cart, created = Cart.objects.get_or_create(buyer=request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += int(quantity)
        cart_item.save()
        return Response({'status': 'اضافه شد.'})

    def delete(self, request):
        cart = request.user.cart
        product_id = request.data.get('product_id')
        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if cart_item:
            cart_item.delete()
        return Response({'status': 'حذف شد.'})

class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def post(self, request):
        cart = request.user.cart
        if not cart.items.exists():
            return Response({'error': 'خالی است.'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.product.price * item.quantity for item in cart.items.all())
        if request.user.wallet_balance < total_price:
            return Response({'error': 'موجودی کافی نیست.'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(buyer=request.user, total_price=total_price)
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart.items.all().delete()
        request.user.wallet_balance -= total_price
        request.user.save()
        return Response({'status': 'order placed', 'order_id': order.id})

# ویوی فروشنده
class SellerProductAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def get(self, request):
        products = Product.objects.filter(seller=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)