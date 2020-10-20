from .models import Cart

#Fetch the current cart of the user if it exists.
def current_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, ordered=False)
        if cart.exists():
            return {"total_items": cart[0].get_total_items()}
    return {}

