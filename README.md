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
1. Linting checks your code formatting. We will be using flake 8.
2. We will install flake 8
3. Then we wll run our flake 8 tool through docker compose via the command 'docker-compose run --rm app sh -c "flake8"'


## Testing (Django Test Framework)
1. We will be using the Django Test Suite to run our unit tests.
2. We will set up the tests for each different Django app we create
3. We will run the tests through Docker Compose with the command 'docker-compose run --rm app sh -c "python manage.py test"
4. The Django test framework is built on top of the unit test library.ls
5. The unit test library comes out of the box with Python, but the Django test framework adds some additional features to this library.
6. That's useful when you're testing Django projects.
7. Some of these additional features include things like the test client, which is a dummy web browser that you can use to make requests to your project.
8. It also allows you to simulate authentication so you can handle authentication by overriding it for your unit tests, which is useful when you're running tests because you don't always want to have to handle the log in and registration process for your test.
9. The Django test framework also comes with database integration.
10. It automatically creates a temporary database for you and then it will automatically clear the data from that database.
11. Once you've finished running each test on top of Django, we have the Django Rest framework, which also adds some additional testing features specifically useful for testing rest APIs.
12. The main one that we'll be using is the API test client, which is just like the test client that Django provides, except it's specifically used for testing API requests.
### Test Classes
1. SimpleTestCase : Tests that dont need database integration
2. TestCase : Tests that need database integration.

## Creating the Django Project
1. We going to create our Django project and we're going to do it via Docker Compose.
2. So the way that you do it is you run the following command in the terminal or they get Bash Command
3. 'docker-compose run --rm app sh -c "django-admin startproject app ."'
4. Now, because Django is installed inside our Docker image, we can run the CLIA commands just as if they were on our local machine.
5. What's going to happen here is it's going to create a new project called App and we specify the dot here to say create it in the current directory.
6. So here we have the new Django project added to our code.
7. The way that it was able to sync was through the volume that we defined in Docker Compose.
8. So because we have the app directory mapped, then what it does is anything we create inside the container gets mapped to our project and anything we create inside the project, our directory gets mapped tothe container.
9. So it's like a two way relationship thing where you can create files in the container and access them in the project and you can create files in the project and access them in the container.
10. The following are created when we create the Django Project :
    app folder inside the main app folder.
    __pycache__ folder
    __init__.py file
    asgi.py
    settings.py
    urls.py
    wsgi.py

## Run Our Development Server
1. So now that we've actually created our Django project, we can finally go ahead and run our development
server and see something in the browser.
2. From the terminal run the following command: 'docker compose up' . This is the command for starting our services.
3. Go to http://127.0.0.1:8000/ and you will see the Django Launch Page.
4. So this is the template that is added for all default Django projects.
5. This basically means that our project is working correctly and that we've configured everything with Docker.
6. We are running the services inside Docker.
7. To Stop the services, we can press Ctrl + C.

## Configure GitHub Actions
1. GitHub Actions is an automation tool. 
2. You start by setting up triggers. So triggers can be anything that happens to your project on GitHub.
3. There are various different trigger options. They're all documented on the GitHub actions website.
4. When this trigger occurs, for example, when the code is pushed to get hub, you then set up jobs that run when that trigger is hit.

5. Create a config file at DiagnosticTestRecommender/.github/workflows/checks.yml file.
6. Once you create the config file, the next time you commit and push your code to github, the github actions will run
7. If you look at the steps in github actions, you will see more steps than you added in the config file. these are added automatically.
8. We can see the log output by expanding these steps.

##  Database
1. We're going to be using Docker Compose to configure our database for our project.
2. So this will allow us to define the database configuration inside our actual project source code, which means it's reusable for other developers who might be working on the project. Or if we want to shift from one machine to another and it's also reusable for our deployment environment. The way we are going to do this is we are going to have two services in Docker Compose. One is the App and the other is the Database service.
3. We will be using the Postgresql database.

##  Connecting to our PostgreSql Database
1. Psycopg2 is the package needed for Django to connect to our PostGreSql database.
2. So to install psychology, too, they have a list of the package dependencies in the official documentation and this list includes the 
    C compiler 
    Python3-dev
    libpq-dev
3. For our alpine image , the equivalent packages are:
    postgresql-client
    build-base
    postgresql-dev
    musl-dev
    build-base, postgresqldev and musl-dev are only needed to install the psycop2 package. So these can be deleted after we build our project.

4. So we update our DockerFile to install these dependencies.
