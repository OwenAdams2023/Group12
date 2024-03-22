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
    path('checkout/', views.checkout, name='checkout'),
    path('orderhistory/', views.order_history, name='orderhistory'),
    path('return_request/<int:order_id>/', views.return_request, name='return_request'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_info/', views.update_info, name='update_info'),
    path('update_user/', views.update_user, name='update_user'),
    path('earning/', views.update_earning, name='earning'),
]
