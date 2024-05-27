# Create your models here.
"""
Database models.
"""
# import uuid
# import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# Define a user manager based on the BaseUserManager Class
class UserManager(BaseUserManager):
    """Manager for users."""

# Define create_user method.
# We pass email and password for a user.
# The extra fields means that we can provide keyword arguments
# any number of keyword arguments that will be passed into our model
# verifies that if an email is not provided, it raises an error.
# The self.model is the same as defining a user using the User class we defined below.
# We pass in the email and any extra fields that were passed in. We normalise the email as well.
# Takes the passin password and encrypts it using a hashing process
# So when you look in the database , you will not see the actual password.
# Save the user model. We use self._db so that in the event that we use multiple databases, we choose the db.

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

# Define create_user method.
# We pass email and password for a user.
# We call the create_user method and set the staff and superuser fields.
# We save using self._db. This is useful if we have multiple databases defined for Django.
    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# Defining a new class and we base from abstract base user on the permissions mixed in.
# And as I mentioned, abstract base user contains the functionality for the
# authentication system, but not any fields.
# And the permissions mixed in contains the functionality for the permissions
# feature of Django, and it also contains any fields that are needed for the permissions feature.
# Define the fields
# only staff users can log in to Django Admin. By defualt its set to False
# Assign the user manager created above to this custom model we created.
# username field here which defines the field that we want to use for authentication.
# And this is how we replace the username default field that comes with the default user model to our
# custom email field
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'


# Add a DiagnosticTest Class
# We are basing it off of just the basic Model class.
# This is different from the Users class as there were were extending the functionality of User
# we add the fields that will make up the DiagnosticTest model.
# The user that the recipe belongs to. We set up a foreign key relationship with the user model.
# And you can see that in the first argument that we're passing to the foreign key is the author user model.
# So this is the author user model that we define in our settings.py file.
# If we change the user model, we don't want to have to go through a bunch of hard coded references to
# that user model in order to change it all through our code base.
# So that's why the best practice is to reference it from the settings when you're referencing your user
# username or relationship to your user model.
# Then we have on Delete Cascade. And what that does is it says with this relationship,
# if the related object is deleted, we're also going to cascade that change to this model.
# Then we have the rest of the fiels.
# Finally we have the str method which returns the string rep of the object which in this case is the title.
# if we dont have the str method then when we print the object, it will print its id.
class DiagnosticTest(models.Model):
    """DiagnosticTest object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    # Adding tags to the DiagnosticTest Model fields
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


# Add a Tag class
# We are basing it off of just the basic Model class.
# This is similar to the DiagnosticTest model
# there is a fk relationship to User and similar to DiagnosticTest , its a cascade.
class Tag(models.Model):
    """Tag for filtering DiagnosticTests."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
