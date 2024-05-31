# This is used to mark our file as a shell script so that it is run by the shell. Its called a shebang
#!/bin/sh

# Any command that files in the rest of the file, it will ensure that the app crashes so that we can go and fix the error.
set -e

# Now we're going to type the commands that we use to start our service.
# First we want to make sure we wait for our database
python manage.py wait_for_db
# when we start our application, we can make sure that all of the static files for all of the different
# apps in our project are copied to the same directory.
# So we can make that directory accessible by the nginx reverse proxy.
# That way we can serve all of the files directly from that directory instead of having to send them through Django.
python manage.py collectstatic --noinput
# This will run any migrations when we start our app. The migrate scipt will ensure that only changes that have not been applied yet will be applied.
# So there is no harm in running this evertime we start our app.
python manage.py migrate

# Socket 9000
    # We set the socket to 9000 which is the port number from our nginx server to connect to the app
# workers
    # Then we're going to run workers for which says four different wsgi workers.
    # So the application is going to be running on four workers.
    # You can change this depending on the number of CPU's and things like that in your server.
# master
    # We set the uwsgi server or running application as the master thread
# enable threads
    # allows us to use multi threading
# module
    # This is saying we want to the run the wsgi file in our app/app folder.
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi