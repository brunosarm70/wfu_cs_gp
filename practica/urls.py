from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login
from django.conf import settings

from django.shortcuts import redirect

def anonymous_required(func):
    def as_view(request, *args, **kwargs):
        redirect_to = kwargs.get('next', settings.LOGIN_REDIRECT_URL )
        if request.user.is_authenticated():
            return redirect(redirect_to)
        response = func(request, *args, **kwargs)
        return response
    return as_view

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    #url(r'^accounts/login/$', anonymous_required(login)),
    url(r'', include('gp.urls')),
]
