# DiagnosticTestRecommender API

## Create GitHub Project
## Define Python Requirements
## Docker Configiration
### Docker File
### Docker Compose File
## Create Django Project
## Configure Github Actions
## Configure Database



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

##  Installing the PostgreSql Database Adapter
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

## Configure Database in Django
1. Open up settings.py and scroll to the database section
2. You will see a default database configured. This comes with all django projects.
3. You can replace that configuration wuth the equivalent for POstgreSql.

## Fixing Race Condition
1. Although we added a depends on condition in our docker compose file which ensures that the app service only starts after the db service, this can still lead to issues.
2. This is because starting the db service doesnt necessarily mean that the postgresql database is up and running. And if the app services to start and connect to the db and if postgresql is not yet ready, the app will crash.
3. To fix this race condition, we create another django app called Core and added a custom wait for db command which checks for the availability of the database before proceeding.


## Database Migrartions
1. Django comes witn an ORM (Object Relational Mapper)
2. The ORM serves as an abstraction layer between your data and your actual database.
3. All the manual work of setting up tables, adding columns, sql statements to add data, change data etc.. are handledn by Django using the ORM.
4. We first define our models
5. Models are Python classes wbased on the Python Models Base Class. Models also map to a table in your database. Models contain a name which is the name of the class and then some fields which would be the columns in your table. We can also store other metadata like relaltionships between tables. Finally, if you want to, you can add some custom python logic.So if you wanted to execute some code every time you saved or loaded something or you wanted to add some validation, you can add that to the python code.
5. Using these models you execute a Django command to generate migration files.
6. Then you run these migration files which will set up your database.
7. Ensure app is enabled in settings.py
8. use Django CLI to run "python manage.py makemigrations".
9. Then python manage.py migrate to apply the migrations to the database. If it's already being applied, then it doesn't do anything, it just skips on and it continues with next command.


## User Model
1. Django comes with a built in authentication system.
2. This gives us a basic framework of features that we can use for our project, including registration,login and authentication. So Django has some tools that allow us to relatively easily handle this.
3. The default Django user model is the foundation of the authentication system.
4. It's what includes the data of the users who register to this system using Django authentication, and it's also used to authenticate those users by checking their password.
5. Django comes with a default user model.
6. For example, by default it uses a username instead of a user's email address. And also it's not very easy to customize.
7. It's best to define your own user model so that it makes it easier to customize. It's kind of like future proofing your project.
8. The main difference between our user model and the default one is that we're going to be using an email instead of a username, but I'm going to show you how to do all of the work to set up a custom user model in case you want to add more customizations to your project later on.

## Creating your own User Model
1. Create a Model based from AbstractBaseClass and PermissionMixin. The AbstractBase class provides all of the authentication features. The PermissionsMixin is used for the Django permission system that allows you to assign permissions to different users.
2. Create a custom manager. The manager is mostly used for the Django CLI integration, but it's also used for other things like creating and managing objects that of the user
3. Set the auth user model configuration in your settings file and this will tell your Django project that you want to use this custom model foryour project.
4. Finaly you can create and run the migrations using the new custom user model.
