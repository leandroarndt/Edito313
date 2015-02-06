"""
WSGI config for Edito 313 project. This file should be copied or hard linked
into the website's document root. The WSGI process should not have write
permissions on it.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os

# Isolates one user from another, if this has been configured. Requires POSIX system.
if not os.environ.get('SITEPATH', False):
    os.environ['SITEPATH'] = os.path.normpath(__file__)
os.chdir(os.environ.get('SITEPATH'))
try:
    os.chroot(os.environ['SITEPATH'])
    os.environ['SITEPATH'] = '/'
except AttributeError: # We're non-POSIX
    pass

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edito313.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
