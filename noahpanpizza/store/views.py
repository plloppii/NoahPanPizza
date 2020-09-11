from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, CartItem, Cart
from django.views.generic import TemplateView, ListView, DetailView, View
# Create your views here.

class ProductList(ListView):
    model = Product
    context_object_name = "products"
    template_name= "store/product-list.html"

class ProductDetail(DetailView):
    model = Product
    context_object_name = "product"
    template_name= "store/product-page.html"

class ShoppingCart(TemplateView):
    model = Cart
    template_name = "store/shopping-cart.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            current_cart = Cart.objects.filter(user=self.request.user, ordered=False)[0]
            context["cart"] = current_cart
            subtotal = sum([ (item.quantity*item.product.price) for item in current_cart.items.all()]) 
            context["subtotal"] = subtotal
        return context 
class CheckoutPage(TemplateView):
    template_name= "store/checkout-page.html"


    # def render_to_response(self, context, **response_kwargs):
    #     if self.request.user.is_authenticated:
    #         current_cart = Cart.objects.filter(user=self.request.user, ordered=False)[0]
    #         subtotal = sum([ (item.quantity*item.product.price) for item in current_cart.items.all()])
    #         context["subtotal"] = subtotal
    #         context["cart"] = current_cart
    #     return render(self.request, self.get_template_names()[0], context)



def add_to_cart(request, pk, slug):
    if not request.user.is_authenticated:
       return redirect('product-detail', pk=pk, slug=slug)    
    product = get_object_or_404(Product, id=pk, slug=slug)

    order_item, created = CartItem.objects.get_or_create(user = request.user, product=product, ordered=False)

    #Try to find if a cart of the current user exists. 
    order_query = Cart.objects.filter(user=request.user, ordered=False)
    if(order_query.exists()):
        order = order_query[0]
        #Check if the order_item is already inside the cart.
        if order.items.filter(product=product).exists():
            order_item.quantity+=1
            order_item.save()
            # theitem = order.items.filter(item=product)[0]
            # theitem.quantity+=1
            # theitem.save()
        else:
            order.items.add(order_item)
    else:
        order = Cart.objects.create(user=request.user)
        order.items.add(order_item)
    return redirect('product-detail', pk=pk, slug=slug)   

def delete_from_cart(request, pk, slug):
    if not request.user.is_authenticated:
       return redirect('product-detail', pk=pk, slug=slug)    

    product = get_object_or_404(Product, id=pk, slug=slug)
    cart_item = CartItem.objects.filter(user=request.user, product=product, ordered=False)
    if cart_item.exists():
        cart_item.delete()
        
    return redirect('shopping-cart')    