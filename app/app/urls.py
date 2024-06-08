"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# This is the entry point for the project. Contains the root URL configuration of the entire project

# Import DRF specific Modules
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
# The include allows us to include urls from a different app.
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Adds a url to our project that will generate the schema for our api
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    # This will serve the swagger documentation that will use the above schema for our api documentation
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),
    # Connects the view we created in the user app to the main app.
    # The include allows us to include urls from a different app.
    path('api/user/', include('user.urls')),
    path('api/diagnostictest/', include('diagnostictest.urls')),
]
