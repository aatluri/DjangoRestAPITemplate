# Create your views here.
# We first create a serializer that uses our model. We then create a view that uses our serializer.
# We then create a url pattern which when accessed will use the View. So when a http call is made to
# the url pattern defined, it calls the view thats is defined which inturn calls the serialiser
# which in turn uses the model.
# URL -> View-> Serializer -> Model

"""
Views for the user API.
"""
# So, rest framework does a lot of the logic that we need for creating objects in the database for us.
# And it does that by providing a bunch of different base classes that we can configure for our views
# that will handle the request in a kind of default standardized way, while at the same time giving us
# the ability to override some of that behavior so we can modify it if we need.
# So what we're doing is we're using the generics module that's provided by the DJANGO framework

from rest_framework import generics, authentication, permissions
# Import existing view so that a lot of work is done for us and just override a few things.
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

# then we're importing our user sterilizer and authtokenserialiser that we just defined.
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

# we're creating a view called create user view and we're basing it from the Create API view that is part of generics
# The Create API view handles a http post request that's designed for creating objects in the database
# We just need to define the serialization, which we've already done, and then set the serialize class on this view
# so that the Django rest framework knows what serializer to use.
# So when you make the http type request, it goes through to the URL and then it gets passed into this create
# user view clause, which will then call the sterilizer and create the object and return the appropriate response.


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


# So what we're doing here is we're using the obtain auth token view that's provided by general rest framework
# and we're customizing the serialize the to use the custom serialize that we created.
# And the reason we do this is because the obtain or token view uses the username and password instead
# of email and password. We want to customize this to be email and password in a serialized.
# So we override the behavior and we customize the serialized that's used with the default auth token view.
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
# What this does is it uses the default render of classes for this obtain or token view.
# So by default, if we want to include this, we wouldn't get the browser or API that's used for Django Rest framework.
# It wouldn't show the nice user interface for that.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# We are defining a new class called manage user view and we're basing it from
# generic.retrieve update API view
# retrieve update API view is provided by the Django Resource Framework to provide the functionality
# needed for retrieving and updating objects in the database.
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
# We use the same serialiser as our CreateUser view.
    serializer_class = UserSerializer
# Authentication is how we know the user who is who they say they are
# For authentication we use TokenAuthentication
    authentication_classes = [authentication.TokenAuthentication]
# Permission is what is the authenticated user allowed to do.
# In this case we want to make sure the user is authenticated. There are no other restriction
    permission_classes = [permissions.IsAuthenticated]

# Now we override the get object.
#  get object gets the objects basically for the http get request or any request that's made to this API.
# In this case, we're overriding this behavior and we're just retrieving the user that's attached to the request.
    def get_object(self):
        """Retrieve and return the authenticated user."""
# So the way the authentication system works is that when a user is authenticated, the user object that
# is being authenticated gets assigned to the request object that's available in the view.
# So we can use that to return the user object for the request made for this API.
        return self.request.user

# So when you make a hasty get request to this endpoint, it's going to call get objects to get the user,
# it's going to retrieve the user that was authenticated and then it's going to run it through our serialize
# is that we defined before returning the result to the API.
