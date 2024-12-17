from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

class Page (models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        
        
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:page_detail', args=[self.slug])