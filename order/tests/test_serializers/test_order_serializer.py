from django.test import TestCase

from order.factories import OrderFactory, ProductFactory
from order.serializers import OrderSerializer


class TestOrderSerializer(TestCase):
    def setUp(self) -> None:
        self.product_1 = ProductFactory(price=100)
        self.product_2 = ProductFactory(price=200)

        self.order = OrderFactory(
            product=(self.product_1, self.product_2)
        )
        self.order_serializer = OrderSerializer(self.order)

    def test_order_serializer(self):
        serializer_data = self.order_serializer.data

        self.assertEquals(
            serializer_data["product"][0]["title"],
            self.product_1.title,
        )
        self.assertEquals(
            serializer_data["product"][1]["title"],
            self.product_2.title,
        )

    def test_order_fields(self):
        serializer_data = self.order_serializer.data

        self.assertIn("product", serializer_data)
        self.assertIn("total", serializer_data)
        self.assertIn("user", serializer_data)

    def test_order_total(self):
        serializer_data = self.order_serializer.data

        self.assertEquals(serializer_data["total"], 300)

    def test_order_creation_with_products(self):
        data = {
            "user": self.order.user.id,
            "products_id": [
                self.product_1.id,
                self.product_2.id,
            ],
        }

        serializer = OrderSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        order = serializer.save()

        self.assertEquals(order.user, self.order.user)
        self.assertIn(self.product_1, order.product.all())
        self.assertIn(self.product_2, order.product.all())