"""
WSGI config for bot474 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

#import os

#from django.core.wsgi import get_wsgi_application

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot474.settings')

#application = get_wsgi_application()
# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys
#
## assuming your django settings file is at '/home/VladKuzmin/mysite/mysite/settings.py'
## and your manage.py is is at '/home/VladKuzmin/mysite/manage.py'
path = '/home/VladKuzmin/mysite'
if path not in sys.path:
    sys.path.append(path)
#
os.environ['DJANGO_SETTINGS_MODULE'] = 'bot474.settings'
#
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()