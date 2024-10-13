from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from catering_app.models import Dish, Menu, Client

DISH_LIST_URL = reverse("catering_app:dish_list")
MENU_LIST_URL = reverse("catering_app:menu_list")
CLIENT_LIST_URL = reverse("catering_app:client_list")


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="PASSWORD",
        )
        self.client.force_login(self.user)

        self.dish1 = Dish.objects.create(dish_name="Soup", price=5.50)
        self.dish2 = Dish.objects.create(dish_name="Salad", price=7.00)
        self.menu1 = Menu.objects.create(menu_name="Lunch Menu")
        self.menu1.menu_dishes.set([self.dish1, self.dish2])
        self.menu2 = Menu.objects.create(menu_name="Dinner Menu")
        self.menu2.menu_dishes.set([self.dish1, self.dish2])
        self.client1 = Client.objects.create(client_name="Alice")
        self.client2 = Client.objects.create(client_name="Bob")


class PublicDishListTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DISH_LIST_URL)
        self.assertRedirects(res, f"/accounts/login/?next={DISH_LIST_URL}")


class PublicMenuListTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MENU_LIST_URL)
        self.assertRedirects(res, f"/accounts/login/?next={MENU_LIST_URL}")


class PublicClientListTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CLIENT_LIST_URL)
        self.assertRedirects(res, f"/accounts/login/?next={CLIENT_LIST_URL}")



class PrivateDishListTest(BaseTest):
    def test_create_dish(self):
        res = self.client.get(DISH_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["dish_list"]),
            list(Dish.objects.all()),
        )
        self.assertTemplateUsed(res, "catering/dish_list.html")

    def test_search_dish(self):
        res = self.client.get(DISH_LIST_URL, {"dish_name": "Soup"})
        self.assertEqual(res.status_code, 200)
        self.assertIn("Soup", str(res.content))
        self.assertNotIn("Salad", str(res.content))

    def test_delete_dish(self):
        Dish.objects.filter(dish_name="Soup").delete()
        res = self.client.get(DISH_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["dish_list"]),
            list(Dish.objects.all()),
        )
        self.assertTemplateUsed(res, "catering/dish_list.html")


class PrivateMenuListTest(BaseTest):
    def test_create_menu(self):
        menu = Menu.objects.create(menu_name="New Menu")
        menu.menu_dishes.set([self.dish1, self.dish2])
        self.assertEqual(menu.menu_name, "New Menu")
        self.assertIn(self.dish1, menu.menu_dishes.all())
        self.assertIn(self.dish2, menu.menu_dishes.all())
        self.assertEqual(menu.menu_dishes.count(), 2)

    def test_delete_menu(self):
        Menu.objects.filter(menu_name="Lunch Menu").delete()
        res = self.client.get(MENU_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertNotIn(self.menu1, Menu.objects.all())
        self.assertIn(self.menu2, Menu.objects.all())
        self.assertTemplateUsed(res, "catering/menu_list.html")


class PrivateClientListTest(BaseTest):
    def test_create_client(self):
        res = self.client.get(CLIENT_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Alice", str(res.content))
        self.assertIn("Bob", str(res.content))

    def test_search_client(self):
        res = self.client.get(CLIENT_LIST_URL, {"client_name": "Bob"})
        self.assertEqual(res.status_code, 200)
        self.assertIn("Bob", str(res.content))
        self.assertNotIn("Alice", str(res.content))
