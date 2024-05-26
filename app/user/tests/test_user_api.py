"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# returns the full url path for user create inside our project
# So these reverse functions are looking for user and it's going to find it in the urls.py because
# we define app name equals user
# Then they match to the url patern like create or token or me etc..
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


# helper function that creates a user in our tests.
# **params gives us the flexibility to pass any parameters we want to the function
# The function calls the create_user method in the user model
def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


# First we will write tests for Unauthenticated requests like registering a user
class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

# creates an apiclient which we can use to test
    def setUp(self):
        self.client = APIClient()

# makes a httppost request to the url by passing the payload.
# checks that the endpoint returns a http 201 response which is the code returned for a sucessful create.
# retrieves the object from the database with the email requal to what we pass in
# validate that the object was actually created in the database ater we did the post.
# check if the password for the object returned matches our password for our test user.
# check that the password is not returned in the response of the post request.
    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

# First create the user with the payload by calling the create_user method
# Now try to create the same user by calling the post url for createing a user
# verify that we get a bad request code 400 in the response.
    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # This calls the filter mthod on the user model and calls the exists() which returns a boolean.
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        # validate that the boolean returned is false
        self.assertFalse(user_exists)

# So what this does is it adds a unit test that first creates a new user and then generates a payload
# that has the same email address and password. Then it posts the payload to the token URL
# And checks that the response result data includes a token and we also check that
# the status code was Hastie HTTP 200 which means auth was successful and user can be logged in.
# paylod to be sent to the token api to login
# create the user
# call the token url which calls the CreateTokenView which calls the AuthTokenSerializer.validate method
# The validate method validates the email and password and returns the  token.
# checks that the response includes a token which means auth was successful
# checks that the status code returned is a success i.e 200.
    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

# So what this does is it adds a unit test that first creates a new user and then generates a payload
# with a different password i.e incorrect password. Then it posts the payload to the token URL
# And checks that the response result data does not include a token and that the status code is 400.
    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email='test@example.com', password='goodpass')

        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

# So what this does is it adds a unit test that first creates a new user and then generates a payload
# with a different email. Then it posts the payload to the token URL
# And checks that the response result data does not include a token and that the status code is 400.
    def test_create_token_email_not_found(self):
        """Test error returned if user not found for given email."""
        payload = {'email': 'test@example.com', 'password': 'pass123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

# So what this does is it adds a unit test that first creates a new user and then generates a payload
# with a blank password. Then it posts the payload to the token URL
# And checks that the response result data does not include a token and that the status code is 400.
    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


# This is the setup method that is called before each test below.
# We are creating a test user that we can use for our tests.
# We call force auth so we can force auth for a specific user.
# so any request we make with this client will be authenticated with the specified user.
class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""
    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
# This calls the url that rereives the details of the current auth user which we set using force auth
        res = self.client.get(ME_URL)
# We then balidate if the detauls match and that the http code returned was 200.
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

# So what we're doing here is we're making sure that the HTP post method is disabled for any endpoint.
# Http Post should only really be used when you're creating objects in the system.
# Since this endpoint isn't designed to create objects, that's what the correct user API is for.
# This API should disable the post method for that endpoint.
# So you can't make post requests to this API because we're not actually going to be creating anything with this API.
    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

# So we have an existing user which we create in the setup above. So this is the existing user.
# We we're authenticated with our user.
# So we want to update the profile of that user, update a username and password or the name and password
# in this case.
# And what we do is we make the HTTP patch request to the ME endpoint and we pass in the payload and then
# we have to call refresh from DB so that the user values are refreshed from the database because by default
# they're not refreshed automatically.
# They are loaded when you first create the user and then you need to call refresh from DB method directly
# in order to get the updated data for that object.
# Then we check the name, password and status code.
    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {'name': 'Updated name', 'password': 'newpassword123'}
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
