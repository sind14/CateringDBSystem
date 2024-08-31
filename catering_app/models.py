from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"


class Client(models.Model):
    client_name = models.CharField(max_length=100, unique=True)
    client_address = models.CharField(max_length=100)

    def __str__(self):
        return self.client_name


class SavedDish(models.Model):
    dish_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.dish_name


class SavedMenu(models.Model):
    menu_name = models.CharField(max_length=50)
    menu_dishes = models.ManyToManyField(SavedDish, related_name="saved_menus")

    @property
    def total_price(self):
        return self.menu_dishes.aggregate(total=Sum('price'))['total']


class SavedOrder(models.Model):
    num_people = models.IntegerField()
    order_menu = models.ForeignKey(SavedMenu, related_name="saved_orders", on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name="saved_orders", on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-order_date',)

    @property
    def total_price(self):
        return self.order_menu.total_price * self.num_people

    def __str__(self):
        return f"Order {self.id} by {self.client.client_name}"


class Dish(models.Model):
    dish_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.dish_name


class Menu(models.Model):
    menu_name = models.CharField(max_length=50)
    menu_dishes = models.ManyToManyField(Dish, related_name="menus")

    @property
    def total_price(self):
        return self.menu_dishes.aggregate(total=Sum('price'))['total']

    def __str__(self):
        return self.menu_name


class Order(models.Model):
    num_people = models.IntegerField()
    order_menu = models.ForeignKey(Menu, related_name="orders", on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name="orders", on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.order_menu.total_price * self.num_people


@receiver(post_save, sender=Order)
def create_saved_order(sender, instance, created, **kwargs):
    if created:
        saved_menu = SavedMenu.objects.create(menu_name=instance.order_menu.menu_name)

        for dish in instance.order_menu.menu_dishes.all():
            saved_dish = SavedDish.objects.create(
                dish_name=dish.dish_name,
                price=dish.price
            )
            saved_menu.menu_dishes.add(saved_dish)

        SavedOrder.objects.create(
            num_people=instance.num_people,
            order_menu=saved_menu,
            client=instance.client,
            order_date=instance.order_date
        )
