from rest_framework.test import APIClient
from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from products.models import Product, Category, Comment
import json
from decimal import Decimal
from django.contrib.auth.models import User

#testing views

class TestViews(TestCase):
    ### 10/10, completed ###

    def setUp(self):
        TestCase.allow_database_queries = True
        self.study_notes_category = Category.objects.create(name = 'Study notes')
        self.clothing_category = Category.objects.create(name = 'Clothing')

        self.author_user = User.objects.create(username='testuser')
        self.author_user.set_password('12345')
        self.author_user.save()

        self.client = Client()
        login = self.client.login(username='testuser', password='12345')
        #author_user creates his product with id/pk = 1
        '''
        self.product1 = Product.objects.create(
            image_link_1 = 'http://personal.psu.edu/xqz5228/jpg.jpg',
            image_link_2 = 'https://media.alienwarearena.com/media/1327-m.jpg',
            category = self.study_notes_category, #category taken from CATEGORY_CHOICES
            title = 'T-shirt',
            condition = 'N',
            price_in_SGD = 1.0,
            description = 'testing',
            this_product_has_multiple_quantities = True,
            delivery_location = 'CLB/Engineering', #delivery_location taken from DELIVERY_CHOICES
            extra_information = 'Nothing to add',
            author = author_user,
            #attributes auto-generated: pub_date and view_count
        )
        self.PRODUCT_ID = 1
        '''
        self.another_user = User.objects.create(username='another_dude')
        self.another_user.set_password('12345')
        self.another_user.save()

        self.client = Client()
        self.API_client = APIClient()
        self.product1 = Product.objects.create(
            image_link_1 = 'http://personal.psu.edu/xqz5228/jpg.jpg',
            image_link_2 = 'https://media.alienwarearena.com/media/1327-m.jpg',
            category = self.study_notes_category, #category taken from CATEGORY_CHOICES
            title = 'T-shirt',
            condition = 'N',
            price_in_SGD = 1.0,
            description = 'testing',
            this_product_has_multiple_quantities = True,
            delivery_location = 'CLB/Engineering', #delivery_location taken from DELIVERY_CHOICES
            extra_information = 'Nothing to add',
            author = self.author_user,
            #attributes auto-generated: pub_date and view_count
        )
        self.PRODUCT_ID = 1

    def test_product_list_view_number_of_listings_works(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200) #status code 200, the request was fulfilled.
        self.assertTemplateUsed(response, 'products/product_list.html')
        self.assertEquals(Product.objects.count(), 1)

    def test_product_category_view_categorisation_works(self):
        self.product2 = Product.objects.create(
            image_link_1 = 'http://personal.psu.edu/xqz5228/jpg.jpg',
            image_link_2 = 'https://media.alienwarearena.com/media/1327-m.jpg',
            category = self.study_notes_category, #<---------------
            title = 'T-shirt',
            condition = 'N',
            price_in_SGD = 1.0,
            description = 'testing',
            this_product_has_multiple_quantities = True,
            delivery_location = 'CLB/Engineering', #delivery_location taken from DELIVERY_CHOICES
            extra_information = 'Nothing to add',
            author = self.author_user,
            #attributes auto-generated: pub_date and view_count
        )

        self.product3 = Product.objects.create(
            image_link_1 = 'http://personal.psu.edu/xqz5228/jpg.jpg',
            image_link_2 = 'https://media.alienwarearena.com/media/1327-m.jpg',
            category = self.clothing_category, #<---------------
            title = 'T-shirt',
            condition = 'N',
            price_in_SGD = 1.0,
            description = 'testing',
            this_product_has_multiple_quantities = True,
            delivery_location = 'CLB/Engineering', #delivery_location taken from DELIVERY_CHOICES
            extra_information = 'Nothing to add',
            author = self.author_user,
            #attributes auto-generated: pub_date and view_count
        )

        #correct counts
        self.assertEquals(len(Product.objects.filter(category = self.study_notes_category)), 2)
        self.assertEquals(len(Product.objects.filter(category = self.clothing_category)), 1)

        #correct HTTPResponse
        response = self.client.get(reverse('product-by-category', args = (self.PRODUCT_ID,)))
        self.assertEquals(response.status_code, 200) #the request was fulfilled.

    def test_user_profile_view_works(self):
        response = self.client.get(reverse('user-details'))
        self.assertEquals(response.status_code, 200) #the request was fulfilled.

    def test_product_create_works(self):
        '''
            check if the product listing is actually created
        '''
        Product.objects.create(
            image_link_1 = 'http://personal.psu.edu/xqz5228/jpg.jpg',
            image_link_2 = 'https://media.alienwarearena.com/media/1327-m.jpg',
            category = self.study_notes_category, #category taken from CATEGORY_CHOICES
            title = 'T-shirt',
            condition = 'N',
            price_in_SGD = 1.0,
            description = 'testing',
            this_product_has_multiple_quantities = True,
            delivery_location = 'CLB/Engineering', #delivery_location taken from DELIVERY_CHOICES
            extra_information = 'Nothing to add',
            author = self.author_user,
            #attributes auto-generated: pub_date and view_count
        )
        self.PRODUCT_ID += 1
        response = self.client.get(reverse('product-detail', args = (self.PRODUCT_ID,))) 
        self.assertEquals(response.status_code, 302) #redirected to product-details page
        self.assertEquals(Product.objects.count(), 2) #check if the product listing is created
        
    def test_product_detail_view_from_author_works(self):
        self.client.login(username='testuser', password='12345')
        #self.author_user, the creator of the product listing, requests to view the listing.
        response = self.client.get(reverse('product-detail', args = (self.PRODUCT_ID,)))

        #authenticated
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertEquals(response.status_code, 200)
    
    def test_product_detail_view_from_other_users_works(self):
        self.client.login(username='another_dude', password='12345')
        #self.author_user, the creator of the product listing, requests to view the listing.
        response = self.client.get(reverse('product-detail', args = (self.PRODUCT_ID,)))

        #authenticated
        self.assertTemplateUsed(response, 'products/product_detail_guest.html')
        self.assertEquals(response.status_code, 200)

    def test_product_update_view_from_author_works(self):
        self.client.login(username='testuser', password='12345')
        #self.author_user, the creator of the product listing, requests to update the listing.
        response = self.client.get(reverse('product-update', args = (self.PRODUCT_ID,)))

        #authenticated, view from author of the listing
        self.assertTemplateUsed(response, 'products/product_create.html')
        self.assertEquals(response.status_code, 200)

        UPDATE_request = self.client.post(reverse('product-update', args = (self.PRODUCT_ID,)))
        self.assertEquals(response.status_code, 200) #check that update POST request is fulfilled (html rendered)
        self.assertEquals(Product.objects.count(), 1) #confirm that product1 is still here

    def test_product_update_view_from_other_users_unauthorised(self):
        self.client.login(username='another_dude', password='12345')
        response = self.client.get(reverse('product-update', args = (self.PRODUCT_ID,)))

        #permission denied, will redirect to home
        self.assertEquals(response.status_code, 302) #redirected to home

    def test_product_delete_view_from_author_works(self):
        self.client.login(username='testuser', password='12345')
        #self.author_user, the creator of the product listing, requests to delete the listing.
        GET_response = self.client.get(reverse('product-delete', args = (self.PRODUCT_ID,)))

        #authenticated, view from author of the listing
        self.assertTemplateUsed(GET_response, 'products/product_delete.html')
        self.assertEquals(GET_response.status_code, 200)

        POST_response = self.client.post(reverse('product-delete', args = (self.PRODUCT_ID,)))

        self.assertEquals(POST_response.status_code, 302) #product1 deleted, redirects to home
        self.assertEquals(Product.objects.count(), 0) #confirm that product1 is already deleted

    def test_product_delete_view_from_other_users_unauthorised(self):
        self.client.login(username='another_dude', password='12345')
        response = self.client.get(reverse('product-delete', args = (self.PRODUCT_ID,))) #product2

        #permission denied, will redirect to home
        self.assertEquals(response.status_code, 302) #redirected to home
