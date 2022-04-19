from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

admin.site.site_header="Doret E-Commerce Admin"
admin.site.site_title="Doret E-Commerce Admin"
admin.site.index_title="Doret E-Commerce Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('dj_rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
    
    path('', include('ecommerce.urls',namespace='ecom')),
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)