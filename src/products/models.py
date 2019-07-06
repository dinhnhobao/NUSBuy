from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
# Create your models here.
class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Household items & Electronics', 'Household items & Electronics'),
        ('Clothing', 'Clothing'),
        ('Study notes', 'Study notes'),
        ('Others', 'Others')
    ]
    name = models.CharField(max_length=100, unique=True, choices = CATEGORY_CHOICES)
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-by-category', args=[self.name])

class Product(models.Model):

    image_link_1 = models.URLField(max_length = 1000, blank = True, default = '')
    image_link_2 = models.URLField(max_length = 1000, blank = True, default = '')
    image_link_3 = models.URLField(max_length = 1000, blank = True, default = '')
    image_link_4 = models.URLField(max_length = 1000, blank = True, default = '')

    category = models.ForeignKey('Category', on_delete = models.CASCADE, null = True, blank = True)

    title = models.CharField(max_length = 255)

    CONDITION_CHOICES = [
        ('N', 'New'),
        ('USED', 'Used'),
    ]
    condition = models.CharField(max_length = 255, choices = CONDITION_CHOICES, default = 'Not chosen')
    price_in_SGD = models.DecimalField(decimal_places=2, max_digits=10000)
    description = models.TextField(blank=True, null=True)
    this_product_has_multiple_quantities = models.BooleanField()

    LOCATION_CHOICES = [
        ('ONL', 'ONLINE'),
        ('PGP', "Prince George Park's Residences/ KEVII Hall"),
        ('KRMRT', 'Kent Ridge MRT'),
        ('S', 'Science/ UHall'),
        ('UHC', 'UHC/ RVRC/ YIH'),
        ('M', 'Museum/Raffles Hall'),
        ('U', 'UTown'),
        ('CLB', 'CLB/Engineering'),
        ('AS', 'FASS/ Eusoff Hall/ Temasek Hall'),
        ('COM', 'SoC'),
        ('BIZ', 'Business School/ Kent Ridge Hall/ Sheares Hall'),
    ]
    delivery_location = models.CharField(max_length = 255, choices = LOCATION_CHOICES, default = 'Not yet chosen')
    extra_information = models.TextField(blank = True, null = True)

    #automatically generated
    pub_date = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, on_delete = models.CASCADE, default = '')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.pk])

class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, default = '') #many-to-one
    listing = models.ForeignKey(Product, on_delete = models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

