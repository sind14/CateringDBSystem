from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import MenuForm
from .models import (
    Client,
    Dish,
    Menu,
    Order,
    SavedOrder,
)


def index(request):
    """View function for the home page of the site."""

    clients_num = Client.objects.count()
    dishes_num = Dish.objects.count()
    menus_num = Menu.objects.count()

    context = {
        "clients_num": clients_num,
        "dishes_num": dishes_num,
        "menus_num": menus_num,
    }

    return render(request, "catering/index.html", context=context)


class DishListView(generic.ListView):
    model = Dish
    paginate_by = 5
    context_object_name = "dish_list"
    template_name = "catering/dish_list.html"


class DishCreateView(generic.CreateView):
    model = Dish
    fields = "__all__"
    template_name = "catering/create_form.html"
    success_url = reverse_lazy("catering_app:dish_list")


class MenuListView(generic.ListView):
    model = Menu
    context_object_name = "menu_list"
    template_name = "catering/menu_list.html"


class MenuDetailView(generic.DetailView):
    model = Menu
    template_name = "catering/menu_detail.html"


class MenuCreateView(generic.CreateView):
    model = Menu
    form_class = MenuForm
    template_name = "catering/create_form.html"
    success_url = reverse_lazy("catering_app:menu_list")


class MenuUpdateView(generic.UpdateView):
    model = Menu
    form_class = MenuForm
    template_name = "catering/create_form.html"
    success_url = reverse_lazy("catering_app:menu_list")


class MenuDeleteView(generic.DeleteView):
    model = Menu
    template_name = "catering/delete_form.html"
    success_url = reverse_lazy("catering_app:menu_list")


class ClientListView(generic.ListView):
    model = Client
    paginate_by = 5
    template_name = "catering/client_list.html"


class ClientCreateView(generic.CreateView):
    model = Client
    fields = "__all__"
    template_name = "catering/create_form.html"
    success_url = reverse_lazy("catering_app:client_list")


class OrderListView(generic.ListView):
    model = SavedOrder
    paginate_by = 5
    template_name = "catering/order_list.html"
    context_object_name = "order_list"


class OrderCreateView(generic.CreateView):
    model = Order
    fields = "__all__"
    template_name = "catering/create_form.html"
    success_url = reverse_lazy("catering_app:order_list")


class DishUpdateView(generic.UpdateView):
    model = Dish
    fields = ["price",]
    template_name = "catering/create_form.html"
    success_url = reverse_lazy("catering_app:dish_list")
