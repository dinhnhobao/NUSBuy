from django.db import models

# everytime we make changes to model.py
# use python manage.py makemigrations && python manage.py migrate


# Create your models here.
# store memory of products

class Product(models.Model): #inherit from Django's model class
    #attributes
    title = models.CharField(max_length = 100) # max_length = required, in characters

    description = models.TextField()  #?

    price = models.TextField()

    summary = models.TextField(blank=True, null=False)

    featured = models.BooleanField() # null = True, default = True
    
    # null = True: if the attribute is not available in the old objects,
    # its value will be default to True

    # or we can input this default value when the prompt asks

    # blank = False: it is required to fill up this field
    # null = True/False: whether it can be null values in the databases