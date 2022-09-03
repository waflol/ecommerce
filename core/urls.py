from django.urls import path
from core import views

urlpatterns = [
    path('', views.index,name='index'),
    path('add_product/',views.Add_Product.as_view(),name='add_product'),
    path('product_desc/<pk>',views.product_desc,name='product_desc'),
    path('add_to_cart/<pk>',views.add_to_cart,name='add_to_cart'),
    path('orderlist/',views.orderlist,name='orderlist'),
    path('add_item/<int:pk>',views.add_item,name='add_item'),
    path('remove_item/<int:pk>',views.remove_item,name='remove_item'),
]