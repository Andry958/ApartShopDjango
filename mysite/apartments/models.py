from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_positive(value):
    if value <= 0:
        raise ValidationError('Значення повинно бути більше 0')


class Apartment(models.Model):
    TYPE_CHOICES = [
        ('ST', 'Studio'),
        ('1B', '1 Bedroom'),
        ('2B', '2 Bedrooms'),
        ('3B', '3 Bedrooms'),
        ('PH', 'Penthouse'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name='Назва',
        help_text='Назва/заголовок квартири'
    )
    description = models.TextField(
        verbose_name='Опис',
        help_text='Детальний опис квартири'
    )
    apartment_type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        verbose_name='Тип квартири'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(10000000)],
        verbose_name='Ціна ($)',
        help_text='Ціна в доларах'
    )
    square_meters = models.FloatField(
        validators=[MinValueValidator(10), MaxValueValidator(1000)],
        verbose_name='Площа (м²)',
        help_text='Площа квартири в квадратних метрах'
    )
    floor = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Поверх',
        help_text='Поверх будинку'
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Адреса',
        help_text='Повна адреса квартири'
    )
    image = models.ImageField(
        upload_to='apartments/',
        verbose_name='Фото',
        help_text='Фото квартири',
        blank=True,
        null=True
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='Доступна',
        help_text='Чи вільна квартира для продажу'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата створення'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата оновлення'
    )

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартири'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.price}$"

    def get_type_display_ua(self):
        type_dict = {
            'ST': 'Студія',
            '1B': '1-кімнатна',
            '2B': '2-кімнатна',
            '3B': '3-кімнатна',
            'PH': 'Пентхаус',
        }
        return type_dict.get(self.apartment_type, self.get_apartment_type_display())


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує підтвердження'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Скасовано'),
        ('completed', 'Завершено'),
    ]

    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Квартира'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Користувач'
    )
    start_date = models.DateField(
        verbose_name='Дата початку'
    )
    end_date = models.DateField(
        verbose_name='Дата закінчення'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Загальна ціна'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата створення'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Примітки'
    )

    class Meta:
        verbose_name = 'Бронювання'
        verbose_name_plural = 'Бронювання'
        ordering = ['-created_at']

    def __str__(self):
        return f"Бронювання {self.apartment.title} - {self.user.username}"

    def calculate_days(self):
        return (self.end_date - self.start_date).days
