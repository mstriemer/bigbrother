import os
import sys

path = '/var/apps/bigbrother/releases/current'
if path not in sys.path:
    sys.path.append(path)

path = '/var/apps/bigbrother/releases/current/bigbrother'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'bigbrother.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

