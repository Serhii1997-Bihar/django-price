from django.contrib import admin
from .models import PersonModel, ProductModel, PriceModel

@admin.register(PersonModel)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("get_username", "telegram", "get_email", "chat_id")
    search_fields = ("user__username", "telegram", "user__email")
    ordering = ("user__username",)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = "Username"

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "link", "get_users")
    search_fields = ("product_name", "link")
    list_filter = ("users",)

    def get_users(self, obj):
        return ", ".join([user.username for user in obj.users.all()])
    get_users.short_description = "Users"


@admin.register(PriceModel)
class PriceAdmin(admin.ModelAdmin):
    list_display = ("product", "price", "old_price", "discount", "date", "get_person_username")
    search_fields = ("product__product_name", "person__user__username")
    list_filter = ("person", "date",)
    ordering = ("-date",)

    def get_person_username(self, obj):
        return obj.person.user.username if obj.person else "-"
    get_person_username.short_description = "Added By"






#admin2025 passwordadmin
