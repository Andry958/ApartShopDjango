from django.contrib import admin
from .models import Apartment


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    """Адміністрування квартир"""
    
    list_display = ['id', 'title', 'apartment_type', 'price', 'square_meters', 
                    'floor', 'is_available', 'created_at']
    list_filter = ['is_available', 'apartment_type', 'created_at']
    search_fields = ['title', 'description', 'address']
    list_editable = ['is_available']
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'description', 'apartment_type')
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
        """Збереження моделі з додатковою логікою"""
        super().save_model(request, obj, form, change)
        
    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартири'
