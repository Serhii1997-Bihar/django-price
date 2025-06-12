
from django.urls import path, include
from prices_app.views import get_prices, product_history, history, username_products, success, get_rozetka, get_rozetka_category, get_discounts

urlpatterns = [
    path('', get_prices, name='prices'),
    path('product_history/<int:id>/', product_history, name='product_history'),
    path('products/', history, name='history'),
    path('accounts/', include('allauth.urls')),
    path('<str:username>/products/', username_products, name='username_products'),
    path('success/', success, name='success'),
    path('rozetka/', get_rozetka),
    path('rozetka/discounts/', get_discounts, name='discount_products'),
    path('rozetka/<str:name>/', get_rozetka_category, name='category'),



]
