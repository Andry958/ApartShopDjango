from django import forms
from django.core.exceptions import ValidationError
from .models import Apartment


class ApartmentForm(forms.ModelForm):
    """Форма для створення та редагування квартир з валідацією"""
    
    class Meta:
        model = Apartment
        fields = ['title', 'description', 'apartment_type', 'price', 
                  'square_meters', 'floor', 'address', 'is_available']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть назву квартири'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опис квартири',
                'rows': 4
            }),
            'apartment_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ціна в $',
                'step': '0.01'
            }),
            'square_meters': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Площа в м²',
                'step': '0.1'
            }),
            'floor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Поверх'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Повна адреса'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'title': 'Назва квартири',
            'description': 'Опис',
            'apartment_type': 'Тип квартири',
            'price': 'Ціна ($)',
            'square_meters': 'Площа (м²)',
            'floor': 'Поверх',
            'address': 'Адреса',
            'is_available': 'Доступна для продажу'
        }

    def clean_title(self):
        """Валідація назви - мінімум 5 символів"""
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError('Назва повинна містити мінімум 5 символів')
        return title

    def clean_price(self):
        """Валідація ціни - повинна бути більше 0 та не більше 10 мільйонів"""
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError('Ціна повинна бути більше 0')
        if price > 10000000:
            raise ValidationError('Ціна не може перевищувати 10,000,000$')
        return price

    def clean_square_meters(self):
        """Валідація площі - від 10 до 1000 м²"""
        square_meters = self.cleaned_data.get('square_meters')
        if square_meters < 10:
            raise ValidationError('Площа повинна бути мінімум 10 м²')
        if square_meters > 1000:
            raise ValidationError('Площа не може перевищувати 1000 м²')
        return square_meters

    def clean_floor(self):
        """Валідація поверху - від 1 до 100"""
        floor = self.cleaned_data.get('floor')
        if floor < 1:
            raise ValidationError('Поверх повинен бути мінімум 1')
        if floor > 100:
            raise ValidationError('Поверх не може перевищувати 100')
        return floor

    def clean_address(self):
        """Валідація адреси - мінімум 10 символів"""
        address = self.cleaned_data.get('address')
        if len(address) < 10:
            raise ValidationError('Адреса повинна містити мінімум 10 символів')
        return address

    def clean_description(self):
        """Валідація опису - мінімум 20 символів"""
        description = self.cleaned_data.get('description')
        if len(description) < 20:
            raise ValidationError('Опис повинен містити мінімум 20 символів')
        return description
