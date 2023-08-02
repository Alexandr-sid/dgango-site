from django.urls import path
from .views import shop_index, groups_list, create_product, products_list, orders_list, create_order

app_name = 'shopapp'

urlpatterns = [
    path(r"", shop_index, name="index"),
    path(r"groups/", groups_list, name="groups-list"),
    path(r"products/", products_list, name="products_list"),
    path(r"create_product/", create_product, name="create-product"),
    path(r"orders/", orders_list, name="orders_list"),
    path(r"create_order/", create_order, name="create_order"),
]
