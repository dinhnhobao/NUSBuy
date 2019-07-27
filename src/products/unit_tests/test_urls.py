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
    ### 9/9, completed ###
    
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
        self.PRODUCT_ID = 1
        another_user = User.objects.create(username='another_dude')
        another_user.set_password('12345')
        another_user.save()

        self.client = Client()

    def test_home_url_resolves(self): #resolved: settled
        self.assertEquals(resolve(reverse('home')).func, views.products_list) #function_based view

    def test_product_create_url_resolves(self): 
        self.assertEquals(resolve(reverse('product-create')).func, views.product_create) #view_class for class based views
    
    def test_product_detail_url_resolves(self):
        #we will test the response view from the first item
        url = reverse('product-detail', args = (self.PRODUCT_ID,))
        self.assertEquals(resolve(url).func.view_class, views.PostDetail)

    def test_product_update_url_resolves(self):
        url = reverse('product-update', args = (self.PRODUCT_ID,))
        self.assertEquals(resolve(url).func, views.product_update)

    def test_product_delete_url_resolves(self):
        url = reverse('product-delete', args = (self.PRODUCT_ID,))
        self.assertEquals(resolve(url).func, views.product_delete_view)

    def test_login_url_resolves(self):
        self.assertEquals(resolve(reverse('login')).func, views.login_view)

    def test_logout_url_resolves(self):
        self.assertEquals(resolve(reverse('logout')).func.view_class, auth_views.LogoutView)
    
    def test_profile_url_resolves(self):
        self.assertEquals(resolve(reverse('user-details')).func.view_class, TemplateView.as_view(template_name= 'users/user_details.html').view_class)

    def test_category_url_resolves(self):
        url = reverse('product-by-category', args = (self.PRODUCT_ID,))
        self.assertEquals(resolve(url).func.view_class, views.PostCategory)
