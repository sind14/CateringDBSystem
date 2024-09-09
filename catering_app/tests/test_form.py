from django.test import TestCase
from catering_app.forms import (
    MenuForm,
    ClientNameSearchForm,
    DishNameSearchForm,
    OrderSearchForm
)
from catering_app.models import Dish


class MenuFormTest(TestCase):
    def setUp(self):
        self.dish1 = Dish.objects.create(dish_name="Dish 1", price=10.00)
        self.dish2 = Dish.objects.create(dish_name="Dish 2", price=20.00)
        self.form_data = {
            "menu_name": "Test Menu",
            "menu_dishes": [self.dish1.id, self.dish2.id]
        }

    def test_form_valid(self):
        form = MenuForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = MenuForm(data={})
        self.assertFalse(form.is_valid())

    def test_form_has_dish_choices(self):
        form = MenuForm()
        self.assertIn(self.dish1, form.fields["menu_dishes"].queryset)
        self.assertIn(self.dish2, form.fields["menu_dishes"].queryset)


class ClientNameSearchFormTest(TestCase):
    def test_form_valid(self):
        form = ClientNameSearchForm(data={"client_name": "Test Client"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["client_name"], "Test Client")

    def test_form_invalid(self):
        form = ClientNameSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["client_name"], "")


class DishNameSearchFormTest(TestCase):
    def test_form_valid(self):
        form = DishNameSearchForm(data={"dish_name": "Test Dish"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["dish_name"], "Test Dish")

    def test_form_invalid(self):
        form = DishNameSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["dish_name"], "")


class OrderSearchFormTest(TestCase):
    def test_form_valid(self):
        form = OrderSearchForm(data={"client": "Test Client"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["client"], "Test Client")

    def test_form_invalid(self):
        form = OrderSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["client"], "")
