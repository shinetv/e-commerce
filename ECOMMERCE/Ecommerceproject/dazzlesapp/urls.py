from . import views
from django.urls import path

app_name='dazzlesapp'

urlpatterns = [
    path('',views.allprodcat,name='allprodcat'),
    path('<slug:c_slug>/',views.allprodcat,name='product_by_category'),
    path('<slug:c_slug>/<slug:product_slug>/',views.ProDetail,name='productCatdetail'),
    path('searchresult',views.searchresult,name="searchresult"),
   
]