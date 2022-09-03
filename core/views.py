from email import message
from multiprocessing import context
from django.shortcuts import render,redirect
from core.forms import *
from django.views import View
from django.contrib import messages
from core.models import *
from django.http import HttpResponse

# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request,'core/index.html',context)


class Add_Product(View):
    def put(self,request):
        pass
    def get(self,request):
        form = ProductForms()
        context = {'form':form}
        return render(request,'core/add_product.html',context)
    def post(self,request):
        form = ProductForms(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request,'Data save successfully!')
            return redirect('add_product')
        else:
            print('Not Working')
            messages.info(request,'Product is not added. Try Again!')
            return redirect('add_product')


def product_desc(request,pk):
    product = Product.objects.get(pk=pk)
    context = {'product':product}
    return render(request,'core/product_desc.html',context)

def add_to_cart(request,pk):
    product = Product.objects.get(pk=pk)
    
def orderlist(request):
    pass

def add_item(request,pk):
    pass

def remove_item(request,pk):
    pass    
    