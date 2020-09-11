from django.urls import path, include
from .views import ProductList, ProductDetail, ShoppingCart, CheckoutPage, add_to_cart, delete_from_cart

urlpatterns = [
    path('', ProductList.as_view() , name='store'),
    path('product/<int:pk>/<slug:slug>', ProductDetail.as_view(), name='product-detail'),
    path('cart', ShoppingCart.as_view(), name='shopping-cart'),
    path('checkout', CheckoutPage.as_view(), name='checkout'),
    path('add-to-cart/<int:pk>/<slug:slug>', add_to_cart, name='add-to-cart'),
    path('delete-from-cart/<int:pk>/<slug:slug>', delete_from_cart, name='delete-from-cart')
]