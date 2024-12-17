
from django.contrib import admin
from django.urls import path, include
from home.views import home
from django.conf import settings
from django.conf.urls.static import static
from ckeditor_uploader import urls as ckeditor_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('ckeditor/', include(ckeditor_urls)),
    path('', home, name='home'),
    path('blog/', include('blog.urls'), name='blog'),
    path('page/', include('page.urls'), name='page'),
   
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
