from django import forms
from django.core.exceptions import ValidationError
from .models import Apartment, Booking
from datetime import date


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['title', 'description', 'apartment_type', 'price', 
                  'square_meters', 'floor', 'address', 'image', 'is_available']
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
            'image': forms.FileInput(attrs={
                'class': 'form-control'
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
            'image': 'Фото квартири',
            'is_available': 'Доступна для продажу'
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError('Назва повинна містити мінімум 5 символів')
        return title

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError('Ціна повинна бути більше 0')
        if price > 10000000:
            raise ValidationError('Ціна не може перевищувати 10,000,000$')
        return price

    def clean_square_meters(self):
        square_meters = self.cleaned_data.get('square_meters')
        if square_meters < 10:
            raise ValidationError('Площа повинна бути мінімум 10 м²')
        if square_meters > 1000:
            raise ValidationError('Площа не може перевищувати 1000 м²')
        return square_meters

    def clean_floor(self):
        floor = self.cleaned_data.get('floor')
        if floor < 1:
            raise ValidationError('Поверх повинен бути мінімум 1')
        if floor > 100:
            raise ValidationError('Поверх не може перевищувати 100')
        return floor

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if len(address) < 10:
            raise ValidationError('Адреса повинна містити мінімум 10 символів')
        return address

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 20:
            raise ValidationError('Опис повинен містити мінімум 20 символів')
        return description


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Додаткові побажання або коментарі',
                'rows': 3
            })
        }
        labels = {
            'start_date': 'Дата початку',
            'end_date': 'Дата закінчення',
            'notes': 'Примітки'
        }

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < date.today():
            raise ValidationError('Дата початку не може бути в минулому')
        return start_date

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date <= start_date:
                raise ValidationError('Дата закінчення повинна бути пізніше дати початку')
            
            days = (end_date - start_date).days
            if days < 1:
                raise ValidationError('Мінімальний термін бронювання - 1 день')

        return cleaned_data
