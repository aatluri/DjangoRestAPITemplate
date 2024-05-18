# DiagnosticTestRecommender API

## GitHub Project & Docker Hub
1. Ensure you have github account
2. Ensure you have a docker hub account.
3. Create the repository in github. Add a readme file and a gitignore file.
4. Clone the repository onto your local machine
5. Set up the project with the credentials needed to authenticate with Docker Hub.
6. So head over to the Docker Hub page, which is Hub dot dot com, and we're going to click on your username here and click on account settings.
7. Then we're going to click on security and this will allow us to create something called an access token.
8. We're going to create a token by clicking new access token and you can give the token, the description,the name of the project.
9. Now you're only going to see this token once.Once you close this, you won't be able to get it back. 
10. However, if you do close, you don't worry.You can just simply delete the token and you can create a new token.
11. Go back to the github project And I'm going to click on Secrets. And then we're going to add a new repository secret.
12. First secret we're going to add is going to be the name of the user that we're going to log in. So I'm going to type DOCKERHUB_USER.
13. And then in the value, you want to put your Docker hub username. So that's the username you use to sign up to Docker Hub.
14. Next, we're going to add our token.
15. So click on New Repository Secret. We're going to add a second secret here.
16. I'm going to call this DOCKERHUB_TOKEN. Copy paste the value from Step 9.


## Linting
Linting checks your code formatting. We will be using flake 8.
We will install flake 8
Then we wll run our flake 8 tool through docker compose via the command 'docker-compose run --rm app sh -c "flake8"'


## Unit Testing
We will be using the Django Test Suite to run our unit tests.
We will set up the tests for each different Django app we create
We will run the tests through Docker Compose with the command 'docker-compose run --rm app sh -c "python manage.py test"

## Creating the Django Project
We going to create our Django project and we're going to do it via Docker Compose.
So the way that you do it is you run the following command in the terminal or they get Bash Command
'docker-compose run --rm app sh -c "django-admin startproject app ."'
Now, because Django is installed inside our Docker image, we can run the CLIA commands just as if they were on our local machine.
What's going to happen here is it's going to create a new project called App and we specify the dot here to say create it in the current directory.
So here we have the new Django project added to our code.
The way that it was able to sync was through the volume that we defined in Docker Compose.
So because we have the app directory mapped, then what it does is anything we create inside the container
gets mapped to our project and anything we create inside the project, our directory gets mapped tothe container.
So it's like a two way relationship thing where you can create files in the container and access them in the project and you can create files in the project and access them in the container.
The following are created when we create the Django Project :
app folder inside the main app folder.
__pycache__ folder
__init__.py file
asgi.py
settings.py
urls.py
wsgi.py

## Run Our Development Server
So now that we've actually created our Django project, we can finally go ahead and run our development
server and see something in the browser.
From the terminal run the following command: 'docker compose up' . This is the command for starting our services.
Go to http://127.0.0.1:8000/ and you will see the Django Launch Page.
So this is the template that is added for all default Django projects.
This basically means that our project is working correctly and that we've configured everything with Docker.
We are running the services inside Docker.
To Stop the services, we can press Ctrl + C.

## Configure GitHub Actions
The 