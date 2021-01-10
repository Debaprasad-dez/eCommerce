from django.db import models
from django.db.models import Avg, Count
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.


class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    status = models.CharField(max_length=20, choices=STATUS)
    slug = models.SlugField(null=True, unique=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

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
    keywords = models.TextField()
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

    def avaregereview(self):
        reviews = Review.objects.filter(product=self, status='True').aggregate(average=Avg('rate'))
        avg=0
        if reviews["average"] is not None:
            avg=float(reviews["average"])
        return avg

    def countreview(self):
        reviews = Review.objects.filter(product=self, status='True').aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt
    
    @property
    def offer(self):
        import math
        return math.ceil(( ((self.prevprice - self.price)*100/self.prevprice) / 1000 ) * 1000)
    
    image_tag.short_description = 'Image'
    
class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')
    class Meta:
        verbose_name_plural = "Images"
    
    def __str__(self):
        return self.title
    
class Review(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # subject = models.CharField(max_length=50, blank=True)
    # comment = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status=models.CharField(max_length=10,choices=STATUS, default='New')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rate']
