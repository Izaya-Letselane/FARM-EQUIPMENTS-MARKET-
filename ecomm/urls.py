from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('checkout/', views.checkout, name="checkout"),
    path('about/', views.about, name="about"),
    path('search/', views.search, name="search"),
    path('shop/', views.shop, name="shop"),
    path('login/', views.login_user, name="login"),
    path('invoice/', views.invoice, name="invoice"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('update_user/', views.update_user, name="update_user"),
    path('update_info/', views.update_info, name="update_info"),
    path('update_password/', views.update_password, name="update_password"),
    path('product/<int:pk>', views.product, name="product"),
]