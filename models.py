from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


# کاربر
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    profile_pic = models.ImageField(upload_to='pfp/', blank=True)
    phone_number = models.CharField(max_length=11, blank=True)
    check_signup = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)
    bank_info = models.CharField(max_length=24, null=True, blank=True)
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.username

# محصولات
class Product(models.Model):
    PRODUCT_TYPES = [
        ('TYPE1', 'گوساله'),
        ('TYPE2', 'گوسفند'),
        ('TYPE3', 'بز'),
    ]
    SEX_CHOICES = [
        ('M', 'نر'),
        ('F', 'ماده'),
    ]

    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100) #نام
    age = models.DecimalField(max_digits=10, decimal_places=2) #سن 
    weight = models.DecimalField(max_digits= 10, decimal_places=3) #وزن
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='M') #جنسیت
    description = models.TextField() #توضیحات
    picture = models.ImageField(upload_to='products/', blank=True) #عکس
    type = models.CharField(max_lenght= 50) # نوع
    price = models.DecimalField(max_digits=30, decimal_places=2) #قیمت
    earnest = models.DecimalField(max_digits=30, decimal_places=2) #بیعانه
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00) # تخفیف
    discount_end = models.DateTimeField(null=True, blank=True) # انقضای تخفیف
    daily_discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00) #تخفیف روز
    daily_discount_end = models.DateTimeField(null=True, blank=True) #تاریخ پایان روزانه
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPES, default='TYPE1') #نوع محصول
    stock = models.IntegerField() #موجودی
    created_at = models.DateTimeField(auto_now_add=True) #تاریخ ثبت محصول
    updated_at = models.DateTimeField(auto_now=True) #تاریخ آپدیت

    def __str__(self):
        return self.name

    @property
    def is_discount_active(self): #بررسی فعال بودن تخفیف
        if self.discount_end:
            return timezone.now() <= self.discount_end
        return False

    @property
    def is_daily_discount_active(self): # بررسی فعال بودن تخفیف روزانه
        if self.daily_discount_end:
            return timezone.now() <= self.daily_discount_end
        return False

    @property
    def final_price(self):
        prices = [self.price]  # قیمت اصلی

        if self.is_discount_active:
            prices.append(self.price * (1 - self.discount / 100)) #قیمت با تخفیف

        if self.is_daily_discount_active and self.daily_discount_price:
            prices.append(self.price * (1 - self.daily_discount_price / 100)) # قیمت با تخفیف روزانه

        return min(prices)  # قیمت نهایی کمترین

# سبد خرید
class Cart(models.Model):
    buyer = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart') #فروشنده
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