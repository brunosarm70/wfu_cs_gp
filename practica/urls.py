from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login
from django.conf import settings
from django.conf.urls.static import static

from django.shortcuts import redirect


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    #url(r'^accounts/login/$', anonymous_required(login)),
    url(r'', include('gp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
