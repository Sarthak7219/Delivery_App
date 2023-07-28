from django.shortcuts import render
from Items.models import Items

# Create your views here.
def item_detail_view(request, slug):
    try : 
        item = Items.objects.get(slug = slug)
        context = {
            'item' : item,
        }

        return render(request, 'items/item_detail.html', context)
    
    except Exception as e:
        print('*****')
        print(e)
        print('*****')