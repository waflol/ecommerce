from email import message
from multiprocessing import context
from time import timezone
from django.shortcuts import render,redirect
from core.forms import *
from django.views import View
from django.contrib import messages
from core.models import *
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
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
    # Get that particular product of id = pk
    product = Product.objects.get(pk=pk)
    
    # Create Order Item
    order_item, created = OrderItem.objects.get_or_create(
        product = product,
        user = request.user,
        ordered = False,
    )
    
    # Get query set of Order Object of Particular User
    order_qs = Order.objects.filter(user = request.user,ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk = pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,"Added quantity item")
            return redirect("product_desc",pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request,"Item add to cart")
            return redirect("product_desc",pk=pk)
        
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"Item add to cart")
        return redirect("product_desc",pk=pk)
    
def orderlist(request):
    if Order.objects.filter(user = request.user,ordered = False).exists():
        order = Order.objects.get(user = request.user,ordered = False)
        context = {'order':order}
        return render(request,'core/orderlist.html',context)
    context = {'message':"Your Cart is Empty"}
    return render(request,'core/orderlist.html',context)

def add_item(request,pk):
    product = Product.objects.get(pk=pk)
    
    # Create Order Item
    order_item, created = OrderItem.objects.get_or_create(
        product = product,
        user = request.user,
        ordered = False,
    )
    
    # Get query set of Order Object of Particular User
    order_qs = Order.objects.filter(user = request.user,ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk = pk).exists():
            if order_item.quantity < product.product_available_count:
                order_item.quantity += 1
                order_item.save()
                messages.info(request,"Added quantity item")
                return redirect("orderlist")
            else:
                messages.info(request,"Sorry! Product is out of Stock")
                return redirect("orderlist")
        else:
            order.items.add(order_item)
            messages.info(request,"Item add to cart")
            return redirect("product_desc",pk=pk)
        
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"Item add to cart")
        return redirect("product_desc",pk=pk)

def remove_item(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(
        user = request.user,
        ordered = False,
    )   
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk = pk).exists():
            order_item = OrderItem.objects.filter(
                product = item,
                user = request.user,
                ordered = False,
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request,"Item quantity was updated")
            return redirect("orderlist")
        else:
            messages.info(request,"This item is not in your cart!")
            return redirect("orderlist")
    else:
        messages.info(request,"You Do not have any Order!")
        return redirect("orderlist")
    