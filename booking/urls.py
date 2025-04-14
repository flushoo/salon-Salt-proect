from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (
    booking_list, cancel_booking, services, get_services,
    booking_success, booking_view, user_profile, register,
    user_login, user_logout, home, salt_store, confirm_booking,
    edit_booking, create_booking, get_barbers,
    add_to_cart, view_cart, checkout  # Добавляем view для корзины и оформления
)

urlpatterns = [
    # Бронирование
    path('bookings/', booking_list, name='booking_list'),
    path('cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('confirm_booking/<int:booking_id>/', confirm_booking, name='confirm_booking'),
    path('booking/', booking_view, name='booking'),
    path('booking/success/', booking_success, name='booking_success'),
    path('create_booking/', create_booking, name='create_booking'),
    path('edit_booking/<int:booking_id>/', edit_booking, name='edit_booking'),

    # Услуги
    path('services/', services, name='services'),
    path('get-services/', get_services, name='get_services'),  

    # Личный кабинет
    path('profile/', user_profile, name='user_profile'),

    # SMS Подтверждение
    path('send_sms_code/', views.send_sms_code, name='send_sms_code'),
    path('verify_sms_code/', views.verify_sms_code, name='verify_sms_code'),

    # Пользователи
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # Корзина
    path('cart/', view_cart, name='view_cart'),  # Отображение корзины
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),  # Добавление товара в корзину
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Удаление товара из корзины

    # Оформление заказа
    path('checkout/', checkout, name='checkout'),  # Оформление заказа

    # Дополнительно
    path('salt-store/', salt_store, name='salt_store'),  # Страница магазина
    path('get_barbers/', get_barbers, name='get_barbers'),  # Получение списка барберов

    # Главная страница
    path('', home, name='home'),
]

# Добавляем обработку медиафайлов и статики в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    


