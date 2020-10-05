from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.forms.models import model_to_dict
from django.contrib import messages
from django.http import HttpResponse
from .models import Product, CartItem, Cart, BillingAddress, ShippingAddress, ContactInfo
from .forms import CheckoutForm, ContactForm, ShippingForm
from django.views.generic import View, TemplateView, ListView, DetailView, FormView

import json
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

class contact_form(View):
    def post(self, *args, **kwargs):
        response = {}
        form = ContactForm(self.request.POST.dict() or None)
        current_order = Cart.objects.filter(user=self.request.user, ordered=False)
        if(current_order.exists()):
            current_order = current_order[0]
            if form.is_valid():
                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                email = form.cleaned_data.get("email")
                phone_number = form.cleaned_data.get("phone_number") 
                contact_info = ContactInfo(
                    first_name = first_name,
                    last_name = last_name,
                    email_address = email,
                    phone_number = phone_number 
                )
                contact_info.save()
                current_order.contact = contact_info
                response["contact-text"] = contact_info.__str__()
                response["contact"] = json.dumps(model_to_dict(contact_info))
            else:
                response["error"] = "Something isn't filled out correctly!"
        else:
            response["error"] = "No valid order exists!"
        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )

class shipping_form(View):
    def post(self, *args, **kwargs):
        response = {}
        form = ShippingForm(self.request.POST.dict() or None)
        current_order = Cart.objects.filter(user=self.request.user, ordered=False)
        if(current_order.exists()):
            current_order = current_order[0]
            if form.is_valid():
                address1 = form.cleaned_data.get("address1")
                address2 = form.cleaned_data.get("address2")
                country = form.cleaned_data.get("country")
                state = form.cleaned_data.get("state")
                city = form.cleaned_data.get("city")
                zipcode = form.cleaned_data.get("zipcode")
                same_billing_address = form.cleaned_data.get("same_billing_address")
                shipping_address = ShippingAddress(
                    address1 = address1,
                    address2 = address2,
                    country = country,
                    state = state,
                    city = city,
                    zipcode = zipcode
                )
                shipping_address.save()

                if same_billing_address:
                    billing_address = BillingAddress(
                        address1 = address1,
                        address2 = address2,
                        country = country,
                        state = state,
                        city = city,
                        zipcode = zipcode
                    )
                    billing_address.save()
                    current_order.billing_address = billing_address
                else:
                    current_order.billing_address = None

                current_order.shipping_address = shipping_address
                current_order.save()
                response["shipping-text"] = shipping_address.__str__()
                shipping_address = model_to_dict(shipping_address)
                shipping_address["country"] = shipping_address["country"].code

                response["billing"] = (current_order.billing_address is not None)
                response["shipping"] = json.dumps(shipping_address)

            else:
                response["error"] = "Something isn't filled out correctly!"
        else:
            response["error"] = "No valid order exists!"
        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )
        

class CheckoutPage(FormView):
    form_class = CheckoutForm
    template_name= "store/checkout-page_test.html"
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Cart, user=request.user, ordered=False)
        if order.ready_for_payment():
            subtotal = sum([ (item.quantity*item.product.price) for item in order.items.all()]) 
            return render(request, 'store/checkout-page_test.html', {'order': order, 'subtotal': subtotal, 'form': CheckoutForm()})
        else:
            messages.error(self.request,"Order already placed")
            return redirect('shopping-cart')

class CheckoutSuccessPage(TemplateView):
    template_name = "store/checkout-success.html"
    def post(self, *args, **kwargs):
        current_order = Cart.objects.filter(user=self.request.user, ordered=False)
        if(current_order.exists()):
            current_order = current_order[0]
            
        else:
            response["error"] = "No valid order exists!"

    # def get(self, request, *args, **kwargs):


class PaymentPage(TemplateView):
    #Check if given cart and name, billing/ shipping address is filled out. 
    template_name = "store/payment-page.html"
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Cart, user=request.user, ordered=False)
        if order.ready_for_payment():
            subtotal = sum([ (item.quantity*item.product.price) for item in order.items.all()]) 
            return render(request, 'store/payment-page.html', {'order': order, 'subtotal': subtotal})
        else:
            messages.error(self.request,"Order already placed")
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