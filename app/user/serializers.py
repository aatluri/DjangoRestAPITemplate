
"""
Serializers for the user API View.
"""
# We first create a serializer that uses our model. We then create a view that uses our serializer.
# We then create a url pattern which when accessed will use the View. So when a http call is made to
# the url pattern defined, it calls the view thats is defined which inturn calls the serialiser
# which in turn uses the model.
# URL -> View-> Serializer -> Model

# authenticate is a function that comes with Django that allows you to authenticate with the authentication system
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
# import translations
from django.utils.translation import gettext as _

# So serialize is simply just a way to convert objects to and from python objects.
# So it takes JSON input that might be posted from the API and validates the input to make sure that
# it is secure and correct as part of validation rules.
# And then it converts it to either a python object that we can use or a model in our actual database.

# imports the serializers module from rest framework
from rest_framework import serializers


# This is the class for our serializer
# Model Serializer allow us to automatically validate and save things to a
# specific model that we define in our serialization.
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""


# Then we define a class Meta
# So this is where we tell the Django rest framework, the model and the fields and any additional arguments
# that we want to pass to the serializer
# the serializer needs to know which model it's representing
# So this serialize is going to be for our user model.
# Then we define the acutal fields that will be in the request that should be saved in the model.
# We do not include fields like isactive or isstaff as those we want to set by the admins and not the user.
# The we define the extra keyword args
# And that is a dictionary that allows us to provide extra metadata to the different fields.
# eg: do we want the field to be write only or read only? Or do we want that to be a minimum length on the value?
# Here we say tht the passwors is a write only and cannot be read. And it has to have a length of atleast 5.
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

# The Create method allows us to override the behavior that the serialize it does when you create new
# objects out of that serialize.
# So the default behavior is just to create an object with whatever values are passed in verbatim.
# So if you pass in the password, then the default behavior, the model sterilizer will be just to save
# that password as clear text in the model.
# Now we don't want that to happen because we want it to pass through the encryption.
# So ideally we want it to use the create user method that we provided on our model manager for creating users
# Call the get user model and pass in the already validated user data.
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

# We are overriding the update method on our UserSerializer
# The update method is called whenever we call the update action on the model a serializer represents.
# self is common for all these methods, instance is the model instance being updated
# validated_data is the data that has passed through the serialize validation.
# In our case its the name, email address and password.
# We retrieve the password from the validated_data dictionary by popping it, i.e it gets removed after
# We default to None as its possible the user might be updating something else other than password.
# So what this does is it calls the update method on the model serialize a base clause.
# So that's the one that's provided by the model serialize.
# And this is going to perform all of the steps for updating the object.
# So what we're doing is we're leveraging the existing logic from the model serialize and we're only overwriting
# and changing what we need to change.
# since we removed the password from the dictionary, the above line will not update the password.
# if password has a value, then we update the user object password.
# Then return the user.
    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


# So what we've done here is we've defined a sterilizer with two fields.
# The first is the email field that will use to authenticate with, and that is just the email address of the user.
# And the second is the password field.
# So the password field is a character field and we've entered this style input type password here because
# when we are using the browser or API, we want the inputs to be a password So that the text is hidden
# Then you have trim whitespace equals false.
# django rest framework by default will trim the whitespace off the input for the character field.
# And we don't want this to happen with the password field because it's very plausible that the user might
# have a space at the end of their password, and they may have done that deliberately.
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

# validate method is called on the serializer at the validation stage when it goes
# to validate the input to the serialize i.e this is when the user is loggin in.
# So when the data is posted to the view, it's going to pass it to the sterilizer and then it's going
# to call validate to validate that the data is correct.
# gets the email address and password that was passed to the endpoint
# The authenitcate function accepts 3 arguments.
# The request context which contains the head of the message data.
# We then pass in the email as the username as we are using emailaddress as username.
# And then we pass in the password.
# So this checks if the passed in username and password are correct, If yes it returns the user.
# if not it returns an empty object.
# If it is empty then we raise an error.
# we set the user attribute, which is the attributes that we're validating for the sterilizer.
# So then we can use this user in the view this is what the view is going to expect to be set when the
# authentication was successful.
# Then we return the attributes from our validate method.
    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
