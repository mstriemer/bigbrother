from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic.simple import redirect_to

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', redirect_to, {'url': '/bigbrother/'}),
    (r'^bigbrother/', include('gameshow.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^accounts/password_change/$',
        'django.contrib.auth.views.password_change', {'post_change_redirect':
        '/bigbrother/'}),
)

if settings.SERVE_STATIC:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )

