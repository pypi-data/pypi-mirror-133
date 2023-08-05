from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from .views import MaintenancePage

coming_soon_urlpatterns = [
    path("admin/", admin.site.urls),
    re_path("", TemplateView.as_view(template_name="coming-soon.html")),
]

maintenance_urlpatterns = [
    path("admin/", admin.site.urls),
    re_path("", MaintenancePage.as_view()),
]

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if getattr(settings, "MAINTENANCE_MODE", False):
    urlpatterns = maintenance_urlpatterns

if getattr(settings, "COMING_SOON_MODE", False):
    urlpatterns = coming_soon_urlpatterns

if "debug_toolbar" in settings.INSTALLED_APPS:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls", namespace="djdt"))]
