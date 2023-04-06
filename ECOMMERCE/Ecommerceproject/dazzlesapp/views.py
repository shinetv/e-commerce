from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from . models import *
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.db.models import Q



# Create your views here.
def allprodcat(request,c_slug=None):
    c_page = None
    products_list = None
    if c_slug != None:
        c_page = get_object_or_404 (Category, slug = c_slug)
        products_list = Product.objects.all().filter(category =c_page, available = True)
    else:
        products_list = Product.objects.all().filter(available = True)
    paginator = Paginator(products_list, 2)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request, "category.html", {'category' : c_page, 'products' : products})

def searchresult(request):
    product=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        product=Product.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))
        return render(request,'search.html',{'query':query,'product':product})
    return render(request,'search.html')


def ProDetail(request, c_slug, product_slug):
    try:
        product = Product.objects.get(category__slug = c_slug, slug = product_slug)
    except Exception as e:
        raise e
    return render(request, "product.html", {'product' : product})




    