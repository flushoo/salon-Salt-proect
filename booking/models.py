from django.contrib.auth.models import User
from django.db import models


class Barber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    services = models.ManyToManyField('Service', related_name='barbers', blank=True)  # Связь барбера с услугами

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    duration = models.IntegerField(help_text="Продолжительность в минутах")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Изображение")

    def __str__(self):
        return f"{self.name} - {self.price} руб."

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждена'),
        ('canceled', 'Отменена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=13, blank=True, null=True)  # Добавлено
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Запись {self.client_name} на {self.service.name} у {self.barber.user.get_full_name()} ({self.get_status_display()})"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')  # Путь для хранения изображений
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
    
from django.db import models
from django.conf import settings
from .models import Product

# Корзина покупок
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина {self.user.username}"

# Товары в корзине
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
    def total_price(self):
        return self.product.price * self.quantity
    
    
