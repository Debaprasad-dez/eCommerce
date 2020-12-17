from django.db import models
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.urls import reverse

# Create your models here.


class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    status = models.CharField(max_length=20, choices=STATUS)
    slug = models.SlugField(null=True, unique=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self) :
        return self.title
    
    class MPTTMeta:
        order_insertion_by = ['title']
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})
        
    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])



class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    prevprice = models.FloatField()
    price = models.FloatField()
    amount = models.IntegerField()
    minamount = models.IntegerField()
    detail = RichTextUploadingField()
    status = models.CharField(max_length=20, choices=STATUS)
    slug = models.SlugField()
    featured = models.BooleanField(default=False)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})
    
    def image_tag(self):
        return mark_safe('<img_src="{}" height="50"/>'.format(self.image.url))
    
    image_tag.short_description = 'Image'
    
class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')
    
    def __str__(self):
        return self.title
    