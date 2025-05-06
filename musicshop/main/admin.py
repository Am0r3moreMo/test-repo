from django.contrib import admin
from django.db import models
from typing import Iterable
from .models import Product, Order, PickUpPoint, User, Cart, CartItem
from django.utils.html import format_html


def editable_filter(fields: Iterable[models.Field]) -> list[str]:
    return [field.name for field in fields if field.name not in ("created_at", "id")]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = [field.name for field in Product._meta.local_fields]
    # list_editable = editable_filter(Product._meta.local_fields)
    list_filter = ("color", "manufacturer")
    search_fields = ("name", "description", "manufacturer")
    list_per_page = 50

    # Для красивого отображения JSONField
    # readonly_fields = ("display_characteristics",)

    # def display_characteristics(self, instance):
    #     if instance.characteristics:
    #         import json
    #         from django.utils.html import format_html

    #         return format_html(
    #             "<pre>{}</pre>", json.dumps(instance.characteristics, indent=2)
    #         )
    #     return "-"

    # display_characteristics.short_description = "Characteristics"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Order._meta.get_fields()
        if field.name not in ("user", "pickup_point", "items")
    ]
    list_editable = ("status",)
    list_per_page = 50


@admin.register(PickUpPoint)
class PickUpPointAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PickUpPoint._meta.local_fields]
    list_editable = ("name", "address")
    list_per_page = 50


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.local_fields]


# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Cart._meta.local_fields]

# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in CartItem._meta.local_fields]


class CartItemInline(admin.TabularInline):  # или admin.StackedInline для другого вида
    model = CartItem
    extra = 0  # не показывать дополнительные пустые формы
    readonly_fields = ["product_link", "total_price"]
    fields = ["product_link", "quantity", "total_price"]

    def product_link(self, obj):
        url = f"/admin/app_name/product/{obj.product.id}/"
        return format_html('<a href="{}">{}</a>', url, obj.product.name)

    product_link.short_description = "Товар"

    def total_price(self, obj):
        return f"{obj.total_price()} ₽"

    total_price.short_description = "Сумма"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    list_display = ["user", "created_at", "total_cart_price", "items_count"]
    inlines = [CartItemInline]
    readonly_fields = ["total_cart_price"]

    def total_cart_price(self, obj):
        return f"{obj.total_price()} ₽"

    total_cart_price.short_description = "Общая сумма корзины"

    def items_count(self, obj):
        return obj.items.count()

    items_count.short_description = "Товаров в корзине"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart", "product", "quantity", "total_price_display"]
    list_filter = ["cart__user", "product"]
    search_fields = ["product__name", "cart__user__username"]

    def total_price_display(self, obj):
        return f"{obj.total_price()} ₽"

    total_price_display.short_description = "Сумма"
