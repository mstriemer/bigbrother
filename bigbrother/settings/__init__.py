from base import *
try:
    from local import *
except ImportError:
    print("You may define local settings in `settings/local.py`")
