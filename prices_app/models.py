from django.db import models
from django.contrib.auth.models import User

class PersonModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')
    telegram = models.CharField(max_length=20, verbose_name="Telegram Username", unique=True)
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


class DepartmentRozetkaModels(models.Model):
    name = models.CharField(max_length=250)
    icon = models.ImageField(upload_to="images/", null=True, blank=True)

    class Meta:
        managed = False  # Django не буде створювати/видаляти цю таблицю
        db_table = 'rozetka_app_departmentrozetkamodels'  # Точна назва в базі

    def __str__(self):
        return self.name

class ProductRoz(models.Model):
    department_foreign_key = models.ForeignKey(DepartmentRozetkaModels, on_delete=models.SET_NULL, null=True,
                                               blank=True, related_name='products')
    department = models.CharField(max_length=250, null=True, blank=True)
    category = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=500)
    price = models.CharField(max_length=50, null=True, blank=True)
    price_old = models.CharField(max_length=50, null=True, blank=True)
    discount = models.PositiveIntegerField(null=True, blank=True)
    bonus = models.CharField(max_length=250, default=None, null=True, blank=True)
    status = models.CharField(max_length=25, default='New')
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    link = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'rozetka_app_productroz'
