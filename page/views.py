from django.shortcuts import render, get_object_or_404
from .models import Page

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)

    blocks = page.blocks.order_by('order')  
    rendered_blocks = [block.render() for block in blocks]  

    return render(request, 'page/page_detail.html', {
        'page': page, 
        'blocks': rendered_blocks
    })