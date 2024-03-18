from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register_user, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('payment_success', views.payment_success, name='paymemt_success'),
    path('search', views.search, name='search'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),
    path('return_request/<int:order_id>/', views.return_request, name='return_request'),
    path('return_request_success/', views.return_request_success, name='return_request_success'),
]


