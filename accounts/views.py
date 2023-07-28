from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from accounts.models import Profile, Cart, CartItems
from django.conf import settings
from Items.models import Items, Coupon, Category
import razorpay


# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = authenticate(request, username = username, password = password)

        if user_obj is None:
            messages.warning(request, "Invalid username or password")
            return HttpResponseRedirect(request.path_info)
        
        # if not user_obj.profile.is_email_verified:
        #     messages.warning(request, "Account is not verified")
        #     return HttpResponseRedirect(request.path_info)

        login(request,user_obj)
        return redirect('/')
        
    return render(request, "accounts/login.html")

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)

        if user_obj.exists() :
            messages.warning(request, "Email is already registered ")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = email
        )
        user_obj.set_password(password)
        user_obj.save()
        

        
        
        messages.success(request, "A verification email has been sent to your mail")
        return HttpResponseRedirect(request.path_info)


    return render(request, 'accounts/register.html')


def add_to_cart(request, slug):
    item = Items.objects.get(slug = slug)
    user = request.user
    cart , _ = Cart.objects.get_or_create(user = user, is_paid = False)
    cart_item = CartItems.objects.create(cart = cart, item = item)
    messages.success(request, "Item added to your cart successfully!")
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def order_now_view(request, slug):
    item = Items.objects.get(slug = slug)
    context={
        'order_item' : item,
    }
    return render(request, 'accounts/cart.html', context)

def remove_from_cart(request, id):
    try:
        cart_item = CartItems.objects.get(id = id)
        cart_item.delete()

    except Exception as e:
        print(e)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def cart_view(request):
    try:
        cart = Cart.objects.get(is_paid = False, user = request.user)

    except Exception as e:
        print(e)
    
    try:

        cart_items = CartItems.objects.filter(cart = cart)

    except Exception as e:
        print(e)

    

    # if request.POST:
    #     coupon = request.POST.get('coupon')
    #     coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
    #     if not coupon_obj :    
    #         messages.warning(request, "Invalid Coupon!")
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    #     if cart.get_cart_total() < coupon_obj[0].min_req_amount:
    #         messages.warning(request, f'Minimum amount should be {coupon_obj[0].min_req_amount}')
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    #     if coupon_obj[0].is_expired:
    #         messages.warning(request, 'Coupon expired!')
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    #     if cart.coupon:
    #         messages.warning(request, 'Coupon already exists!')
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    #     cart.coupon = coupon_obj[0]

    #     cart.save()
        messages.success(request, "Coupon applied successfully!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    # Razorpay
    client = razorpay.Client(auth= (settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({'amount' : cart.get_cart_total()*100, 'currency' : 'INR', 'payment_capture' : 1})
    print(payment)
    cart.razorpay_order_id = payment['id']
    cart.save()

    context = {
        'cart' : cart,
        'cart_items' : cart_items,
        'payment' : payment
        
    }

    return render(request, 'accounts/cart.html', context)


    
    







