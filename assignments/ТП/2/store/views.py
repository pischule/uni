from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from .models import Product, Order, ProductInstance, User
from .forms import SellerCreateProductInstanceForm


def index(request):
    context = {
        'num_products': Product.objects.count(),
        'num_orders': Order.objects.count(),
        'num_user': User.objects.count(),
        'catalog_items': ProductInstance.objects.filter(count__gt=0).count(),
        'num_buyer': User.objects.filter(user_type=User.BUYER).count(),
        'num_seller': User.objects.filter(user_type=User.SELLER).count(),
        'num_delivery': User.objects.filter(user_type=User.DELIVERY).count(),
    }

    return render(request, 'index.html', context=context)


class CatalogListView(generic.ListView):
    model = ProductInstance
    template_name = "store/catalog.html"

    def get_queryset(self):
        return ProductInstance.objects.filter(count__gt=0)


class ProductInstanceDetailView(generic.DetailView):
    model = ProductInstance


class ProductDetailView(generic.DetailView):
    model = Product


class OrderListView(generic.ListView):
    model = Order


class OrderDetailView(generic.DetailView):
    model = Order


class OrderBuyerListView(LoginRequiredMixin, generic.ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    fields = ['product', 'count']

    def form_valid(self, form):
        form.instance.buyer = self.request.user
        return super(OrderCreateView, self).form_valid(form)


class SellerProductListView(LoginRequiredMixin, generic.ListView):
    model = Product
    template_name = 'store/seller_product_list.html'

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)


class SellerCreateProductView(LoginRequiredMixin, generic.CreateView):
    fields = ['title', 'price']
    model = Product
    success_url = reverse_lazy('store:seller-products')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super(SellerCreateProductView, self).form_valid(form)


class SellerEditProductView(LoginRequiredMixin, generic.UpdateView):
    fields = ['title', 'price']
    model = Product
    success_url = reverse_lazy('store:seller-products')


class SellerProductInstanceListView(LoginRequiredMixin, generic.ListView):
    model = ProductInstance
    template_name = 'store/seller_productinstance_list.html'

    def get_queryset(self):
        return ProductInstance.objects.filter(product__seller=self.request.user)


class SellerProductInstanceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ProductInstance
    fields = ['product', 'count']
    template_name = 'store/seller_productinstance_form.html'
    success_url = reverse_lazy('store:seller-productinstances')


class SellerSoldOrders(LoginRequiredMixin, generic.ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(product__seller=self.request.user)


class BuyerProductInstanceOrder(LoginRequiredMixin, generic.CreateView):
    model = Order
    fields = ['count']

    def form_valid(self, form):
        product_instance = ProductInstance.objects.get(pk=self.kwargs['pk'])

        if form.instance.count > product_instance.count:
            form.instance.count = None
            return super(BuyerProductInstanceOrder, self).form_invalid(form)

        form.instance.buyer = self.request.user
        form.instance.status = Order.Status.CREATED
        form.instance.product = product_instance.product

        product_instance.count -= form.instance.count
        product_instance.save()

        return super(BuyerProductInstanceOrder, self).form_valid(form)


class SellerProductInstanceCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = SellerCreateProductInstanceForm
    template_name = 'store/seller_productinstance_form.html'
    success_url = reverse_lazy('store:seller-productinstances')

    def get_form_kwargs(self):
        kwargs = super(SellerProductInstanceCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class SellerProductDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Product
    success_url = reverse_lazy('store:seller-products')


class SellerProductInstanceDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ProductInstance
    success_url = reverse_lazy('store:seller-productinstances')


class DeliveryOrdersToDeliverList(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'store/delivery_orders_todeliver.html'

    def get_queryset(self):
        return Order.objects.filter(status=Order.Status.CREATED)


class DeliveryOrderHistory(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'store/delivery_orders_history.html'

    def get_queryset(self):
        return Order.objects.filter(status=Order.Status.DELIVERED)


class DeliveryOrderUpdateStatus(LoginRequiredMixin, generic.UpdateView):
    fields = ['status']
    model = Order
    success_url = reverse_lazy('store:delivery-order-list')
