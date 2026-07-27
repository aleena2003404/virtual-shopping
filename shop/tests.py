from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Category, Product, Cart


class ShoppingProjectTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="aleena",
            password="1234"
        )

        self.category = Category.objects.create(
            name="Cashew"
        )
           
        self.product = Product.objects.create(
            category=self.category,
            name="Premium Cashew",
            description="Best Quality",
            price=500,
            stock=10,
            image="products/test.jpg"
        )

    # Home Page
    def test_home_page(self):

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

    # Login
    def test_user_login(self):

        login = self.client.login(
            username="aleena",
            password="1234"
        )

        self.assertTrue(login)

    # Product Detail
    def test_product_detail(self):

        response = self.client.get(
            reverse("product_detail",
            args=[self.product.id])
        )

        self.assertEqual(response.status_code, 200)

    # Product Created
    def test_product_exists(self):

        self.assertEqual(
            Product.objects.count(),
            1
        )

    # Add To Cart
    def test_add_to_cart(self):

        self.client.login(
            username="aleena",
            password="1234"
        )

        self.client.post(
            reverse("add_to_cart",
            args=[self.product.id]),
            {
                "quantity":2
            }
        )

        self.assertEqual(
            Cart.objects.count(),
            1
        )

    # Cart Quantity
    def test_cart_quantity(self):

        Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=3
        )

        cart = Cart.objects.first()

        self.assertEqual(
            cart.quantity,
            3
        )

    # Remove Cart
    def test_remove_cart(self):

        self.client.login(
            username="aleena",
            password="1234"
        )

        cart = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )

        self.client.get(
            reverse(
                "remove_cart",
                args=[cart.id]
            )
        )

        self.assertEqual(
            Cart.objects.count(),
            0
        )

    # Product Stock
    def test_product_stock(self):

        self.assertEqual(
            self.product.stock,
            10
        )