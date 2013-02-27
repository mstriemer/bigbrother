from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class ForceSSLMiddleware(object):
    """Force all requests to use HTTPS unless ``settings.DEBUG`` is True.
    """
    def process_request(self, request):
        if not (settings.DEBUG or request.is_secure()):
            url = request.build_absolute_uri(request.get_full_path())
            secure_url = url.replace('http://', 'https://')
            return HttpResponsePermanentRedirect(secure_url)
