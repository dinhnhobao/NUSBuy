from django.test import SimpleTestCase
from products.forms import ProductForm, CommentForm

class TestForms(SimpleTestCase):
    def test_product_form_valid_data(self):
        self.user = User.objects.create_user(username='test_user',
                                        password='dq123456')
        clothing_category = Category(name = 'Clothing')
        clothing_category.save() #save the category first
        form = ProductForm(data = {
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
        })
        self.assertTrue(form.is_valid())

    def test_product_form_invalid_or_no_data(self):
        form = ProductForm(data = {})

        self.assertFalse(form.is_valid()) #check if it is not valid
    
    def test_comment_form_valid_data(self):
        pass

    def test_comment_form_invalid_or_no_data(self):