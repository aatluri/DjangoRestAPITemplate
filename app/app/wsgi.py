"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

# Django supports deploying on WSGI(Web Server Gateway Interface).
# Django’s startproject management command sets up a default WSGI configuration for you,
# which you can tweak as needed for your project, and direct any WSGI-compliant application server to use.
# It is used as an interface between application server to
# connect with django or any python framework which implements wsgi


import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_wsgi_application()
