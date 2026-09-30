from django.test import TestCase

from product.factories import CategoryFactory
from product.serializers import CategorySerializer


class TestCategorySerializer(TestCase):
    def setUp(self) -> None:
        self.category = CategoryFactory(title="food")
        self.category_serializer = CategorySerializer(self.category)

    def test_category_serializer(self):
        serializer_data = self.category_serializer.data

        self.assertEquals(serializer_data["title"], "food")
        self.assertIn("slug", serializer_data)
        self.assertIn("description", serializer_data)
        self.assertIn("active", serializer_data)

    def test_category_valid_data(self):
        data = {
            "title": "food",
            "description": "Food category",
            "active": True,
        }

        serializer = CategorySerializer(data=data)

        self.assertTrue(serializer.is_valid())

