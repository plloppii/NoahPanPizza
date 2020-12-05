from django.contrib import admin
from .models import Product, CartItem, Cart, ContactInfo, BillingAddress, ShippingAddress, Coupon


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "contact", "ordered_date", "ordered", "coupon"]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ["coupon_code", "expiration_date"]


admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(BillingAddress)
admin.site.register(ShippingAddress)
admin.site.register(ContactInfo)
