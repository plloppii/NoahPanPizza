from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django_countries.fields import CountryField

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    thumbnail = models.ImageField(default='', upload_to='product_thumbnails', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_instock = models.IntegerField()
    date_posted = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.name + " "+ str(self.price)
    
    def save(self, *args, **kwargs):
        mslug = slugify(self.name)
        if self.slug == None or self.slug != mslug:
            exists = Product.objects.filter(slug=mslug).exists()
            count = 1
            while exists:
                count+=1
                mslug = slugify(self.name)+ "-"+str(count)
                exists = Product.objects.filter(slug=mslug).exists()
            self.slug = mslug
        super().save(*args, **kwargs)


class ContactInfo(models.Model):
    first_name = models.CharField(max_length=100) 
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email_address = models.CharField(max_length=100)
    def __str__(self):
        return self.first_name+" "+self.last_name+"\n"+self.email_address+" "+self.phone_number

# class PaymentInfo(models.Model):
#     payment_id =models.CharField(max_length=100)


class BillingAddress(models.Model):
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=5)
    def __str__(self):
        return self.address1+self.address2+"\n"+self.city+" "+self.state+" "+self.zipcode+"\n"+self.country.code
class ShippingAddress(BillingAddress):
    pass

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey("Cart", on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)

    def get_subtotal(self):
        return self.product.price*self.quantity

    def __str__(self):
        return self.product.name
        # return self.product.name + " OrderID:"+str(self.order.id)+" "+" Qty:"+str(self.quantity)
    def save(self, *args, **kwargs):
        print("CartItem Save called!")
        super().save(*args, **kwargs)   
 
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    contact = models.ForeignKey(ContactInfo, on_delete=models.SET_NULL, blank=True, null=True)
    items = models.ManyToManyField(CartItem)
    ordered_date = models.DateTimeField(auto_now_add=True)
    paypal_information = JSONField(null=True, blank=True)
    billing_address = models.ForeignKey(BillingAddress, related_name="billing_address", on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey(ShippingAddress,related_name="shipping_address", on_delete=models.SET_NULL, blank=True, null=True)
    ordered = models.BooleanField(default=False)

    def is_empty(self):
        return self.get_total_items() == 0
    def get_total_items(self):
        return sum([quat.quantity for quat in self.items.all()])
    def get_subtotal(self):
        return sum([(item.quantity*item.product.price) for item in self.items.all()]) 

    def __str__(self):
        rtn = str(self.user)+" Order ("+ str(self.get_total_items())+" Items): "
        if(self.ordered): rtn+="Filled"
        else: rtn+="Open" 
        return rtn

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)    

    def ready_for_payment(self):
        return (self.ordered == False and not self.is_empty() )


