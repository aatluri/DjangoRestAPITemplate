"""
Django command to wait for the database to be available.
"""
# In this project we have the database and application on the same docker image which we will install on a server.
# Although we added a depends on condition in our docker compose file which ensures that the app service only starts
# after the db service, this can still lead to issues.
# This is because starting the db service doesnt necessarily mean that the postgresql database is up and running.
# And if the app services to start and connect to the db and if postgresql is not yet ready, the app will crash.
# To fix this race condition, we create another django app called Core and added a custom wait for db command which
# checks for the availability of the database before proceeding.

import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""
# When we call the wait_for_db command , it will call this handle method.
    def handle(self, *args, **options):
        """Entrypoint for command."""
        # Log a message
        self.stdout.write('Waiting for database...')
        # Set a boolean that tracks if the db is up to false.
        db_up = False
        while db_up is False:
            try:
                # we call the check method by passing
                # the database as a parameter.
                self.check(databases=['default'])
                db_up = True
            # If the database is not ready it will raise an exception
            # which is caught in the excep clause.
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
