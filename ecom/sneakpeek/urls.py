from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('search/', views.search, name='search'),
    path('add_product/', views.add_product, name='add_product'),
    path('payment_success', views.payment_success, name='payment_success'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:cat_name>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
]
