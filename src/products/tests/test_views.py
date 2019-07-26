'''
from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from products.models import Product, Category, Comment
import json
from decimal import Decimal
from django.contrib.auth.models import User

#testing views

class TestViews(TestCase):

    def setUp(self): #run before all other test methods
        #set-up a certain scenario
        self.client = Client()
        self.list_url = reverse('home')
        self.user = User.objects.create_user(username='test_user',
                                        password='dq123456')
        self.client.login(username = 'test_user', password = 'dq123456')
        clothing_category = Category(name = 'Clothing')
        clothing_category.save() #save the category first

        self.product1 = Product.objects.create(
            #this product has id/pk = 1 (STARTING_SLUG)
            image_link_1 = "https://www.facebook.com/",
            category = clothing_category,
            title = 'T-shirt',
            condition = 'N',
            price_in_SGD = Decimal(str(1.0)),
            description = 'testing',
            this_product_has_multiple_quantities = True,
            delivery_location = 'COM',
            extra_information = 'Nothing to add',
            author = self.user,
        )
        STARTING_SLUG = 1
        self.detail_url = reverse('product-detail', args = [str(STARTING_SLUG)]) #this is the url for the product1 product.
        '''
    GET request: the user retrieves information from the server.
    POST request: check whether the server saves the information received for storage
        '''
    def test_product_list_GET(self): #test READ list method
        response = self.client.get(self.list_url) #reverse('list') returns the url
                                                  #client.get(url) -> response
        self.assertEquals(response.status_code, 200) #render html: status code 200, the request was fulfilled.
        self.assertTemplateUsed(response, 'products/product_list.html')

    def test_product_detail_GET(self): #test READ details method
        response = self.client.get(self.detail_url) #reverse('list') returns the url
                                                    #client.get(url) -> response

        self.assertEquals(response.status_code, 200) #request fulfilled
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_product_list_GET_add_new_product(self): #test CREATE method
        study_notes_category = Category(name = 'Study notes')
        study_notes_category.save() #save the category first

        self.product2 = Product.objects.create(
            image_link_1 = "https://www.google.com/",
            category = study_notes_category,
            title = 'CS2040',
            condition = 'N',
            price_in_SGD = Decimal(str(1.0)),
            description = 'testing',
            this_product_has_multiple_quantities = True,
            delivery_location = 'COM',
            extra_information = 'Nothing to add',
            author = self.user,
        )
        self.assertEquals(Product.objects.all().count(), 2)

    def test_product_list_DELETE_deletes_product(self): #test DELETE method
        #Note: not yet tested when delete request is denied/another case

        response = self.client.delete(self.list_url, json.dumps({
            'id': 1, #id of product we have just created
        }))
        self.assertEquals(response.status_code, 200) #request fulfilled
        self.assertEquals(Product.objects.all().count(), 1) #there is only one left
    
    def test_product_list_UPDATE_updates_product(self):
        pass
    #add other methods
    '''