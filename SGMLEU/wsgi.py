"""
WSGI config for SGMLEU project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

import site

site.addsitedir("C:/Python27/Lib/site-packages")

sys.path.append("C:/Apache2.2/htdocs/SGMLEU/SGMLEU")
sys.path.append("C:/Apache2.2/htdocs/SGMLEU")

#os.environ.setdefault ["DJANGO_SETTINGS_MODULE"]= "SGMLEU.settings"
os.environ["DJANGO_SETTINGS_MODULE"] = "SGMLEU.settings"

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()

application = get_wsgi_application()
