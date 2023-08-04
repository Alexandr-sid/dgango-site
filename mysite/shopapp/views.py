from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView

from .forms import ProductForm, OrderForm, GroupForm
from .models import Product, Order


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = Product.objects.all()
        context = {
            'time_runner': default_timer(),
            'products': products,
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailView(DetailView):
    template_name = 'shopapp/product-details.html'
    model = Product
    context_object_name = 'product'


class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)

class ProductCreateView(CreateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    success_url = reverse_lazy('shopapp:products_list')


class ProductUpdateView(UpdateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    context_object_name = "product"
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)



class OrdersListView(ListView):
    template_name = 'shopapp/orders_list.html'
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )
    context_object_name = 'orders'


class OrdersDetailView(DetailView):
    template_name = 'shopapp/order_detail.html'
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


def create_order(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        print(request.POST.dict())
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse("shopapp:orders_list")
            return redirect(url)
    else:
        form = OrderForm()
    context = {
        "form": form
    }
    return render(request, 'shopapp/create-order.html', context=context)
