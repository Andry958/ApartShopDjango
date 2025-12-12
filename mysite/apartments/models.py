from django.db import models

class Apartment(models.Model):
    TYPE_CHOICES = [
        ('ST', 'Studio'),
        ('1B', '1 Bedroom'),
        ('2B', '2 Bedrooms'),
        ('3B', '3 Bedrooms'),
        ('PH', 'Penthouse'),
    ]

    title = models.CharField(max_length=200)  # Назва/заголовок квартири
    description = models.TextField()  # Опис
    apartment_type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Ціна
    square_meters = models.FloatField()  # Площа
    floor = models.IntegerField()  # Поверх
    address = models.CharField(max_length=255)  # Адреса
    is_available = models.BooleanField(default=True)  # Чи вільна квартира
    created_at = models.DateTimeField(auto_now_add=True)  # Дата додавання
    updated_at = models.DateTimeField(auto_now=True)  # Дата оновлення

    def __str__(self):
        return f"{self.title} - {self.price}$"
