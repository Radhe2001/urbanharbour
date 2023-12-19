from . import views
from django.urls import path


urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('login/',views.user_login,name='login'),
    path('register/',views.register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('brand/',views.brand_page,name='brand'),
    path('cart/',views.cart,name='cart'),
    path('order/',views.order,name='order'),
    path('category/',views.category_page,name='category'),
    path('product/',views.product_page,name='product'),
    path('offer/',views.offer_page,name='offer'),
    path('brand_detail/<int:id>/',views.brand_detail,name='brand_detail'),
    path('category_detail/<int:id>/',views.category_detail,name='category_detail'),
    path('detail/<int:id>/',views.detail,name='detail'),
    path('add_to_cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
    path('add_to_order/<int:id>/',views.add_to_order,name='add_to_order'),
] 
