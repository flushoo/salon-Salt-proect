from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.views.decorators.http import require_POST
from .models import Booking, Service, Barber, Product
from .forms import BookingForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import random
import json
from django.core.cache import cache
from .models import Cart, CartItem, Product
import stripe
from django.conf import settings

@login_required
def booking_list(request):
    """Отображает список записей пользователя"""
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'user_profile.html', {'bookings': bookings})

def services(request):
    """Выводит список всех доступных услуг"""
    services_data = Service.objects.all()
    return render(request, 'services.html', {"services": services_data})

def booking_success(request):
    """Страница успешного бронирования"""
    return render(request, "booking_success.html")

def get_services(request):
    """Возвращает список услуг в формате JSON"""
    services = list(Service.objects.values("id", "name", "price"))
    return JsonResponse({"services": services})


@login_required
def create_booking(request):
    """Создание записи через модальное окно"""
    if request.method == 'POST':
        service_id = request.POST.get('service')
        barber_id = request.POST.get('barber')
        date = request.POST.get('date')
        time = request.POST.get('time')
        client_name = request.POST.get('client_name')
        client_email = request.POST.get('client_email')

        # Проверяем существование услуги
        service = get_object_or_404(Service, id=service_id)

        # Проверяем существование барбера
        barber = get_object_or_404(Barber, id=barber_id)

        # Создаём запись
        booking = Booking.objects.create(
            user=request.user,
            service=service,
            barber=barber,
            date=date,
            time=time,
            client_name=client_name,
            client_email=client_email,
            status='pending'
        )

        return JsonResponse({"message": "Запись успешно создана", "booking_id": booking.id}, status=200)

    services = Service.objects.all()
    barbers = Barber.objects.all()
    return render(request, 'booking.html', {'services': services, 'barbers': barbers})


@login_required
def confirm_booking(request, booking_id):
    """Подтверждение записи"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        booking.status = 'confirmed'
        booking.save()
        return redirect('user_profile')

    return render(request, 'booking.html', {'booking': booking})


def booking_view(request):
    """Просмотр и создание новой записи"""
    services = Service.objects.all()
    barbers = Barber.objects.all()  # ✅ Добавляем барберов

    if request.method == 'POST':
        form = BookingForm(request.POST, request=request)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('user_profile')

    else:
        form = BookingForm(request=request)

    return render(request, 'booking.html', {'form': form, 'services': services, 'barbers': barbers})


@login_required
@require_POST
def cancel_booking(request, booking_id):
    """Отмена записи"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, "Запись успешно отменена.")  # Сообщение для пользователя
    return redirect("user_profile")  # Перенаправляем обратно в личный кабинет


@login_required
@require_POST
def update_booking_status(request):
    """Обновление статуса бронирования через модальное окно"""
    booking_id = request.POST.get("booking_id")
    new_status = request.POST.get("status")

    if not booking_id or not new_status:
        return JsonResponse({"success": False, "error": "Некорректные данные"}, status=400)

    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.status = new_status
    booking.save()

    return JsonResponse({"success": True, "new_status": booking.status})


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_profile')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    """Авторизация пользователя"""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect('login')


@login_required
def user_profile(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_profile.html', {'bookings': bookings})


def home(request):
    """Главная страница"""
    return render(request, 'home.html')


def salt_store(request):
    """Отображение страницы Salt Store с товарами"""
    products = Product.objects.all()
    return render(request, 'salt_store.html', {'products': products})


@login_required
def edit_booking(request, booking_id):
    """Редактирование записи"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking, request=request)  # ✅ Передаём request в форму
        if form.is_valid():
            form.save()
            messages.success(request, "Запись успешно обновлена!")
            return redirect('user_profile')  # 🔹 Переход в личный кабинет после сохранения
        else:
            print("Ошибки формы:", form.errors)  # 🔹 Вывод ошибок в консоль для отладки
            messages.error(request, "Ошибка при обновлении записи. Проверьте данные.")
    else:
        form = BookingForm(instance=booking, request=request)  # ✅ Передаём request

    return render(request, 'edit_booking.html', {'form': form, 'booking': booking})


@login_required
def get_barbers(request):
    """Получение списка барберов для выбранной услуги"""
    service_id = request.GET.get('service_id')
    barbers = Barber.objects.filter(services__id=service_id).values('id', 'name')
    return JsonResponse({"barbers": list(barbers)})


@csrf_exempt
@login_required
@require_POST
def send_sms_code(request):
    """Отправляет код подтверждения на телефон"""
    data = json.loads(request.body)
    phone = data.get("phone")
    booking_id = data.get("booking_id")

    if not phone or not phone.startswith("+375") or not phone[1:].isdigit():
        return JsonResponse({"success": False, "message": "Некорректный номер"}, status=400)

    # Генерируем случайный 6-значный код
    code = random.randint(100000, 999999)
    
    # Сохраняем код в кэше на 5 минут
    cache.set(f"sms_code_{phone}", code, timeout=300)

    try:
        # Сохраняем телефон в записи, если номер изменился
        booking = Booking.objects.get(id=booking_id, user=request.user)
        if booking.client_phone != phone:
            booking.client_phone = phone
            booking.save()

        print(f"Отправленный код для {phone}: {code}")  # Для отладки

        return JsonResponse({"success": True, "message": "Код отправлен!"})
    except Booking.DoesNotExist:
        return JsonResponse({"success": False, "message": "Запись не найдена!"}, status=404)


@csrf_exempt
@login_required
@require_POST
def verify_sms_code(request):
    """Подтверждение записи по SMS-коду"""
    data = json.loads(request.body)
    booking_id = data.get("booking_id")
    code = data.get("code")

    if not code or not code.isdigit():
        return JsonResponse({"success": False, "message": "Некорректный код!"}, status=400)

    try:
        # Получаем запись
        booking = Booking.objects.get(id=booking_id, user=request.user)
        phone = booking.client_phone  # Берём номер из базы

        if not phone:
            return JsonResponse({"success": False, "message": "Ошибка: у записи нет номера!"}, status=400)

        # Получаем сохранённый код из кэша
        stored_code = cache.get(f"sms_code_{phone}")

        if stored_code and str(stored_code) == code:
            # Если код совпадает — подтверждаем запись
            booking.status = "confirmed"
            booking.save()

            # Удаляем использованный код из кэша
            cache.delete(f"sms_code_{phone}")

            return JsonResponse({"success": True, "message": "Запись подтверждена!"})
        else:
            return JsonResponse({"success": False, "message": "Неверный код!"}, status=400)

    except Booking.DoesNotExist:
        return JsonResponse({"success": False, "message": "Запись не найдена!"}, status=404)
    
    
    
@login_required
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)  # Пытаемся найти продукт по ID
    except Product.DoesNotExist:
        messages.error(request, "Этот продукт не существует!")
        return redirect('salt_store')

    # Получаем или создаем корзину для текущего пользователя
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Проверяем, есть ли уже этот товар в корзине
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    # Увеличиваем количество товара в корзине
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Перенаправляем на страницу Salt Store
    messages.success(request, f"Товар '{product.name}' добавлен в корзину!")
    return redirect('salt_store')




@login_required
def view_cart(request):
    # Получаем или создаем корзину для пользователя
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Получаем все товары в корзине
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Если корзина пуста
    if not cart_items:
        return render(request, 'cart.html', {
            'cart_items': [],
            'total': 0
        })
    
    # Рассчитываем общую стоимость товаров в корзине
    total = sum(item.total_price() for item in cart_items)
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })
    
    
    
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    # Удаляем товар из корзины
    cart_item.delete()
    
    return redirect('view_cart')
    
    
    

# Устанавливаем ключи Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.total_price() for item in cart_items)

    # Создание сессии для оплаты с помощью Stripe
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'rub',
                    'product_data': {
                        'name': item.product.name,
                    },
                    'unit_amount': int(item.total_price() * 100),  # Сумма в копейках
                },
                'quantity': item.quantity,
            }
            for item in cart_items
        ],
        mode='payment',
        success_url=request.build_absolute_uri('/payment-success/'),
        cancel_url=request.build_absolute_uri('/payment-cancel/'),
    )

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'session_id': session.id,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })
    
    
    
    
