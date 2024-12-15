from django.contrib import admin
from .models import Product
from django.utils.html import format_html

# Register your models here

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name', 'price')
    list_filter = ('name', 'price')
    list_per_page = 10
    list_editable = ('price',)
    
    
        # Método para mostrar una vista previa de la imagen
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"  # Etiqueta para la columna