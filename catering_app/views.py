from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import (
    MenuForm,
    ClientNameSearchForm,
    DishNameSearchForm,
    OrderSearchForm,
)
from .models import (
    Client,
    Dish,
    Menu,
    Order,
    SavedOrder,
    SavedMenu,
)


@login_required
def index(request):
    """View function for the home page of the site."""

    clients_num = Client.objects.count()
    dishes_num = Dish.objects.count()
    menus_num = Menu.objects.count()
    orders_num = SavedOrder.objects.count()

    context = {
        "clients_num": clients_num,
        "dishes_num": dishes_num,
        "menus_num": menus_num,
        "orders_num": orders_num,
    }

    return render(request, "catering/index.html", context=context)


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 5
    context_object_name = "dish_list"
    template_name = "catering/dish_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        dish_name = self.request.GET.get("dish_name", "")
        context["search_form"] = DishNameSearchForm(
            initial={"dish_name": dish_name}
        )
        return context

    def get_queryset(self):
        form = DishNameSearchForm(self.request.GET)
        if form.is_valid():
            return Dish.objects.filter(
                dish_name__icontains=form.cleaned_data["dish_name"]
            )
        return Dish.objects.all()


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    fields = "__all__"
    template_name = "catering/create_form.html"
    success_url = reverse_lazy("catering_app:dish_list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "catering/delete_form.html"
    success_url = reverse_lazy("catering_app:dish_list")


class MenuListView(LoginRequiredMixin, generic.ListView):
    model = Menu
    context_object_name = "menu_list"
    template_name = "catering/menu_list.html"


class MenuDetailView(LoginRequiredMixin, generic.DetailView):
    model = Menu
    template_name = "catering/menu_detail.html"


class SavedMenuDetailView(LoginRequiredMixin, generic.DetailView):
    model = SavedMenu
    template_name = "catering/saved_menu_detail.html"


class MenuCreateView(LoginRequiredMixin, generic.CreateView):
    model = Menu
    form_class = MenuForm
    template_name = "catering/create_form.html"
    success_url = reverse_lazy("catering_app:menu_list")


class MenuUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Menu
    form_class = MenuForm
    template_name = "catering/create_form.html"
    success_url = reverse_lazy("catering_app:menu_list")


class MenuDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Menu
    template_name = "catering/delete_form.html"
    success_url = reverse_lazy("catering_app:menu_list")


class ClientListView(LoginRequiredMixin, generic.ListView):
    model = Client
    paginate_by = 5
    template_name = "catering/client_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        client_name = self.request.GET.get("client_name", "")
        context["search_form"] = ClientNameSearchForm(
            initial={"client_name": client_name}
        )
        return context

    def get_queryset(self):
        form = ClientNameSearchForm(self.request.GET)
        if form.is_valid():
            return Client.objects.filter(
                client_name__icontains=form.cleaned_data["client_name"]
            )
        return Client.objects.all()


class ClientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Client
    fields = "__all__"
    template_name = "catering/create_form.html"
    success_url = reverse_lazy("catering_app:client_list")


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = SavedOrder
    paginate_by = 5
    template_name = "catering/order_list.html"
    context_object_name = "order_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        client = self.request.GET.get("client", "")
        context["search_form"] = OrderSearchForm(
            initial={"client": client}
        )
        return context

    def get_queryset(self):
        form = OrderSearchForm(self.request.GET)
        if form.is_valid():
            return SavedOrder.objects.filter(
                client__client_name__icontains=form.cleaned_data["client"]
            )
        return Order.objects.all()


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    fields = "__all__"
    template_name = "catering/create_form.html"
    success_url = reverse_lazy("catering_app:order_list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    fields = ["price", ]
    template_name = "catering/create_form.html"
    success_url = reverse_lazy("catering_app:dish_list")
