from django.contrib import admin
from .models import Product, CartItem, Cart, BillingAddress, ShippingAddress

# Register your models here.

admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(BillingAddress)
admin.site.register(ShippingAddress)