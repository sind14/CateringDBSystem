from decimal import Decimal

from django.test import TestCase

from catering_app.models import (
    Client,
    Dish,
    Menu,
    Order,
    SavedMenu,
    SavedOrder
)


class ModelTests(TestCase):
    def create_menu(self):
        self.dish1 = Dish.objects.create(dish_name="Dish 1", price=Decimal("10.50"))
        self.dish2 = Dish.objects.create(dish_name="Dish 2", price=Decimal("20.00"))
        self.dish3 = Dish.objects.create(dish_name="Dish 3", price=Decimal("5.00"))
        self.menu = Menu.objects.create(menu_name="Test Menu")
        self.menu.menu_dishes.add(self.dish1, self.dish2, self.dish3)
        return self.menu

    def test_client_str(self):
        client = Client.objects.create(client_name="test")
        self.assertEqual(str(client), client.client_name)

    def test_dish_str(self):
        dish = Dish.objects.create(dish_name="test", price=100)
        self.assertEqual(str(dish), dish.dish_name)

    def test_menu_total_price(self):
        self.create_menu()
        total_price = self.menu.total_price
        expected_total_price = Decimal("10.50") + Decimal("20.00") + Decimal("5.00")
        self.assertEqual(total_price, expected_total_price)

    def test_create_saved_orders(self):
        client = Client.objects.create(client_name="Test Client")
        order = Order.objects.create(
            num_people=5,
            order_menu=self.create_menu(),
            client=client,
            order_date="2024-09-09",
            )
        saved_menu = SavedMenu.objects.get(menu_name=self.menu.menu_name)
        saved_order = SavedOrder.objects.get(order_menu=saved_menu)
        self.assertIsNotNone(saved_menu)
        self.assertIsNotNone(saved_order)
        self.assertEqual(saved_menu.menu_dishes.count(), 3)
        self.assertEqual(saved_order.client, client)
        self.assertEqual(saved_order.order_date.date(), order.order_date.date())
