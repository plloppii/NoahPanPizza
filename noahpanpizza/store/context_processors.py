from .models import Cart
from django.core import serializers
from .views import get_serialized_cart, deserialize_cart
from .models import get_cart_quantity
# Fetch the current cart of the user if it exists.


def current_cart(request):
    total_items = 0
    #if not request.user.is_authenticated:
    if "cart" in request.session:
        total_items= get_cart_quantity(deserialize_cart(get_serialized_cart(request)))
    #else:
    #    cart = Cart.objects.filter(user=request.user, ordered=False)
    #    if cart.exists():
    #        total_items = cart[0].get_total_items()
    if total_items:
        return {"total_items": total_items}
    return {}
