from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import Product, CartItem, Cart, BillingAddress, ShippingAddress
from .forms import CheckoutForm
from django.views.generic import TemplateView, ListView, DetailView, FormView
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

class CheckoutPage(FormView):
    form_class = CheckoutForm
    template_name= "store/checkout-page.html"
        
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        current_order = Cart.objects.filter(user=self.request.user, ordered=False)
        if current_order.exists():
            current_order = current_order[0]
            if form.is_valid():
                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                email = form.cleaned_data.get("email")
                address1 = form.cleaned_data.get("address1")
                address2 = form.cleaned_data.get("address2")
                country = form.cleaned_data.get("country")
                state = form.cleaned_data.get("state")
                zipcode = form.cleaned_data.get("zipcode")
                same_billing_address = form.cleaned_data.get("same_billing_address")
                payment_option = form.cleaned_data.get("payment_option")
                billing_address = BillingAddress(
                    user = self.request.user,
                    address1 = address1,
                    address2 = address2,
                    country = country,
                    state = state,
                    zipcode = zipcode
                )
                shipping_address = ShippingAddress(
                    user = self.request.user,
                    address1 = address1,
                    address2 = address2,
                    country = country,
                    state = state,
                    zipcode = zipcode
                )
                billing_address.save()
                shipping_address.save()
                current_order.billing_address = billing_address
                current_order.shipping_address = shipping_address
                current_order.save()
                #TODO redirect to a payment method 
                return redirect('payment')
            else:
                messages.warning(self.request,"Invalid form")
                return redirect('checkout')
        else:
            return redirect('checkout')
        return redirect('home')

class PaymentPage(TemplateView):
    #Check if given cart and name, billing/ shipping address is filled out. 
    template_name = "store/payment-page.html"
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Cart, user=request.user, ordered=False)
        if order.ready_for_payment():
            return render(request, 'store/payment-page.html', {'order': order})
        else:
            return redirect('shopping-cart')

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