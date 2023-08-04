from django.urls import path
from .views import (
    ShopIndexView,
    GroupsListView,
    ProductDetailView,
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrdersListView,
    OrdersDetailView,
    create_order)

app_name = 'shopapp'

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupsListView.as_view(), name="groups-list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("products/create/", ProductCreateView.as_view(), name="create_product"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/<int:pk>/", OrdersDetailView.as_view(), name="order_detail"),
    path("create_order/", create_order, name="create_order"),
]
