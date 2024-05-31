# Docker & Django
# Advantages:
# 1. It allows you, as I mentioned earlier, to have a consistent development and production environment.
# 2. It also makes it easier to collaborate with other developers on the project and allows you to capture all of the dependencies for your Django projects in your actual source code.
# 3. You have the easier cleanup, which means when you're finished with your Django project,you can easily remove all the dependencies from your system.

# Disadvantages
# 1. Visual Studio code is unable to access the interpreterof your Python project.
# 2. It's difficult to configure your editor to use the integrated features that work with Python and other things such as the interactive debugger and also the learning tools that come with Visual Studio code.

# The Docker File has all of the operating system level dependencies required for our project
# We first choose the base image and then install all the dependencies on that image.


# Using python on the alpine linux image. It is is  light weight image We can find all the python images available at https://hub.docker.com/_/python
FROM python:3.9-alpine3.13

# This lets other developers know who maintains this app
LABEL maintainer="Adarsh Atluri"

# This is recommended when you are running Python in a Docker container. it tells Python that you don't want to buffer the output.
# The output from Python will be printed directly to the console, which prevents any delays of messages getting from our Python running application
# to the screen so we can see the logs immediately in the screen as they're running.
ENV PYTHONUNBUFFERED 1

# Copies the requirement.txt from our local machine to /tmp/requirments.txt on the docker image.
COPY ./requirements.txt /tmp/requirements.txt
# Copies the requirement.dev.txt from our local machine to /tmp/requirments.txt on the docker image.
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# This will copy the scripts folder to the docker image. The scripts folder will contain helper scripts.
COPY ./scripts /scripts

# Copies the app directory
COPY ./app /app
# Next we set the WORKDOR. it's the default directory that will commands are going to be run from when we run commands on our Docker image.
# basically we're setting it to the location where our Django project is going to be sent to so that
# when we run the commands, we don't need to specify the full path of the Django Management Command. It will automatically be running from before slash app directory.
WORKDIR /app

# Next we set expose 8000, which says we want to expose Port 8000 from our container to our machine when we run the container.
# it allows us to access that port on the container that's running from our image. And this way we can connect to the Django Development Server.
EXPOSE 8000

# Sets a build argument called DEV and sets it to false. We override this DEV to TRUE in the Docker Compose configuration. So when we use
# So when we use this docker follow through this docker compose configuration, it's going to update this dev to true.
# Whereas when we use it in any other Docker compose configuration, it's going to leave it as false.
# So by default, we're not running in development mode.
ARG DEV=false

# First we create a new python virtual environment.
RUN python -m venv /py && \
# Upgrade pip for the virtual environment we just created
    /py/bin/pip install --upgrade pip && \
# Installing the postgresql-client package inside our alpine image in order for the psycopg2 package to be able to connect to Postgre
    apk add --update --no-cache postgresql-client jpeg-dev && \
# Sets a virtual dependency package. It groups all the packages we install under this name so that they can be deleted later.
# We then add the musl-dev packages we need to be able to install the psycop2 package.
# We also add linux headers which is required for the Uwsgi server installation. its not required after the uwsgi server is installed and so put in the tmp section.
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
# Install all the requirements inside the virtual environment.
    /py/bin/pip install -r /tmp/requirements.txt && \
# If dev equals to true then it installs the dev dependencies. the fi is how you end an if statement in shell script.
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
# remove the tmp directory to keep the image lightweight.
    rm -rf /tmp && \
# we remove the virtual dependency package we created in line 55. Because these packages are only needed to install psycop2 and are not needed post that.
    apk del .tmp-build-deps && \
# Adds a new user inside our image.
# The reason we do this is because it's best practice not to use the root user. If we didn't specify this bit, then the only user available inside the alpine image that we're using
# would be the root user.
# The root user is the user that has the full access and permissions to do everything on the on the server. So any thing that you can do can be done by the root use. It has no restrictions or limitations.
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
# This is for the images etc...
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
# Makes sure we able to execute scripts inside our scripts directory
    chmod -R +x /scripts

# Sets the path environment variable so that we dont need to specify the full python path every time we run a command.
# We add scripts to the path so that we can run them as well as python.
ENV PATH="/scripts:/py/bin:$PATH"

# Specifies the user we are switching to. Until now everything was being done as the root user.
USER django-user

# Name of the script that we create that runs our application.
# So the command here, the bottom is the default command that's run for docker containers that are spawned
# from our image that's built from this Docker file.
# You can override this using Docker compose, and we will be overriding it for our development server
# because our development server is going to be using our manage.py server command instead of UWSGI
# But for deployment we will be using UWSGI and so we will be using this command.
CMD ["run.sh"]


# Command to create the image is : docker build .

