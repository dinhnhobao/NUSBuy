from django.test import SimpleTestCase, TestCase
from products.forms import ProductForm, CommentForm
import json
from decimal import Decimal
from django.contrib.auth.models import User
from products.models import Category
class TestForms(TestCase):
    def test_product_form_valid_data(self):
        TestCase.allow_database_queries = True
        ##query from database
        clothing_category = Category.objects.get(name = 'Clothing')
        form = ProductForm(data = {
            'image_link_1' : 'https://www.facebook.com/',
            'category' : clothing_category, #category taken from CATEGORY_CHOICES
            'title' :'T-shirt',
            'condition' : 'N',
            'price_in_SGD' : 1.0,
            'description' : 'testing',
            'this_product_has_multiple_quantities' : True,
            'delivery_location' : 'CLB/Engineering', #delivery_location taken from DELIVERY_CHOICES
            'extra_information' : 'Nothing to add',
            #attributes auto-generated (3)
        })
        print(form.errors)
        self.assertTrue(form.is_valid())
    def test_product_form_invalid_or_no_data(self):
        form = ProductForm(data = {}) #no data form

        self.assertFalse(form.is_valid()) #check if it is not valid
    
        form = ProductForm(data = {
            'image_link_1': 'this is not a correct link',
            'title': 'There are missing entries too',
        })

        self.assertFalse(form.is_valid()) #check if it is not valid

    def test_comment_form_valid_data(self):
        form = CommentForm(data = {
            'comment': 'This is great.' #the only entry in forms.py
            #the other three fields are tested in test_models.py
        })

        self.assertTrue(form.is_valid())

    def test_comment_form_invalid_or_no_data(self):
        form = CommentForm(data = {
            })

        self.assertFalse(form.is_valid())
