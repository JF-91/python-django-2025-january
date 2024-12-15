
from django.contrib import admin
from django.urls import path, include
from home.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', home, name='home'),

    path('blog/', include('blog.urls'), name='blog'),
   
]
