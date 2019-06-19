from django import forms
from .models import Product, Comment


class ProductForm(forms.ModelForm):
    image_link_1 = forms.CharField(
                        required=True, 
                        widget=forms.Textarea(
                                attrs={
                                    "rows": 1,
                                    'cols': 60
                                }
                            )
                        )

    image_link_2 = forms.CharField(
                        required=False, 
                        widget=forms.Textarea(
                                attrs={
                                    "rows": 1,
                                    'cols': 60
                                }
                            )
                        )

    image_link_3 = forms.CharField(
                        required=False, 
                        widget=forms.Textarea(
                                attrs={
                                    "rows": 1,
                                    'cols': 60
                                }
                            )
                        )

    image_link_4 = forms.CharField(
                        required=False, 
                        widget=forms.Textarea(
                                attrs={
                                    "rows": 1,
                                    'cols': 60
                                }
                            )
                        )

    title = forms.CharField(
                        required=False, 
                        widget=forms.Textarea(
                                attrs={
                                    "rows": 1,
                                    'cols': 50
                                }
                            )
                        )
    description = forms.CharField(
                        required=False, 
                        widget=forms.Textarea(
                                attrs={
                                    "rows": 20,
                                    'cols': 60
                                }
                            )
                        )
    class Meta:
        model = Product
        fields = [
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
        ]
        abstract = True

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)