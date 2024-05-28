

# Create your views here.
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    DiagnosticTest,
    Tag,
)
from diagnostictest import serializers


# First we tell it what serializer to use
# query set represents the objects that are available for this View
# So because it's a model view set is expected to work with a model.
# And the way that you tell it, which models you use is you specify the query set here.
# So we say this is the query set of objects that is going to be manageable through this API or through
# the APIs that are available through our model view.
# Then we specify that in order to use any of the endpoints that provided
# by this feature, you need to use token authentication,
# which is the token authentication system that I showed you previously. And then you need to be authenticated.
class DiagnosticTestViewSet(viewsets.ModelViewSet):
    """View for manage DiagnosticTest APIs."""
    serializer_class = serializers.DiagnosticTestDetailSerializer
    queryset = DiagnosticTest.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# we want to make sure that those recipes are filtered down to the authenticated user.
# And the way that we do that is we override the get query method.
# query set is used to get our objects. Normally it would return all the objects
# But what we're doing here is we're adding an additional filter to filter by the user that is assigned to the request.
# And because we have token authentication and is authenticated as a permission, cos this means all users
# that use this API must be authenticated.
# So because we know that they're going to be authenticated, we can retrieve the user objects from the
# request that's passed in by the authentication system.
# This lets us filter all of the recipes to just those for the specific user that is authenticated.
    def get_queryset(self):
        """Retrieve diagnostic tests for authenticated user."""
        queryset = self.queryset
        return queryset.filter(user=self.request.user).order_by('-id').distinct()

# We want to be able to use a specific serializer based on the endpoint that is called.
# The way that we do that is we override the method called get serialize class method.
# Above we set the serializer_class to use the DetailSerializer by default for all diagnostic test actions.
# But if action is listing, we want to use the DiagnosticTestSerializer. For all other actions it will
# return the serializer_class which we set to DiagnosticTestDetailSerializer
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.DiagnosticTestSerializer
        return self.serializer_class

# This method ensures we save the correct user to the diagnostictests.
# So this perform create method is the way that we override the behavior for when Django Restaurant work
# saves a model in a viewset
# So when we create a new diagnostictest through the create feature of the view, so we're going to call this
# method as part of that object creation.
# So we're going to call it accepts one parameter which is the serialization, and this should be the
# validated sterilizer.
# So we can expect the serialized data to already be validated by the view set before this method is called,
# and then this method is called, and we can just simply do serialize autosave and we can set user equal
# self to request or user, which will set the user value to the current authenticated user when we save
# the object.
    def perform_create(self, serializer):
        """Create a new Diagnostic Test."""
        serializer.save(user=self.request.user)


# The url methods that show up in the doc or that are allowed is based on the methods mentioned in Mixin
class TagViewSet(viewsets.ModelViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# This method is used when we want list all the tags and ensures
# that only the tags created by the current user are displayed
    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

# This method is called during the tag creation and ensures that the current user is also saved along with the tag.
    def perform_create(self, serializer):
        """Create a new Tag."""
        serializer.save(user=self.request.user)
