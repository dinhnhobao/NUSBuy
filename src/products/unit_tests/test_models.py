from django.test import TestCase
from products.models import Category, Product, Comment
from django.contrib.auth.models import User
from django.test import Client

### 5/5 methods, completed ###

class TestModels(TestCase):
    def setUp(self): #run before all other test methods, setup a certain scenario
        TestCase.allow_database_queries = True #query from database for Category
        self.study_notes_category = Category.objects.create(name = 'Study notes') #id 1
        self.clothing_category = Category.objects.create(name = 'Clothing') #id 2, .id to access
        self.house_category = Category.objects.create(name = 'Household items & Electronics')
        self.others_category = Category.objects.create(name = 'Others')

        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        client = Client()
        login = client.login(username='testuser', password='12345')
        # for testing purposes, we will create two Products with (two) different categories, as well as putting one
        # or two comments for each product
        self.product1 = Product.objects.create(
            image_link_1 = 'http://personal.psu.edu/xqz5228/jpg.jpg',
            image_link_2 = 'https://media.alienwarearena.com/media/1327-m.jpg',
            category = self.clothing_category, #category taken from CATEGORY_CHOICES
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

        self.product2 = Product.objects.create(
            image_link_1 = 'http://personal.psu.edu/xqz5228/jpg.jpg',
            image_link_2 = 'https://media.alienwarearena.com/media/1327-m.jpg',
            image_link_3 = 'https://media.alienwarearena.com/media/1327-m.jpg',
            image_link_4 = 'http://personal.psu.edu/xqz5228/jpg.jpg',
            category = self.study_notes_category, #category taken from CATEGORY_CHOICES
            title = 'CS2030',
            condition = 'N',
            price_in_SGD = 10.0,
            description = 'testing',
            this_product_has_multiple_quantities = True,
            delivery_location = 'CLB/Engineering', #delivery_location taken from DELIVERY_CHOICES
            extra_information = 'Nothing to add',
            author = user
            #attributes auto-generated: pub_date and view_count
        )

        self.comment1 = Comment.objects.create(
            comment = 'good',
            author = user,
            listing = self.product1
        )

        self.comment1b = Comment.objects.create(
            comment = 'good job 2',
            author = user,
            listing = self.product1
        )

        self.comment2 = Comment.objects.create(
            comment = 'beautiful item',
            author = user,
            listing = self.product2
        )

        self.comment2b = Comment.objects.create(
            comment = '---zhe de',
            author = user,
            listing = self.product2
        )

    def test_total_of_product_listings(self):
        self.assertTrue(Product.objects.count(), 2)
    
    def test_is_product_category_accurate(self):
        self.assertTrue(Product.objects.order_by('-pub_date')[0].category, self.product2.category)
        self.assertTrue(Product.objects.order_by('-pub_date')[1].category, self.product1.category)

    def test_product_category_filtering(self):
        self.assertEquals(Product.objects.filter(category = self.study_notes_category).count(), 1)
        self.assertEquals(Product.objects.filter(category = self.clothing_category).count(), 1)
        self.assertEquals(Product.objects.filter(category = self.house_category).count(), 0)
        self.assertEquals(Product.objects.filter(category = self.others_category).count(), 0)  

    def test_total_of_comments(self):
        self.assertEquals(Comment.objects.count(), 4)

    def test_product_comment_matches_listing(self):
        self.assertEquals(Comment.objects.filter(listing = self.product1).count(), 2)
        self.assertEquals(Comment.objects.filter(listing = self.product2).count(), 2)

