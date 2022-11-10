from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'store'
urlpatterns = [
    path('about/', views.index, name='about'),
    path('', RedirectView.as_view(url='catalog/', permanent=True)),
    path('catalog/', views.CatalogListView.as_view(), name='catalog'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('product-instance/<int:pk>', views.ProductInstanceDetailView.as_view(), name='productinstance-detail'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/buyer', views.OrderBuyerListView.as_view(), name='orders-buyer'),
    path('order/create', views.OrderCreateView.as_view(), name='order-create'),
    path('seller/products', views.SellerProductListView.as_view(), name='seller-products'),
    path('seller/product/create', views.SellerCreateProductView.as_view(), name='seller-product-create'),
    path('seller/product/<int:pk>/update', views.SellerEditProductView.as_view(), name='seller-product-update'),
    path('seller/product/<int:pk>/delete', views.SellerProductDeleteView.as_view(), name='seller-product-delete'),
    path('seller/product-instances', views.SellerProductInstanceListView.as_view(), name='seller-productinstances'),
    path('seller/product-instance/create', views.SellerProductInstanceCreateView.as_view(), name='seller-productinstance-create'),
    path('seller/product-instance/<int:pk>/update', views.SellerProductInstanceUpdateView.as_view(), name='seller-productinstance-update'),
    path('seller/product-instance/<int:pk>/delete', views.SellerProductInstanceDeleteView.as_view(), name='seller-productinstance-delete'),
    path('buyer/product-instance/<int:pk>/order', views.BuyerProductInstanceOrder.as_view(), name='user-order-product-instance'),
    path('seller/orders', views.SellerSoldOrders.as_view(), name='seller-sold-orders'),
    path('delivery/orders', views.DeliveryOrdersToDeliverList.as_view(), name='delivery-order-list'),
    path('delivery/history/orders', views.DeliveryOrderHistory.as_view(), name='delivery-order-history-list'),
    path('delivery/order/<int:pk>/update', views.DeliveryOrderUpdateStatus.as_view(), name='delivery-order-update')
]
