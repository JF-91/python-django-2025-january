from django.shortcuts import render

# Create your views here.

def home(request):
    title = 'Home'
    subtitle = 'Welcome to the home page'
    context = {
        'title': title,
        'subtitle': subtitle
    }
    return render(request, 'home/index.html', context)