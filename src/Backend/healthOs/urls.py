"""healthOs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.views.static import serve
from healthOs import settings
from django.conf.urls import include, url

admin.site.site_header = 'HealthOs Dashboard'
admin.site.site_title = 'HealthOs Dashboard'
admin.site.index_title = 'HealthOs'
urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),
    path('', admin.site.urls),
    path('auth/', include("user.urls")),
    path('dataplan/', include("dataplan.urls")),
    path('payments/', include("payments.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = [url(r'', include(urlpatterns))]
