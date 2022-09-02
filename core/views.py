from django.shortcuts import render,redirect
from core.forms import ProductForms

from core.models import Product

# Create your views here.
def index(request):
    return render(request,'core/index.html')

def add_product(request):
    if request.method == 'POST':
        form = ProductForms(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form = ProductForms()

    return render(request,'core/add_product.html',{'form':form})
    
    