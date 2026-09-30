from django.test import TestCase

from product.factories import CategoryFactory, ProductFactory
from product.serializers import ProductSerializer


class TestProductSerializer(TestCase):
    def setUp(self) -> None:
        self.category = CategoryFactory(title="technology")
        self.product_1 = ProductFactory(
            title="mouse",
            price=100,
            category=[self.category],
        )
        self.product_serializer = ProductSerializer(self.product_1)

    def test_product_serializer(self):
        serializer_data = self.product_serializer.data

        self.assertEquals(serializer_data["price"], 100)
        self.assertEquals(serializer_data["title"], "mouse")

    def test_product_fields(self):
        serializer_data = self.product_serializer.data

        self.assertIn("id", serializer_data)
        self.assertIn("title", serializer_data)
        self.assertIn("description", serializer_data)
        self.assertIn("price", serializer_data)
        self.assertIn("active", serializer_data)
        self.assertIn("category", serializer_data)

    def test_product_category_relationship(self):
        serializer_data = self.product_serializer.data

        self.assertEquals(
            serializer_data["category"][0]["title"],
            "technology",
        )

    def test_product_creation_with_category(self):
        data = {
            "title": "keyboard",
            "description": "Mechanical keyboard",
            "price": 200,
            "active": True,
            "categories_id": [self.category.id],
        }

        serializer = ProductSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        product = serializer.save()

        self.assertEquals(product.title, "keyboard")
        self.assertEquals(product.price, 200)
        self.assertIn(self.category, product.category.all())