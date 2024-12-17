from django.contrib import admin
from tinymce.widgets import TinyMCE
from .models import Page

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created')  # Campos a mostrar en la vista del admin
    search_fields = ('title', 'slug')  