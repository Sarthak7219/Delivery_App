from django.db import models
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):

    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="categories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:    #to display name of category in the admin panel
        return self.category_name
    

class Items(models.Model):

    item_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='items')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    # In the example above, the Book model has a foreign key relationship to the Author model, and the related_name parameter is set to 'books'. This means that you can access the set of books written by an author using the books attribute on an Author object:
    price = models.DecimalField(max_digits=5, decimal_places=2)
    item_description = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.item_name)
        super(Items, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.item_name
    


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    min_req_amount = models.IntegerField(default=500)

    def __str__(self) -> str:
        return self.coupon_code
    

    
