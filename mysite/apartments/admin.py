from django.contrib import admin
from .models import Apartment, Booking


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'apartment_type', 'price', 'square_meters', 
                    'floor', 'is_available', 'created_at']
    list_filter = ['is_available', 'apartment_type', 'created_at']
    search_fields = ['title', 'description', 'address']
    list_editable = ['is_available']
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'description', 'apartment_type', 'image')
        }),
        ('Характеристики', {
            'fields': ('price', 'square_meters', 'floor', 'address')
        }),
        ('Статус', {
            'fields': ('is_available',)
        }),
        ('Дати', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартири'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'apartment', 'user', 'start_date', 'end_date', 
                    'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at', 'start_date']
    search_fields = ['apartment__title', 'user__username', 'user__email']
    list_editable = ['status']
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Інформація про бронювання', {
            'fields': ('apartment', 'user', 'status')
        }),
        ('Дати', {
            'fields': ('start_date', 'end_date', 'total_price')
        }),
        ('Додатково', {
            'fields': ('notes', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'total_price']
    
    def save_model(self, request, obj, form, change):
        if not change:
            days = (obj.end_date - obj.start_date).days
            obj.total_price = obj.apartment.price * days
        super().save_model(request, obj, form, change)
