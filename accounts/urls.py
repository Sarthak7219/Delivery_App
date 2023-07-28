from django.urls import path
from .views import *


urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<id>/', remove_from_cart, name='remove-from-cart'),
    path('order/<slug>/', order_now_view, name='order-now'),
]
