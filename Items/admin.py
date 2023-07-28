from django.contrib import admin
from .models import Category, Items


admin.site.register(Category)

class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'price', 'image']

admin.site.register(Items, ItemAdmin)




