from django.contrib import admin
from .models import Page, PageBlock, Block, BlockElement, ComplexBlock, SliderBlock, SliderItem, QuoteBlock, QuoteItem
from adminsortable2.admin import SortableAdminMixin
class BlockElementInline(admin.TabularInline):
    model = BlockElement
    extra = 1
    fields = ('content_type', 'text', 'rich_text', 'image', 'link', 'order')
    ordering = ('order',)


@admin.register(Block)
class BlockAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'created', 'updated', 'order')
    search_fields = ('name',)
    inlines = [BlockElementInline]


@admin.register(ComplexBlock)
class ComplexBlockAdmin(BlockAdmin):
    list_display = ('name', 'created', 'updated')
    inlines = [BlockElementInline]


class PageBlockInline(SortableAdminMixin, admin.TabularInline):
    model = PageBlock
    extra = 1
    fields = ('block', 'order')
    ordering = ('order',)
    
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created', 'updated')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PageBlockInline]


class SliderItemInline(admin.TabularInline):
    model = SliderItem
    extra = 1
    fields = ('image', 'caption', 'order')

@admin.register(SliderBlock)
class SliderBlockAdmin(BlockAdmin):
    inlines = [SliderItemInline]


class QuoteItemInline(SortableAdminMixin, admin.TabularInline):
    model = QuoteItem
    extra = 1
    fields = ('quote', 'order')
    ordering = ('order',)
@admin.register(QuoteBlock)
class QuoteBlockAdmin(BlockAdmin):
    list_display = ('name', 'quote', 'author', 'created', 'updated')
    search_fields = ('quote', 'author')