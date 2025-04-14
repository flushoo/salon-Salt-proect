from django.contrib import admin
from django.utils.html import format_html
from .models import Booking, Product, Service, Barber, Cart, CartItem

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'price', 'image_preview')  # Добавляем превью изображения
    search_fields = ('name',)
    list_filter = ('price',)
    fields = ('name', 'duration', 'price', 'image', 'image_preview')  # Поля в админке
    readonly_fields = ('image_preview',)  # Поле превью только для просмотра

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 5px; object-fit: cover;" />', obj.image.url)
        return "(Нет изображения)"
    image_preview.short_description = "Превью изображения"

@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username',)
    list_filter = ('bio',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'service', 'date', 'time', 'barber', 'user')
    search_fields = ('client_name', 'client_email', 'service__name', 'barber__user__username')
    list_filter = ('date', 'service', 'barber')
    ordering = ('-date',)

# Регистрация модели корзины
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)

# Регистрация модели товаров в корзине
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price')
    list_filter = ('cart', 'product')
    search_fields = ('product__name',)





