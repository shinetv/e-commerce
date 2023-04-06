from django.urls import path
from . import views

app_name='my_cart'


urlpatterns=[
    path('add/<int:product_id>/',views.add_cart,name="add_cart"),
    path('cart_detail',views.cart_detail,name="cart_detail"),
    path('remove/<int:product_id>/',views.remove,name="remove"),
    path('Total_remove/<int:product_id>/',views.remove,name="Total_remove"),
    path('success',views.success,name="success")
   

]