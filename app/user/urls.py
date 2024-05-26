"""
URL mappings for the user API.
"""
from django.urls import path

from user import views

# this app name is going to be used for the reverse mapping that we defined in our test for user api
app_name = 'user'

# Defines url paterns. So any request that gets passed to the url pattern will get handled by
# the appropriate view mentioned below.
# Django expcts a function for the view parameter and so we use the as_view to get that view fucntion.
# The name is used again in the reverse lookup.
# The url pattern is lined to a view which is lined to a serializer which is linked to a model.
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
