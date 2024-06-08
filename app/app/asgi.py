"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""
# This is mainly used for deployment if you are deploying via ASGI.
# Django supports deploying on ASGI(Asynchronous Server Gateway Interface)
# Django’s startproject management command sets up a default ASGI configuration for you,
# which you can tweak as needed for your project, and direct any ASGI-compliant application server to use.
# It is used as an interface between application server to
# connect with django or any python framework which implements ASGI


import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_asgi_application()
