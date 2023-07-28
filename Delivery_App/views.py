from django.shortcuts import render
from django.views import View
from Items.models import Category, Items


class Index(View) :
    def get(self, request):
        category = Category.objects.all()
        items = Items.objects.all()
        context = {
            'category' : category,
            'items' : items,
        }
        


        return render(request, 'home/home.html', context)
    
def items_search_view(request) :
    if request.method == 'GET':
        query = request.GET.get('q')
        qs = Items.objects.all()
        qs = Items.objects.filter(item_name__icontains=query)
        context = {
            'query' : query,
            'items':qs
        }
        return render(request,'items/search.html',context=context)


class About(View):
    def get(self, request):
         return render(request, 'home/about.html')
    
class Menu(View):
    def get(self, request):
        category = Category.objects.all()
        items = Items.objects.all()
        context = {
            'category' : category,
            'items' : items,
        }
        print(items)
        return render(request, 'home/menu.html', context)
    
class Book(View):
    def get(self, request):
         return render(request, 'home/book.html')
    
