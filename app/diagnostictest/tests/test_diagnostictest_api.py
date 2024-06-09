
"""
Tests for recipe APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    DiagnosticTest,
    Tag,
)

from diagnostictest.serializers import (
    DiagnosticTestSerializer,
    DiagnosticTestDetailSerializer,
)


DIAGNOSTICTEST_URL = reverse('diagnostictest:diagnostictest-list')


# Helper method for create user
def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


# Creates the url for getting the detail of a diagnostictest
def detail_url(diagnostictest_id):
    """Create and return a diagnostictest detail URL."""
    return reverse('diagnostictest:diagnostictest-detail', args=[diagnostictest_id])


# And basically, this is going to be a helper function that we use in our test for creating a diagnostictest.
def create_diagnostictest(user, **params):
    """Create and return a sample diagnostictest."""
    defaults = {
        'title': 'Sample diagnostictest title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/diagnostictest.pdf',
    }
    # We create a default dictionary and update whatever was passed through params.
    # We do this because we dont want to directly use the values of params
    defaults.update(params)
    diagnostictest = DiagnosticTest.objects.create(user=user, **defaults)
    return diagnostictest


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests."""

# Gives us a test client which we can use for the tests added to this class
    def setUp(self):
        self.client = APIClient()

# tests the API as an unauthenticated user. The diagnostic tests can only be retreived by logged in users.
    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(DIAGNOSTICTEST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated API requests."""

    # Creating a method that creates the client, user and authenticates the user.
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

# So what this test does is we create two recipes and then we call the res.client.get a
# nd we assign the value to response. So that makes the request to the API.
# Now, because we have created the recipes with the user that we're authenticated with, we should see
# both of these recipes returned by our API.
# So all the recipes in the system should be returned.
# And we check that by retrieving all the diagnostictests using .objects.all
# We're checking the order by setting the order to reverse ID order, and then we're passing in all the
# diagnostictests that we got in the test to the serializer
# And then we're checking that the response code is the correct hasty 200 okay Response.
# And then the data return matches the data of all of the recipes from the serialize.
    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        create_diagnostictest(user=self.user)
        create_diagnostictest(user=self.user)
        res = self.client.get(DIAGNOSTICTEST_URL)
        diagnostictests = DiagnosticTest.objects.all().order_by('-id')
        serializer = DiagnosticTestSerializer(diagnostictests, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

# This test is similar to the one above except that we are using 2 different users
# and checking that we only return the logged in users diagnostic tests when we call the list url.
    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""
        other_user = create_user(email='other@example.com', password='test123')
        create_diagnostictest(user=other_user)
        create_diagnostictest(user=self.user)
        res = self.client.get(DIAGNOSTICTEST_URL)
        diagnostictests = DiagnosticTest.objects.filter(user=self.user)
        serializer = DiagnosticTestSerializer(diagnostictests, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

# We create a diagnostic test , call the detail url
# pass the diagnostictest to the serializer.
# Then compare the data we get back fromn serialiser with the data we get back from the detail url.
    def test_get_recipe_detail(self):
        """Test get recipe detail."""
        diagnostictest = create_diagnostictest(user=self.user)
        url = detail_url(diagnostictest.id)
        res = self.client.get(url)
        serializer = DiagnosticTestDetailSerializer(diagnostictest)
        self.assertEqual(res.data, serializer.data)

# So we're going to we can start by defining a payload.
# This is a sample payload that we can post to our recipe endpoint.
# Then we're calling the client a post to make a http post request to our diagnostictest URL
# and we're passing in the payload.
# We check if get a 201 code which means the object was created.

    def test_create_recipe(self):
        """Test creating a recipe."""
        initialpayload = {
            'title': 'Sample recipe',
            'time_minutes': 30,
            'price': Decimal('5.99'),
        }
        res = self.client.post(DIAGNOSTICTEST_URL, initialpayload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
# We then retreive the specific dianostic test that was returned in data from the http post call whch we store in res.
        diagnostictest = DiagnosticTest.objects.get(id=res.data['id'])
# We then compare each of the items in the initialpayload with the data in res.
        for k, v in initialpayload.items():
            self.assertEqual(getattr(diagnostictest, k), v)
# We also ensire that the userassined to the api matches the user we are authenticated with.
        self.assertEqual(diagnostictest.user, self.user)

# We first create a diagnostic test
# We retrieve the diagnostictest detail using the detail url
# We then do an update on the diagnostictest using patch and update the title
# We then referesh the diagnostictest object from the db to get the latest update into it.
# We then compare the refreshed diagnostictest object with the updated title value and other fields
    def test_partial_update(self):
        """Test partial update of a diagnostictest."""
        original_link = 'https://example.com/recipe.pdf'
        diagnostictest = create_diagnostictest(
            user=self.user,
            title='Sample diagnostictest title',
            link=original_link,
        )

        payload = {'title': 'New diagnostictest title'}
        url = detail_url(diagnostictest.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        diagnostictest.refresh_from_db()
        self.assertEqual(diagnostictest.title, payload['title'])
        self.assertEqual(diagnostictest.link, original_link)
        self.assertEqual(diagnostictest.user, self.user)

# Same as above exceot that we test a full udpate, so we use put instead of patch.
    def test_full_update(self):
        """Test full update of diagnostictest."""
        diagnostictest = create_diagnostictest(
            user=self.user,
            title='Sample diagnostictest title',
            link='https://exmaple.com/diagnostictest.pdf',
            description='Sample diagnostictest description.',
        )

        payload = {
            'title': 'New diagnostictest title',
            'link': 'https://example.com/new-diagnostictest.pdf',
            'description': 'New diagnostictest description',
            'time_minutes': 10,
            'price': Decimal('2.50'),
        }
        url = detail_url(diagnostictest.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        diagnostictest.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(diagnostictest, k), v)
        self.assertEqual(diagnostictest.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the recipe user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        diagnostictest = create_diagnostictest(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(diagnostictest.id)
        self.client.patch(url, payload)

        diagnostictest.refresh_from_db()
        # We check that the user has not beed updated and is still self.user and not new_user.
        self.assertEqual(diagnostictest.user, self.user)

# We create a diagnostic test using the helper method
# We get the detail url ie the url which includes the diagnostictestid
# Then we call the http delete method
# Check the status code and that the diagnostictest doesnt exist.
    def test_delete_recipe(self):
        """Test deleting a recipe successful."""
        diagnostictest = create_diagnostictest(user=self.user)

        url = detail_url(diagnostictest.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DiagnosticTest.objects.filter(id=diagnostictest.id).exists())

# We create a new user using the helper method
# So we have 2 users ie the new_user and the user in self.user
# We create a diagnostictest using the new_user
# We get the detail url ie the url which includes the diagnostictestid
# Then we call the http delete method using the self.user
# Check the status code is 404 ie the diagnostictest was not found as it was not created by self.user
# Check that the diagnostictest still exists.
    def test_recipe_other_users_recipe_error(self):
        """Test trying to delete another users recipe gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        diagnostictest = create_diagnostictest(user=new_user)

        url = detail_url(diagnostictest.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(DiagnosticTest.objects.filter(id=diagnostictest.id).exists())

# Create the paylod which includes 2 tags
# Call the post method. This should create the diagnostictest
# and also create the 2 tags and assign it to the diagnistoctest
# Check the statuscode
# Get the diagnoistictests assigned to this user. Check that the count is 1
# Check that number of tags matches the number of tags in the payload and that their names match.
    def test_create_recipe_with_new_tags(self):
        """Test creating a recipe with new tags."""
        payload = {
            'title': 'Thai Prawn Curry',
            'time_minutes': 30,
            'price': Decimal('2.50'),
            'tags': [{'name': 'Thai'}, {'name': 'Dinner'}],
        }
        res = self.client.post(DIAGNOSTICTEST_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        diagnostictests = DiagnosticTest.objects.filter(user=self.user)
        self.assertEqual(diagnostictests.count(), 1)
        diagnostictest = diagnostictests[0]
        self.assertEqual(diagnostictest.tags.count(), 2)
        for tag in payload['tags']:
            exists = diagnostictest.tags.filter(
                name=tag['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

# Create a tag
# Create the paylod which includes 2 tags. One tag should have the same name as the tag already created
# Call the post method. This should create the diagnostictest
# and also assign the 2 tags to the diagnistoctest. For the tag that was already created it
# should just assign it. For the one that doesnt exist it should create and assign it.
# Check the statuscode
# Get the diagnoistictests assigned to this user. Check that the count is 1
# Check that number of tags is still 2 and not 3.
# i.e it should have only created one tag as the other was already there
# Check that the tag names match.
    def test_create_diagnostictest_with_existing_tags(self):
        """Test creating a diagnostictest with existing tag."""
        tag_indian = Tag.objects.create(user=self.user, name='Indian')
        payload = {
            'title': 'Pongal',
            'time_minutes': 60,
            'price': Decimal('4.50'),
            'tags': [{'name': 'Indian'}, {'name': 'Breakfast'}],
        }
        res = self.client.post(DIAGNOSTICTEST_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        diagnostictests = DiagnosticTest.objects.filter(user=self.user)
        self.assertEqual(diagnostictests.count(), 1)
        diagnostictest = diagnostictests[0]
        self.assertEqual(diagnostictest.tags.count(), 2)
        self.assertIn(tag_indian, diagnostictest.tags.all())
        for tag in payload['tags']:
            exists = diagnostictest.tags.filter(
                name=tag['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

# Create a diagnostictest with the helper method
# create a payload with a tag
# create the duagnostictest detail url with the diagnostictest created.
# Call the patch method by passing the payload
# Check that the status code 200 was returned
# Check that a tag object was created with the name in the payload
# Check that the tab created is mapped to the diagnostictest created.
    def test_create_tag_on_update(self):
        """Test create tag when updating a DiagnosticTest."""
        diagnostictest = create_diagnostictest(user=self.user)

        payload = {'tags': [{'name': 'Lunch'}]}
        url = detail_url(diagnostictest.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_tag = Tag.objects.get(user=self.user, name='Lunch')
        self.assertIn(new_tag, diagnostictest.tags.all())

# We create a tag object named breakfast
# We create a diagnostictest object
# We update the diagnostictest with the tab object
# We create a new tag object named lunch
# We create a payload with a tag named lunch.
# We create a detail url with the diagnostictest id created
# We call the diagnostictest patch method.
# We validate that the status code was 200
# We validate that the breakfast and lunch tag objects exist and are mapped to the diagnostictest
    def test_update_diagnostictest_assign_tag(self):
        """Test assigning an existing tag when updating a recipe."""
        tag_breakfast = Tag.objects.create(user=self.user, name='Breakfast')
        diagnostictest = create_diagnostictest(user=self.user)
        diagnostictest.tags.add(tag_breakfast)

        tag_lunch = Tag.objects.create(user=self.user, name='Lunch')
        payload = {'tags': [{'name': 'Lunch'}]}
        url = detail_url(diagnostictest.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(tag_lunch, diagnostictest.tags.all())
        self.assertNotIn(tag_breakfast, diagnostictest.tags.all())

# We create a tag object named Dessert
# We create a diagnostictest object
# We update the diagnostictest with the tag Dessert
# We create a payload with an empty tags list
# We create the diagnostictest detail url with the diagnostictest created
# We call the patch method
# We check that we got the status code 200
# We check that the diagnostictest has no tags.
    def test_clear_recipe_tags(self):
        """Test clearing a recipes tags."""
        tag = Tag.objects.create(user=self.user, name='Dessert')
        diagnostictest = create_diagnostictest(user=self.user)
        diagnostictest.tags.add(tag)

        payload = {'tags': []}
        url = detail_url(diagnostictest.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(diagnostictest.tags.count(), 0)

# This test creates 3 diagnostic tests and 2 tags. The first test is assigned the first tag.
# The second test is assigned the second tag.
# The third test is not assigned any tag
# We then filter by both tags.
# So we validate that none of the tests are returned as by including both tags in the filter parameters
# we only want tests that have both tags.
    def test_filter_by_tags(self):
        """Test filtering Diagnostic Tests by tags """
        """Check no tests are returned when there is no test with all the tags being search for."""
        r1 = create_diagnostictest(user=self.user, title='Thai Vegetable Curry')
        r2 = create_diagnostictest(user=self.user, title='Aubergine with Tahini')
        tag1 = Tag.objects.create(user=self.user, name='Vegan')
        tag2 = Tag.objects.create(user=self.user, name='Vegetarian')
        r1.tags.add(tag1)
        r2.tags.add(tag2)
        r3 = create_diagnostictest(user=self.user, title='Fish and chips')
        params = {'tags': f'{tag1.id},{tag2.id}'}
        res = self.client.get(DIAGNOSTICTEST_URL, params)
        s1 = DiagnosticTestSerializer(r1)
        s2 = DiagnosticTestSerializer(r2)
        s3 = DiagnosticTestSerializer(r3)
        self.assertNotIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)
        self.assertNotIn(s3.data, res.data)

# We want to verify the filter feature for the Basic Health Check ups
    def test_filter_by_tags_exactmatch_basichealthcheckup(self):
        """Test filtering recipes by tags with an exact match."""
        """ Check that only tests with all the tags being searched for are returned."""
        youngmale = Tag.objects.create(user=self.user, name='YoungMale')
        oldmale = Tag.objects.create(user=self.user, name='OldMale')
        youngfemale = Tag.objects.create(user=self.user, name='YoungFemale')
        oldfemale = Tag.objects.create(user=self.user, name='OldFemale')
        cbc = create_diagnostictest(user=self.user, title='CBC')
        mammo = create_diagnostictest(user=self.user, title='Mammography')
        psa = create_diagnostictest(user=self.user, title='PSA')
        cbc.tags.add(youngmale)
        cbc.tags.add(oldmale)
        cbc.tags.add(youngfemale)
        cbc.tags.add(oldfemale)
        mammo.tags.add(youngfemale)
        mammo.tags.add(oldfemale)
        psa.tags.add(oldmale)

        cbcs1 = DiagnosticTestSerializer(cbc)
        mammos2 = DiagnosticTestSerializer(mammo)
        psas3 = DiagnosticTestSerializer(psa)

        # We search by tags oldmale
        params = {'tags': f'{oldmale.id}'}
        res = self.client.get(DIAGNOSTICTEST_URL, params)
        self.assertIn(cbcs1.data, res.data)
        self.assertIn(psas3.data, res.data)
        self.assertNotIn(mammos2.data, res.data)

    # We want to verify the filter feature for the HealthHistory based tests
    def test_filter_by_tags_exactmatch_healthhistory(self):
        """Test filtering recipes by tags with an exact match."""
        """ Check that only tests with all the tags being searched for are returned."""
        hrct = create_diagnostictest(user=self.user, title='HRCT')
        pft = create_diagnostictest(user=self.user, title='PST')
        spiometry = create_diagnostictest(user=self.user, title='SPIOMETRY')
        impulseoscillometry = create_diagnostictest(user=self.user, title='IMPULSE OSCILLOMETRY')
        fibroscan = create_diagnostictest(user=self.user, title='FIBROSCAN')
        afp = create_diagnostictest(user=self.user, title='AFP')
        pivika = create_diagnostictest(user=self.user, title='PIVIKA')
        viralload = create_diagnostictest(user=self.user, title='VIRALLOAD')
        serum = create_diagnostictest(user=self.user, title='SERUMHBSAGHIVHCV')

        male = Tag.objects.create(user=self.user, name='Male')
        female = Tag.objects.create(user=self.user, name='Female')
        heavysmoker = Tag.objects.create(user=self.user, name='Heavy SMoker')
        lightsmoker = Tag.objects.create(user=self.user, name='Light Smoker')
        # nonsmoker = Tag.objects.create(user=self.user, name='Non Smoker')
        heavydrinker = Tag.objects.create(user=self.user, name='Heavy Drinker')
        occasionaldrinker = Tag.objects.create(user=self.user, name='Occasional Drinker')
        # nondrinker = Tag.objects.create(user=self.user, name='Non Drinker')
        hbvpositive = Tag.objects.create(user=self.user, name='HBV Positive')
        hbvnegative = Tag.objects.create(user=self.user, name='HBV Negative')
        bloodexposure = Tag.objects.create(user=self.user, name='Blood Exposure')
        # nobloodexposure = Tag.objects.create(user=self.user, name='No Blood Exposure')

        hrct.tags.add(male)
        hrct.tags.add(female)
        hrct.tags.add(heavysmoker)

        pft.tags.add(male)
        pft.tags.add(female)
        pft.tags.add(heavysmoker)
        pft.tags.add(lightsmoker)

        spiometry.tags.add(male)
        spiometry.tags.add(female)
        spiometry.tags.add(heavysmoker)
        spiometry.tags.add(lightsmoker)

        impulseoscillometry.tags.add(male)
        impulseoscillometry.tags.add(female)
        impulseoscillometry.tags.add(heavysmoker)
        impulseoscillometry.tags.add(lightsmoker)

        fibroscan.tags.add(male)
        fibroscan.tags.add(female)
        fibroscan.tags.add(heavydrinker)

        afp.tags.add(male)
        afp.tags.add(female)
        afp.tags.add(heavydrinker)
        afp.tags.add(occasionaldrinker)

        pivika.tags.add(male)
        pivika.tags.add(female)
        pivika.tags.add(heavydrinker)
        pivika.tags.add(occasionaldrinker)

        viralload.tags.add(male)
        viralload.tags.add(female)
        viralload.tags.add(hbvpositive)

        serum.tags.add(male)
        serum.tags.add(female)
        serum.tags.add(hbvnegative)
        serum.tags.add(bloodexposure)

        hrct_serialized = DiagnosticTestSerializer(hrct)
        pft_serialized = DiagnosticTestSerializer(pft)
        spiometry_serialized = DiagnosticTestSerializer(spiometry)
        impulseoscillometry_serialized = DiagnosticTestSerializer(impulseoscillometry)
        fibroscan_serialized = DiagnosticTestSerializer(fibroscan)
        afp_serialized = DiagnosticTestSerializer(afp)
        pivika_serialized = DiagnosticTestSerializer(pivika)
        viralload_serialized = DiagnosticTestSerializer(viralload)
        serum_serialized = DiagnosticTestSerializer(serum)

        # We search by tags for male and heavy smoker.
        params = {'tags': f'{male.id},{heavysmoker.id}'}
        res = self.client.get(DIAGNOSTICTEST_URL, params)
        self.assertIn(hrct_serialized.data, res.data)
        self.assertIn(pft_serialized.data, res.data)
        self.assertIn(spiometry_serialized.data, res.data)
        self.assertIn(impulseoscillometry_serialized.data, res.data)
        self.assertNotIn(fibroscan_serialized.data, res.data)
        self.assertNotIn(afp_serialized.data, res.data)
        self.assertNotIn(pivika_serialized.data, res.data)

        # We search by tags for female and heavy drinker.
        params = {'tags': f'{female.id},{heavydrinker.id}'}
        res = self.client.get(DIAGNOSTICTEST_URL, params)
        self.assertIn(fibroscan_serialized.data, res.data)
        self.assertIn(afp_serialized.data, res.data)
        self.assertIn(pivika_serialized.data, res.data)
        self.assertNotIn(serum_serialized.data, res.data)
        self.assertNotIn(viralload_serialized.data, res.data)

        # We search by tags for female , hbv negative and blood exposure.
        params = {'tags': f'{female.id},{hbvnegative.id},{bloodexposure.id}'}
        res = self.client.get(DIAGNOSTICTEST_URL, params)
        self.assertNotIn(fibroscan_serialized.data, res.data)
        self.assertNotIn(afp_serialized.data, res.data)
        self.assertNotIn(pivika_serialized.data, res.data)
        self.assertIn(serum_serialized.data, res.data)
        self.assertNotIn(viralload_serialized.data, res.data)
