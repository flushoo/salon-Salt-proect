from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from .models import Booking, Service, Product, Barber

class BookingForm(forms.ModelForm):
    """Форма для бронирования услуг"""
    
    class Meta:
        model = Booking
        fields = ['service', 'date', 'time', 'client_name', 'client_email', 'barber']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'client_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'barber': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        """Добавляем request при инициализации"""
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

def clean(self):
    """Проверка на уникальность записи для пользователя"""
    cleaned_data = super().clean()
    date = cleaned_data.get('date')
    time = cleaned_data.get('time')

    user = getattr(self.instance, 'user', None) or getattr(self.request, 'user', None)
    
    if not user or not user.is_authenticated:
        raise ValidationError("Пользователь не найден или не аутентифицирован.")

    if self.instance and self.instance.pk:
        # ✅ Исключаем текущую запись при проверке уникальности
        existing_booking = Booking.objects.filter(user=user, date=date, time=time).exclude(pk=self.instance.pk)
    else:
        existing_booking = Booking.objects.filter(user=user, date=date, time=time)

    if existing_booking.exists():
        raise ValidationError("У вас уже есть запись на это время.")

    return cleaned_data

class ServiceForm(forms.ModelForm):
    """Форма для услуг"""
    
    class Meta:
        model = Service
        fields = ['name', 'duration', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ProductForm(forms.ModelForm):
    """Форма для товаров"""

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }