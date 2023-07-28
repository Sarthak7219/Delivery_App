from django.urls import path
from .views import item_detail_view

urlpatterns = [
    path('<slug>/', item_detail_view, name='item_detail'),
]
    