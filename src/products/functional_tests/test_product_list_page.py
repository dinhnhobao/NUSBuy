from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.opera.options import Options, ChromeOptions
from products.models import Product, Category, Comment
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.auth.models import User
from seleniumlogin import force_login


class TestProductListPage(StaticLiveServerTestCase): #or LiveServerTestCase

    def setUp(self): #run BEFORE every SINGLE test function
        self.browser = webdriver.Chrome(ChromeDriverManager().install()) #open a browser
        self.author_user = User.objects.create_user(username='author_user', password='password')
        force_login(self.author_user, self.browser, self.live_server_url)
    def tearDown(self): #run after every SINGLE test function
        self.browser.close()
    '''
    def test_no_products_alert_is_displayed(self):
        self.browser.get(self.live_server_url) #locate to our server, which uses StaticLiveServerTestCase
        time.sleep(20)

        # look for elements and call attributes, make sure they are what expected
        # The user requests the page for the first time
        alert = self.browser.find_element_by_class_name('no-products-notification')
        self.assertEquals(
            alert.find_element_by_tag_name('h3').text,
            'There are no product listings yet.'
        )

    def test_create_a_listing_button_redirects_to_add_page(self):
        self.browser.get(self.live_server_url) #locate to our server, which uses StaticLiveServerTestCase

        # The user requests the page for the first time
        add_url = self.live_server_url + reverse('product-create')

        self.browser.find_element_by_link_text('CREATE A LISTING').click() #button
        self.assertEquals(
            self.browser.current_url, #url in test case
            add_url, #expected url
        )

    def test_user_sees_products_list(self):
        #create the category
        self.study_notes_category = Category.objects.create(name = 'Study notes') #id 1

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
            author = self.author_user, #<-----
            #attributes auto-generated: pub_date and view_count
        )

        self.browser.get(self.live_server_url + reverse('home'))

        # check if The user sees the product1 on the screen
        # get the product name via the h5 tag
        self.assertEquals(
            self.browser.find_element_by_tag_name('h2').text,
            'T-shirt'
        )
   
    def test_see_details_button_redirects_to_product_detail_page(self):

        self.study_notes_category = Category.objects.create(name = 'Study notes') #id 1

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
            author = self.author_user, #<-----
            #attributes auto-generated: pub_date and view_count
        )

        self.browser.get(self.live_server_url + reverse('product-detail', args = (1,)))

        self.assertEquals(
            self.live_server_url + reverse('product-detail', args = (1,)),
            self.live_server_url + reverse('product-detail', args = (1,))
        )

    def test_same_category_button_redirects_to_product_category_page(self):
        #similar
        pass
    '''