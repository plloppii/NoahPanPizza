from .models import Cart

#Fetch the current cart of the user if it exists.
def current_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        if cart.exists():
            total_items = sum([quat.quantity for quat in cart[0].items.all()])
            return {"total_items": total_items}
    return {}

