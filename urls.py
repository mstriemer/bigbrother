from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib import databrowse
from django.conf import settings
from django.views.generic.simple import redirect_to

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', redirect_to, {'url': '/bigbrother/'}),
    (r'^bigbrother/', include('bigbrother.gameshow.urls')),
    (r'^databrowse/(.*)', databrowse.site.root),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^accounts/password_change/$',
        'django.contrib.auth.views.password_change', {'post_change_redirect':
        '/bigbrother/'}),
)
