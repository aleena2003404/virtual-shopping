from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #  path('login/', views.login, name='login'),
    #  path('register/', views.register, name='register'),
     path('product/<int:id>/', views.product_detail, name='product_detail'),
     path('cart/', views.cart, name='cart'),
     path('register/', views.register, name='register'),
path('login/', views.user_login, name='login'),
path('logout/', views.user_logout, name='logout'),
]
