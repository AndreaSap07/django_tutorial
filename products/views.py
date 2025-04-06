from django.shortcuts import render
from .models import Product
from .forms import ProductForm, RawProductForm

# Create your views here.

# Pure Django Form
def product_create_view(request):

    my_form = RawProductForm()
    if request.method == 'POST':
        my_form = RawProductForm(request.POST)
        if my_form.is_valid():
            print(my_form.cleaned_data)
            Product.objects.create(**my_form.cleaned_data)
        else:
            print(my_form.errors)

    context = {
        "form": my_form
    }
    return render(request, "product/product_create.html", context)



"""
#WIth RAW html
def product_create_view(request):

    if request.method == 'POST':
        my_new_title = request.POST.get('title') #qua nella stringa va messo quello che mettiamo in "name" nell'html!
        print(my_new_title)
    context = {}
    return render(request, "product/product_create.html", context)
"""


""" 
#With the Django input 
def product_create_view(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ProductForm()
    context = {
        'form': form
        }
    return render(request, "product/product_create.html", context)
"""

def product_detail_view(request):
    obj = Product.objects.get(id=1)
    context = {
        'object': obj,
        }
    return render(request, "product/detail.html", context)