from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.forms.models import model_to_dict
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product, CartItem, Cart, BillingAddress, ShippingAddress, ContactInfo, Coupon, get_cart_quantity, get_cart_subtotal
from .forms import CheckoutForm, ContactForm, ShippingForm
from django.views.generic import View, TemplateView, ListView, DetailView, FormView

import json
from django.core import serializers
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

    return current_order

# Cart Structure:
# { str(CartID) : str(CartItem) }
# Deserialize CartItem: line_item=next(serializers.deserialize("json", current_cart[product_id])).object
# Serialize CartItem: current_cart[product_id] =
# serializers.serialize("json", [line_item])

# Returns Serialized Cart Dictionary


def get_serialized_cart(request):
    if "cart" not in request.session:
        request.session["cart"] = {}
    return request.session["cart"]
# Return List of CartItems


def deserialize_cart(cart):
    return [
        next(
            serializers.deserialize(
                "json",
                item)).object for item in cart.values()]


def serialize_object(django_obj):
    return serializers.serialize("json", [django_obj])


def deserialize_object(serialized_django_obj):
    return next(serializers.deserialize("json", serialized_django_obj)).object


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
        current_cart = deserialize_cart(get_serialized_cart(self.request))
        if current_cart:
            context["cart"] = current_cart
            context["subtotal"] = get_cart_subtotal(current_cart)
        return context


class coupon_form(View):
    def post(self, *args, **kwargs):
        response = {}
        coupon_code = self.request.POST.dict()["coupon"] or None
        coupons = Coupon.objects.filter(coupon_code=coupon_code)

        if coupons.exists():
            for coupon in coupons:
                if(coupon.is_valid()):
                    response["coupon"] = coupon.coupon_code
                    response["discount"] = str(coupon.discount)
                    self.request.session["coupon"] = {
                        "code": coupon.coupon_code,
                        "discount": str(coupon.discount)
                    }
                    self.request.session.modified = True
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
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            phone_number = form.cleaned_data.get("phone_number")
            contact_info = ContactInfo(
                first_name=first_name,
                last_name=last_name,
                email_address=email,
                phone_number=phone_number
            )
            self.request.session["contact"] = serialize_object(contact_info)
            self.request.session.modified = True
            response["contact-text"] = contact_info.__str__()
            response["contact"] = json.dumps(model_to_dict(contact_info))
        else:
            response["error"] = "Something isn't filled out correctly!"
        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )


class shipping_form(View):
    def post(self, *args, **kwargs):
        response = {}
        form = ShippingForm(self.request.POST.dict() or None)
        if form.is_valid():
            address1 = form.cleaned_data.get("address1")
            address2 = form.cleaned_data.get("address2")
            country = form.cleaned_data.get("country")
            state = form.cleaned_data.get("state")
            city = form.cleaned_data.get("city")
            zipcode = form.cleaned_data.get("zipcode")
            same_billing_address = form.cleaned_data.get(
                "same_billing_address")
            shipping_address = ShippingAddress(
                address1=address1,
                address2=address2,
                country=country,
                state=state,
                city=city,
                zipcode=zipcode
            )

            billing_address = None
            if same_billing_address:
                billing_address = BillingAddress(
                    address1=address1,
                    address2=address2,
                    country=country,
                    state=state,
                    city=city,
                    zipcode=zipcode
                )
                self.request.session["billing_address"] = serialize_object(
                    billing_address)

            self.request.session["shipping_address"] = serialize_object(
                shipping_address)
            self.request.session.modified = True

            response["shipping-text"] = shipping_address.__str__()
            shipping_address = model_to_dict(shipping_address)
            shipping_address["country"] = shipping_address["country"].code

            # Store Boolean Billing is same as Shipping
            response["billing"] = (billing_address is not None)
            response["shipping"] = json.dumps(shipping_address)
        else:
            response["error"] = "Something isn't filled out correctly!"
        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )


class CheckoutPage(FormView):
    form_class = CheckoutForm
    template_name = "store/checkout-page.html"

    def get(self, request, *args, **kwargs):
        current_cart = deserialize_cart(get_serialized_cart(request))
        if len(current_cart) != 0:
            return render(request,
                          'store/checkout-page.html',
                          {'cart': current_cart,
                           'subtotal': get_cart_subtotal(current_cart),
                           'form': CheckoutForm()})
        else:
            return redirect('shopping-cart')


class process_order(View):
    def post(self, *args, **kwargs):
        response = {}

        # Validate Session JSON object has Shippng, Billing, CartItems, Contact
        # Create Order, Shipping Object, Billing Address, Items, Contact,
        # Clear Sessions.

        for key, value in self.request.session.items():
            print('{} => {}'.format(key, value))

        # cart => {'2': '[{"model": "store.cartitem", "pk": null, "fields": {"product": 2, "quantity": 1}}]'}
        # contact => {'id': None, 'first_name': 'Noah', 'last_name': 'Pan', 'phone_number': '6463307800', 'email_address': 'noahpan323@gmail.com'}
        # billing_address => {"id": null, "address1": "202-07 56th Ave.", "address2": "", "country": "US", "state": "NY", "city": "Oakland Gardens", "zipcode": "11364"}
        # shipping_address => {"id": null, "address1": "202-07 56th Ave.",
        # "address2": "", "country": "US", "state": "NY", "city": "Oakland
        # Gardens", "zipcode": "11364", "billingaddress_ptr": null}

        contact_info = deserialize_object(self.request.session["contact"])
        shipping_info = deserialize_object(
            self.request.session["shipping_address"])
        billing_info = deserialize_object(
            self.request.session["billing_address"])

        contact_info.save()
        shipping_info.save()
        billing_info.save()
        paypal_info = json.loads(self.request.POST.get('paypal_info'))
        # paypalinfo_pretty = json.dumps(paypalinfo, indent=2)

        print(contact_info)
        print(shipping_info)
        print(billing_info)

        newOrder = Cart(
            contact=contact_info,
            shipping_address=shipping_info,
            billing_address=billing_info,
            paypal_information=paypal_info,
            ordered=True,
            ordered_date=timezone.now()
        )
        newOrder.save()

        # Add Items to the Order
        current_cart = deserialize_cart(get_serialized_cart(self.request))
        for item in current_cart:
            item.save()
            newOrder.items.add(item)
        newOrder.save()

        self.request.session.flush()

        response["success"] = True
        response["orderid"] = newOrder.id

        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )


class CheckoutSuccessPage(DetailView):
    model = Cart
    context_object_name = "order"
    template_name = "store/checkout-success.html"


def add_to_cart(request, pk, slug):
    product = get_object_or_404(Product, id=pk, slug=slug)
    current_cart = get_serialized_cart(request)

    # if request.user.is_authenticated:
    #     cart_item, cart_item_created = CartItem.objects.get_or_create(
    #         user=request.user, product=product, order=current_order)
    #     if cart_item_created:
    #         current_order.items.add(cart_item)
    #     else:
    #         cart_item.quantity += 1
    #         cart_item.save()
    # else:
    print(current_cart)
    # Check if item is in cart
    # Deserialize data if item is in cart
    # Create new object if not in cart.
    product_id = str(product.id)
    if product_id in current_cart:
        # Deserialize the line item from sessions object
        line_item = deserialize_object(current_cart[product_id])
        line_item.quantity += 1
    else:
        line_item = CartItem(product=product)
    # Reserialize the line item to be stored back into sessions
    current_cart[product_id] = serialize_object(line_item)
    request.session["cart"] = current_cart
    request.session.modified = True

    # return HttpResponseRedirect(request.path_info)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_from_cart(request, pk, slug):
    product = get_object_or_404(Product, id=pk, slug=slug)
    current_cart = get_serialized_cart(request)

    # if not request.user.is_authenticated:
    #     cart_item, cart_item_created = CartItem.objects.get_or_create(
    #         product=product, order=current_order)
    # else:
    #     cart_item, cart_item_created = CartItem.objects.get_or_create(
    #         user=request.user, product=product, order=current_order)

    print("Trying to delete id: " + str(product.id))
    product_id = str(product.id)
    if product_id in current_cart:
        # Deserialize the line item from sessions object
        line_item = deserialize_object(current_cart[product_id])
        if line_item.quantity <= 1:
            del current_cart[product_id]
        else:
            line_item.quantity -= 1
            # Reserialize the line item to be stored back into sessions
            current_cart[product_id] = serialize_object(line_item)
        request.session["cart"] = current_cart
        request.session.modified = True

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return HttpResponseRedirect(request.path_info)
