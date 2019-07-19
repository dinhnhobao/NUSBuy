from django import forms
from .models import Product, Comment

class TitleField(forms.CharField):
    # title name will always be (UPPERCASE first letter) + (lowercase the rest)
    def to_python(self, value):
        name = value[0].upper() + value.lower()[1:]
        return name

class ProductForm(forms.ModelForm):
    '''
    Form fields
    https://docs.djangoproject.com/en/2.2/ref/forms/fields/
    required = True/False
    label: human-friendly name for the attribute
    initial: initial value
    widget: Text box size
    help_text: descriptive text
    '''
    image_link_1 = forms.CharField(
                        label = 'Primary image link',
                        initial = 'http://personal.psu.edu/xqz5228/jpg.jpg',
                        widget=forms.Textarea(
                                attrs={
                                    "rows": 1,
                                    'cols': 60
                                }
                            ),
                        help_text = 'This is required. The system can only accept .jpg images as of now. Very sorry for the inconvenience!'
                        )

    image_link_2 = forms.CharField(
                        required=False,
                        initial = 'https://media.alienwarearena.com/media/1327-m.jpg', 
                        widget=forms.Textarea(
                                attrs={
                                    "rows": 1,
                                    'cols': 60
                                }
                            ),
                        help_text = 'This is not required. However, our product detail page has additional effects if there are more than 2 images in the product listing. You can keep the sample image link as above.'
                        )
    
    image_link_3 = forms.CharField(
                        required=False,
                        help_text = 'Not required',
                        widget=forms.Textarea(
                                attrs={
                                    "rows": 1,
                                    'cols': 60
                                }
                            )
                        )

    image_link_4 = forms.CharField(
                        required=False, 
                        help_text = 'Not required',
                        widget=forms.Textarea(
                                attrs={
                                    "rows": 1,
                                    'cols': 60
                                }
                            )
                        )
    
    title = TitleField(
                        label = 'Product title',
                        initial = 'This product',
                        widget=forms.Textarea(
                                attrs={
                                    "rows": 1,
                                    'cols': 50
                                    # 'maxlength': 20
                                }
                            )
                        )
    description = forms.CharField(
                        required=False,
                        initial = 'Good, delivery location: ...',
                        widget=forms.Textarea(
                                attrs={
                                    "rows": 20,
                                    'cols': 60
                                }
                            )
                        )
    class Meta:
        model = Product
        fields = (
            'image_link_1',
            'image_link_2',
            'image_link_3',
            'image_link_4',
            'category',
            'title',
            'condition',
            'price_in_SGD',
            'description',
            'this_product_has_multiple_quantities',
            'delivery_location',
            'extra_information',
        )

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        initial = '5 star!',
        widget=forms.Textarea(attrs={
                                    "rows": 10,
                                    'cols': 60,
                                }
                            )
    )
    class Meta:
        model = Comment
        fields = ('comment',)