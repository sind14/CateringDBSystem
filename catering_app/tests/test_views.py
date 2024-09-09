from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catering_app.forms import DishNameSearchForm
from catering_app.models import Dish

DISH_LIST_URL = reverse("catering_app:dish_list")


class PublicDishListTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DISH_LIST_URL)
        self.assertRedirects(res, f"/accounts/login/?next={DISH_LIST_URL}")


class PrivateDishListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="PASSWORD",
        )
        self.client.force_login(self.user)

    def test_retrieve_dish_list(self):
        Dish.objects.create(dish_name="test", price=10.00)
        Dish.objects.create(dish_name="test2", price=15.25)
        res = self.client.get(DISH_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["dish_list"]),
            list(Dish.objects.all()),
        )
        self.assertTemplateUsed(res, "catering/dish_list.html")

    def test_search_dish(self):
        Dish.objects.create(dish_name="test", price=10.00)
        Dish.objects.create(dish_name="another", price=15.25)
        res = self.client.get(DISH_LIST_URL, {"dish_name": "test"})
        self.assertEqual(res.status_code, 200)
        self.assertIn("test", str(res.content))
        self.assertNotIn("another", str(res.content))
