from django.urls import path
from catering_app import views
from catering_app.views import (
    DishListView,
    DishCreateView,
    MenuListView,
    MenuCreateView,
    MenuDetailView,
    ClientListView,
    ClientCreateView,
    OrderListView,
    OrderCreateView,
    DishUpdateView,
    MenuUpdateView,
    MenuDeleteView,
)

app_name = "catering_app"

urlpatterns = [
    path('', views.index, name='index'),
    path("dishes", DishListView.as_view(), name="dish_list"),
    path("dishes/create/", DishCreateView.as_view(), name="dish_create"),
    path("dishes/<int:pk>/update", DishUpdateView.as_view(), name="dish_update"),
    path("menus", MenuListView.as_view(), name="menu_list"),
    path("menus/create/", MenuCreateView.as_view(), name="menu_create"),
    path("menus/<int:pk>/update/", MenuUpdateView.as_view(), name="menu_update"),
    path("menus/<int:pk>/delete/", MenuDeleteView.as_view(), name="menu_delete"),
    path("menus/<int:pk>/", MenuDetailView.as_view(), name="menu_detail"),
    path("clients", ClientListView.as_view(), name="client_list"),
    path("clients/create/", ClientCreateView.as_view(), name="client_create"),
    path("orders", OrderListView.as_view(), name="order_list"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
]
