from .models import Cart

# Fetch the current cart of the user if it exists.


def current_cart(request):
    total_items = {}
    if not request.user.is_authenticated:
        if "cart" in request.session:
            cart = Cart.objects.get(id=request.session["cart"], ordered=False)
            total_items = cart.get_total_items()
    else:
        cart = Cart.objects.filter(user=request.user, ordered=False)
        if cart.exists():
            total_items = cart[0].get_total_items()
    if total_items:
        return {"total_items": total_items}
    return {}
