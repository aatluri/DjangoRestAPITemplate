"""
URL mappings for the recipe app.
"""


# these are used to define a path and also to include URLs by the URL names.
from django.urls import (
    path,
    include,
)

# So this is the default router that provided by the Django rest framework.
# And you can use this with an API view to automatically create routes for all of the different options
# available for that view.

from rest_framework.routers import DefaultRouter

from diagnostictest import views

# So what we do is we create a default router and then we register our view set with that router with
# the name diagnostictests.
# So what that will do is it will create a new endpoint API /diagnostictests.
# and it will assign all of the different endpoints from our DiagnostocTest view set to that endpoint.
# Basically what it means is that the diagnostictest view set is going to have auto generated URLs depending on
# the functionality that's enabled on the view set.
# Because we're using the model view set, it's going to support all the available methods for create,
# read, update and delete those i.e http get post, put patch and delete.
# It will create and register endpoints for each of those options.
router = DefaultRouter()
router.register('diagnostictests', views.DiagnosticTestViewSet)
router.register('tags', views.TagViewSet)

# Then we define the name which is used to identify the name when we're doing the reverse lookup of URLs.
app_name = 'diagnostictest'

# And then here in the URL patterns, we're using the include function to include the URLs that are generated
# automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
