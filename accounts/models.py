from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from Items.models import Category, Items, Coupon



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_img = models.ImageField(upload_to='profile')
    email = models.CharField(max_length=20 )
 

# @receiver(post_save, sender = User)
# def send_email_token(sender, instance, created, **kwargs):
#     try:
#         if created:
#             email_token = str(uuid.uuid4())
#             Profile.objects.create(user = instance, email_token = email_token)
#             email = instance.email
#             send_account_activation_email(email, email_token)

#     except Exception as e:
#         print(e)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    is_paid = models.BooleanField(default=False)  #if is paid true that means cart items have been ordered and then the cart has to be empty.
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_signature = models.CharField(max_length=100, null=True, blank=True)

    def get_cart_total(self):
        
        price = []
        cart_items = self.cart_items.all()
        for cart_item in cart_items:
            price.append(cart_item.item.price)

        if self.coupon:
            if self.coupon.min_req_amount <= sum(price):
                new_price = sum(price)-self.coupon.discount_price
                return new_price
            self.coupon = None

        return sum(price)

class CartItems(models.Model): 
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(Items, on_delete=models.SET_NULL, null=True, blank=True)

    def get_cart_item_id(self):
        id = self.id
        return id

    def __str__(self) -> str:
        return self.item.item_name
    
    def get_item_price(self):
        price = [self.item.price]
        return sum(price)
    



    