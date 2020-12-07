from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.forms.models import model_to_dict
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product, CartItem, Cart, BillingAddress, ShippingAddress, ContactInfo, Coupon
from .forms import CheckoutForm, ContactForm, ShippingForm
from django.views.generic import View, TemplateView, ListView, DetailView, FormView

import json
from django.utils import timezone
# Create your views here.


# Get the current order depending on if the user is authenticated or not.
# Returns None or the current order.
def get_current_order(request, createOrder=False):
    current_order = None
    if request.user.is_authenticated:
        if createOrder:
            current_order, created = Cart.objects.get_or_create(
                user=request.user, ordered=False)
        else:
            order_query = Cart.objects.filter(user=request.user, ordered=False)
            if order_query.exists():
                current_order = order_query[0]
    else:
        if "cart" in request.session:
            current_order = Cart.objects.get(id=request.session["cart"])
        else:
            if createOrder:
                current_order = Cart.objects.create(ordered=False)
                request.session["cart"] = current_order.id

    return current_order


class ProductList(ListView):
    model = Product
    context_object_name = "products"
    template_name = "store/product-list.html"


class ProductDetail(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "store/product-page.html"


class ShoppingCart(TemplateView):
    model = Cart
    template_name = "store/shopping-cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_cart = get_current_order(self.request)
        if current_cart:
            context["cart"] = current_cart
            subtotal = current_cart.get_subtotal()
            context["subtotal"] = subtotal
        return context


class coupon_form(View):
    def post(self, *args, **kwargs):
        response = {}
        coupon_code = self.request.POST.dict()["coupon"] or None
        coupons = Coupon.objects.filter(coupon_code=coupon_code)

        current_order = get_current_order(self.request)
        if coupons.exists():
            for coupon in coupons:
                if(coupon.is_valid()):
                    valid_coupon = coupon
                    current_order.coupon = valid_coupon
                    current_order.save()
                    response["coupon"] = valid_coupon.coupon_code
                    response["discount"] = str(valid_coupon.discount)
                    break
                else:
                    response["error"] = "Coupon Code " + \
                        str(coupon) + " is no longer valid!"
        else:
            response["error"] = "No Valid Coupon Code: " + coupon_code
        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )


class contact_form(View):
    def post(self, *args, **kwargs):
        response = {}
        form = ContactForm(self.request.POST.dict() or None)
        # current_order = Cart.objects.filter(user=self.request.user, ordered=False)
        current_order = get_current_order(self.request)
        if current_order:
            if form.is_valid():
                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                email = form.cleaned_data.get("email")
                phone_number = form.cleaned_data.get("phone_number")
                contact_info, created = ContactInfo.objects.get_or_create(
                    first_name=first_name,
                    last_name=last_name,
                    email_address=email,
                    phone_number=phone_number
                )
                current_order.contact = contact_info
                current_order.save()
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
        current_order = get_current_order(self.request)
        if current_order:
            if form.is_valid():
                address1 = form.cleaned_data.get("address1")
                address2 = form.cleaned_data.get("address2")
                country = form.cleaned_data.get("country")
                state = form.cleaned_data.get("state")
                city = form.cleaned_data.get("city")
                zipcode = form.cleaned_data.get("zipcode")
                same_billing_address = form.cleaned_data.get(
                    "same_billing_address")
                shipping_address, created = ShippingAddress.objects.get_or_create(
                    address1=address1,
                    address2=address2,
                    country=country,
                    state=state,
                    city=city,
                    zipcode=zipcode
                )

                if same_billing_address:
                    billing_address, created = BillingAddress.objects.get_or_create(
                        address1=address1,
                        address2=address2,
                        country=country,
                        state=state,
                        city=city,
                        zipcode=zipcode
                    )
                    current_order.billing_address = billing_address
                else:
                    current_order.billing_address = None

                current_order.shipping_address = shipping_address
                current_order.save()
                response["shipping-text"] = shipping_address.__str__()
                shipping_address = model_to_dict(shipping_address)
                shipping_address["country"] = shipping_address["country"].code

                response["billing"] = (
                    current_order.billing_address is not None)
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
    template_name = "store/checkout-page.html"

    def get(self, request, *args, **kwargs):
        order = get_current_order(request)
        if order.ready_for_payment():
            subtotal = sum([(item.quantity * item.product.price)
                            for item in order.items.all()])
            return render(request,
                          'store/checkout-page.html',
                          {'order': order,
                           'subtotal': subtotal,
                           'form': CheckoutForm()})
        else:
            return redirect('shopping-cart')


class CheckoutSuccessPage(DetailView):
    model = Cart
    context_object_name = "order"
    template_name = "store/checkout-success.html"

    def post(self, *args, **kwargs):
        response = {}
        current_order = get_current_order(self.request)
        if current_order:
            response["success"] = True
            tmp = json.loads(self.request.POST.get('value'))
            # tmp_pretty = json.dumps(tmp, indent=2)
            current_order.paypal_information = tmp
            current_order.ordered = True
            current_order.ordered_date = timezone.now()
            current_order.save()
            if "cart" in self.request.session:
                print("Order placed! Removing id from sessions")
                del self.request.session["cart"]
        else:
            response["error"] = "No valid order exists!"
        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )


def add_to_cart(request, pk, slug):
    product = get_object_or_404(Product, id=pk, slug=slug)
    current_order = get_current_order(request, True)

    if not request.user.is_authenticated:
        cart_item, cart_item_created = CartItem.objects.get_or_create(
            product=product, order=current_order)
    else:
        cart_item, cart_item_created = CartItem.objects.get_or_create(
            user=request.user, product=product, order=current_order)

    if cart_item_created:
        current_order.items.add(cart_item)
    else:
        cart_item.quantity += 1
        cart_item.save()
    # return HttpResponseRedirect(request.path_info)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_from_cart(request, pk, slug):
    product = get_object_or_404(Product, id=pk, slug=slug)

    current_order = get_current_order(request, True)

    if not request.user.is_authenticated:
        cart_item, cart_item_created = CartItem.objects.get_or_create(
            product=product, order=current_order)
    else:
        cart_item, cart_item_created = CartItem.objects.get_or_create(
            user=request.user, product=product, order=current_order)

    if cart_item.quantity <= 1:
        cart_item.delete()
    else:
        cart_item.quantity -= 1
        cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return HttpResponseRedirect(request.path_info)
