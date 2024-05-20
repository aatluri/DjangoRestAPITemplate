"""
Test custom Django management commands.
"""
# in order to mock behaviour. We're going to mock the behavior of the database
# because we need to be able to simulate when the database is returning a
# response or not.
from unittest.mock import patch

# It's one of the possibilities of the errors that we might get when we try
# and connect to the database before the database is ready.
from psycopg2 import OperationalError as Psycopg2OpError

# Then we have the call command, which is a helper function provided by Django
# that allows us to simulate or to actually call a command by the name.
# And this allows us to actually call the command that we're testing.
from django.core.management import call_command

# And then we have another operational error, which is another exception that
# may get thrown by the database depending on what stage of the start up process it is.
# And we basically want to cover both options.
from django.db.utils import OperationalError

# And then we have a simple test case, which is the base test class
# that we're going to use for testing
from django.test import SimpleTestCase

# This basically says that we want to mock the wait_for_db command.
# The path decorator is used for mocking)
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

# Because we added a patch decorator at the top, we need to catch that in each of our test methods
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        # When we call check inside our command, we just want to return the value as TRUE.
        patched_check.return_value = True

        # Now we call the wait_for_db command. This will execute the code inside the wait_for_db command.
        call_command('wait_for_db')

        # So this basically ensures that the mocked value here i.e the check
        # method inside our command, the mocked object,
        # which is the check method inside our command, is called with these parameters.
        patched_check.assert_called_once_with(databases=['default'])
    
    # mock the sleep method.
    # So what's going to happen is we're going to actually be checking database ]
    # and then calling something called sleep,
    # which will wait for the set period of time before we check again
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # This is the way we raise an exception when the database is not ready.
        # The first 2 times we call the mocked method we want to raise the psycopsg2 error
        # The next 3 times we raise the operational error.
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # we are ensuring it was called 6 times.
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])