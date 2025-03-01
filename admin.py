from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'discount_end', 'daily_discount', 'daily_discount_end')
    list_editable = ('discount', 'discount_end', 'daily_discount', 'daily_discount_end')

admin.site.register(Product, ProductAdmin)