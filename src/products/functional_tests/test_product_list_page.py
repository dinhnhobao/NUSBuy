from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.opera.options import Options, ChromeOptions
from products.models import Product, Category, Comment
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.auth.models import User
from django.test import Client

class TestProductListPage(StaticLiveServerTestCase): #or LiveServerTestCase

    def setUp(self): #run BEFORE every SINGLE test function
        self.browser = webdriver.Chrome(ChromeDriverManager().install()) #open a browser
        
        #login

    def tearDown(self): #run after every SINGLE test function
        self.browser.close()

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
        '''
        <a href="/add/" class="btn-large grey"> <--- button html, redirects to the add form
        <i class="material-icons white-text left">add_circle</i>
        <span class="bold">Add Project</span>
         </a>
        '''
        # The user requests the page for the first time
        add_url = self.live_server_url + reverse('product-create')

        self.browser.find_element_by_link_text('CREATE A LISTING').click() #button
        self.assertEquals(
            self.browser.current_url, #url in test case
            add_url, #expected url
        )

    def test_user_sees_products_list(self):
        '''
        #create the category
        self.study_notes_category = Category.objects.create(name = 'Study notes') #id 1

        #registration
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        #login
        client = Client()
        login = client.login(username='testuser', password='12345')

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
            author = user
            #attributes auto-generated: pub_date and view_count
        )

        self.browser.get(self.live_server_url)

        # check if The user sees the product1 on the screen
        # get the product name via the h5 tag
        self.assertEquals(
            self.browser.find_element_by_tag_name('columns').find_element_by_tag_name('card').find_element_by_tag_name('h2').text,
            'T-shirt'
        )
        '''
        pass

    def test_see_details_button_redirects_to_product_detail_page(self):

        '''
        #create a new project
        project1 = Project.objects.create(
            name = 'project1',
            budget = 10000
        )

        self.browser.get(self.live_server_url) #locate to our server, which uses StaticLiveServerTestCase

        # The user sees the project on the screen. He clicks the 'VISIT' link
        # and is directed to the detail page
        detail_url = self.live_server_url + reverse('detail', args = [project1.slug])

        # navigate to VISIT in html, may only work with only one element/project
        self.browser.find_element_by_link_text('VISIT').click()
        self.assertEquals(
            self.browser.current_url,
            detail_url
        )
        '''
        pass

    