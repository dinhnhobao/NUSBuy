from django.test import SimpleTestCase
from django.urls import reverse, resolve
from products import views
from django.contrib.auth import views as auth_views #name for easy differentiation
#unit-test module

class TestUrls(SimpleTestCase):

    ### unit testing: testing urls ###
    # 4/8 #
    '''
    Formula:
    self.assertEquals(resolve(reverse('<name of view>')).func, correct view function)
    '''
    def test_home_url_resolves(self): #resolved: settled
        self.assertEquals(resolve(reverse('home')).func, views.products_list)

    def test_product_create_url_resolves(self): 
        self.assertEquals(resolve(reverse('product-create')).func.view_class, views.PostCreate) #view_class for class based views
    '''
    def test_product_detail_url_resolves(self): 
        url = reverse('product-detail', kwargs = {'pk': })
        self.assertEquals(resolve(url).func.view_class, views.PostDetail)
    
    def test_product_update_url_resolves(self):
        url = reverse('product-update', args = ['pk'])
        self.assertEquals(resolve(reverse(url)).func, views.product_update)

    def test_product_delete_url_resolves(self):
        url = reverse('product-delete', args = id)
        self.assertEquals(resolve(reverse(url).func, views.product_delete_view))
    '''
    def test_login_url_resolves(self):
        self.assertEquals(resolve(reverse('login')).func.view_class, auth_views.LoginView)

    def test_logout_view_resolves(self):
        self.assertEquals(resolve(reverse('logout')).func.view_class, auth_views.LogoutView)
    '''
    def test_category_view_resolves(self):
        url = reverse('product-category', pk)
        self.assertEquals(resolve(reverse(url).func.view_class, views.PostCategory))
    '''
    ### testing urls ends here ###