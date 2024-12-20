from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from polymorphic.models import PolymorphicModel
from django.urls import reverse
from django.utils import timezone


# Modelo para la página
class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    content = RichTextUploadingField(blank=True, null=True)  # Opcional si se usan solo bloques
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    blocks = models.ManyToManyField('Block', through='PageBlock', related_name='pages')
    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name='Order')

    class Meta:
        ordering = ('my_order',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:page_detail', args=[self.slug])


# Relaciona los bloques con la página y su orden
class PageBlock(models.Model):
    page = models.ForeignKey(Page, related_name='page_blocks', on_delete=models.CASCADE)
    block = models.ForeignKey('Block', related_name='block_pages', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Page: {self.page.title}, Block: {self.block.name}"


# Bloques generales (PolymorphicModel para diferentes tipos)
class Block(PolymorphicModel):
    name = models.CharField(max_length=100, default="Block")
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def render(self):
        raise NotImplementedError("Subclasses must implement the render method.")


# Elementos dentro de un bloque
class BlockElement(models.Model):
    CONTENT_TYPES = [
        ('title', 'Title'),
        ('image', 'Image'),
        ('text', 'Text'),
        ('button', 'Button'),
    ]

    block = models.ForeignKey(Block, related_name="elements", on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    text = models.CharField(max_length=200, blank=True, null=True)
    rich_text = RichTextUploadingField(blank=True, null=True)
    image = models.ImageField(upload_to="blocks/images/", blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']


    def render(self):
        """Renderiza un bloque completo con todos los elementos contenidos"""
        if self.content_type == 'title':
            return f"<h2>{self.text}</h2>"
        elif self.content_type == 'image':
            return f"<img src='{self.image.url}' alt='{self.text}'>"
        elif self.content_type == 'text':
            return f"<p>{self.rich_text}</p>"
        elif self.content_type == 'button':
            return f"<a href='{self.link}' class='btn btn-primary'>{self.text}</a>"
        return ""


# Tipo de bloque específico con varios elementos
class ComplexBlock(Block):  
    def render(self):
        elements_html = ''.join([element.render() for element in self.elements.all()])
        return f"<div class='complex-block'>{elements_html}</div>"
    



class SliderBlock(Block):
    autoplay = models.BooleanField(default=True)
    loop = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def render(self):
        # Renderiza todas las imágenes de este slider
        images_html = ''.join([item.render() for item in self.slider_items.all()])
        return f"<div class='carousel' data-autoplay='{self.autoplay}' data-loop='{self.loop}'>" \
               f"{images_html}</div>"

class SliderItem(models.Model):
    slider = models.ForeignKey(SliderBlock, related_name='slider_items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blocks/slider/')
    caption = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.caption

    def render(self):
        return f"<div class='carousel-item'><img src='{self.image.url}' alt='{self.caption}' class='img-fluid'>" \
               f"<div class='carousel-caption'>{self.caption}</div></div>"

class QuoteBlock(Block):
    quote = models.TextField()
    author = models.CharField(max_length=100)

    def __str__(self):
        return f"Quote by {self.author}"

    def render(self):
        # Renderiza todas las citas de este bloque
        quotes_html = ''.join([item.render() for item in self.quote_items.all()])
        return f"<div class='quote-block'>{quotes_html}</div>"

class QuoteItem(models.Model):
    quote = models.ForeignKey(QuoteBlock, related_name='quote_items', on_delete=models.CASCADE)
    quote = models.TextField()
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.author

    def render(self):
        return f"<blockquote>{self.quote}<footer>{self.author}</footer></blockquote>"