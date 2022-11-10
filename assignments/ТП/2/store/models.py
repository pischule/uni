from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator

from accounts.models import User


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store:product-detail', args=[str(self.id)])


class ProductInstance(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    count = models.PositiveIntegerField()

    def __str__(self):
        return str(self.product) + ' -- ' + str(self.count)

    def get_absolute_url(self):
        return reverse("store:productinstance-detail", kwargs={"pk": self.pk})


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = 'CREATED', 'Created'
        DELIVERED = 'DELIVERED', 'Delivered'

    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.CREATED)
    placed_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    count = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    @property
    def total_price(self):
        return self.product.price * self.count

    def __str__(self):
        return f'{self.product.title}'

    def get_absolute_url(self):
        return reverse('store:order-detail', args=[str(self.id)])
