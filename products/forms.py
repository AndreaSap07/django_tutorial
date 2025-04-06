from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price',
            'summary',
        ]

class RawProductForm(forms.Form):
    title           = forms.CharField(label='Titolone')
    description     = forms.CharField(required=False, 
                                      widget= forms.Textarea(
                                          attrs={
                                              "class": "new-class-name two",
                                              "rows": 10,
                                              "cols": 80,
                                              "id": "my-id-textarea" 
                                          }
                                          ))
    price           = forms.DecimalField(initial=123.00)