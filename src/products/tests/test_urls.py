'''
from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from products import views
from django.contrib.auth import views as auth_views #name for easy differentiation
from django.views.generic import TemplateView
from products.models import Category, Product, Comment
from django.contrib.auth.models import User
from django.test import Client

class TestUrls(TestCase):

    ### unit testing: testing urls ###
    # 12/12, completed #
    
    #Formula:
    #self.assertEquals(resolve(reverse('<name of view>')).func, correct view function)
    def setUp(self):
        TestCase.allow_database_queries = True #query from database for Category
        self.study_notes_category = Category.objects.create(name = 'Study notes')
        
        author_user = User.objects.create(username='testuser')
        author_user.set_password('12345')
        author_user.save()

        client = Client()
        login = client.login(username='testuser', password='12345')
        #author_user creates his product with id/pk = 1
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

        another_user = User.objects.create(username='another_dude')
        another_user.set_password('12345')
        another_user.save()

    def test_home_url_resolves(self): #resolved: settled
        self.assertEquals(resolve(reverse('home')).func, views.products_list) #function_based view

    def test_product_create_url_resolves(self): 
        self.assertEquals(resolve(reverse('product-create')).func, views.product_create) #view_class for class based views
    
    def test_product_detail_view_from_author(self):
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get('/post/1/')

        #view from author of the listing
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_product_detail_view_from_other_users(self):
        c = Client()
        c.login(username='another_dude', password='12345')
        response = c.get('/post/1/')

        #view from other users
        self.assertTemplateUsed(response, 'products/product_detail_guest.html')

    def test_product_update_view_from_author(self):
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get('/post/1/update/')

        #authenticated, view from author of the listing
        self.assertTemplateUsed(response, 'products/product_create.html')
        self.assertEquals(response.status_code, 200)

    def test_product_update_view_from_other_users(self):
        c = Client()
        c.login(username='another_dude', password='12345')
        response = c.get('/post/1/update/')

        #permission denied, will redirect to home
        self.assertEquals(response.status_code, 302) #redirected

    def test_product_delete_view_from_author(self):
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get('/post/1/delete/')

        #authenticated, view from author of the listing
        self.assertTemplateUsed(response, 'products/product_delete.html')
        self.assertEquals(response.status_code, 200)

    def test_product_delete_view_from_other_users(self):
        c = Client()
        c.login(username='another_dude', password='12345')
        response = c.get('/post/1/delete/')

        #permission denied, will redirect to home
        self.assertEquals(response.status_code, 302) #redirected

    def test_login_url_resolves(self):
        self.assertEquals(resolve(reverse('login')).func, views.login_view)

    def test_logout_url_resolves(self):
        self.assertEquals(resolve(reverse('logout')).func.view_class, auth_views.LogoutView)
    
    def test_profile_url_resolves(self):
        self.assertEquals(resolve(reverse('user-details')).func.view_class, TemplateView.as_view(template_name= 'users/user_details.html').view_class)

    def test_category_url_resolves(self):
        c = Client()
        c.login(username='another_dude', password='12345')
        response = c.get('/post/category/1/')

        #permission denied, will redirect to home
        self.assertTemplateUsed(response, 'products/product_category.html')
        self.assertEquals(response.status_code, 200) #redirected
'''