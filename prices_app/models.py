from django.db import models
from django.contrib.auth.models import User

class PersonModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')
    telegram = models.CharField(max_length=20, verbose_name="Telegram Username", unique=True, blank=True, null=True)
    chat_id = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telegram Chat ID")

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"
        ordering = ['user__username']

    def __str__(self):
        return self.user.username


class ProductModel(models.Model):
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    product_name = models.CharField(max_length=400, verbose_name="Product Name")
    link = models.URLField(max_length=400, verbose_name="Product link", null=True, blank=True)
    users = models.ManyToManyField(User, related_name="products", verbose_name="Users who added the product", blank=True)

    class Meta:
        verbose_name = "Product Price"
        verbose_name_plural = "Product Prices"
        ordering = ['-id']

    def __str__(self):
        return f"{self.product_name}"



class PriceModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="prices", verbose_name="Product")
    person = models.ForeignKey(PersonModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Who added the price")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Price")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Old price")
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Discount")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")

    def __str__(self):
        return f"{self.price} on {self.date.date()}"


