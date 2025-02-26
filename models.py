from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


# کاربر
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    profile_pic = models.ImageField(upload_to='pfp/', blank=True)
    phone_number = models.CharField(max_length=11, blank=True)
    check_signup = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

# محصولات
class Product(models.Model):
    name = models.CharField(max_length=100) #نام
    description = models.TextField() #توضیحات
    picture = models.ImageField(upload_to='products/', blank=True) #عکس
    price = models.DecimalField(max_digits=10, decimal_places=2) #قیمت
    stock = models.IntegerField() #موجودی
    created_at = models.DateTimeField(auto_now_add=True) #تاریخ ثبت محصول
    updated_at = models.DateTimeField(auto_now=True) #تاریخ آپدیت

    def __str__(self):
        return self.name

# سبد خرید
class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart') #کاربر
    created_at = models.DateTimeField(auto_now_add=True) # تاریخ ساخت سبد خرید

    def __str__(self):
        return f"Cart of {self.user.username}"

# اقلام سبد خرید
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items') #سبد خرید
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #محصول
    quantity = models.PositiveIntegerField(default=1) #تعداد

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"

# ثبت سفارش
class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders') #کاربر
    created_at = models.DateTimeField(auto_now_add=True) # تاریخ ثبت سفارش
    total_price = models.DecimalField(max_digits=10, decimal_places=2) # قیمت کل سفارش

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    
# اقلام سفارش
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items') #سفارش
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #محصول 
    quantity = models.PositiveIntegerField() #تعداد
    price = models.DecimalField(max_digits=10, decimal_places=2) #قیمت 

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"