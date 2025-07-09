
from django.urls import path, include
from prices_app.views import get_prices, product_info, history, username_products, success, username_info, contacts, about

urlpatterns = [
    path('', get_prices, name='prices'),
    path('product_history/<int:id>/', product_info, name='product_info'),
    path('products/', history, name='history'),
    path('accounts/', include('allauth.urls')),
    path('<str:username>/products/', username_products, name='username_products'),
    path('success/', success, name='success'),
    path('<str:username>/info/', username_info, name='username_info'),
    path('contacts', contacts, name='contacts'),
    path('about', about, name='about')

]
