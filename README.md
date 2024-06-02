# DiagnosticTestRecommender API

https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/

## Explain what the project does
## Explain the general content of this code base i.e the different folders and files. What do the various apps do and where do we run the admin from or models or testing etc... What do we use for linting, testing, api docs etc..
## Prerequisites to Run this Project
## Explain how to run this project
## Create a superuser & Go to Django Admin Interface
## Go to the API Documentation Page
## Explain what happens in the code when each of the APIs are called.
## Steps if we want to reuse this codebase for another project or on another machine.
## What do we do if we want to create a new API based on a new model.

## Steps to setup this project
### See if we can download the Udemy Course content

## Common Questions
1. Why do we need an __init__.py
2. Get some info on how models, views, serialisers , urls interact with each other. What objects are passed and how to access some of the often used data in them. For example how do we get the current user in a view , serialiser etc..
3. What are mixins and how do they work? https://medium.com/silicon-tribe-techdev/mixins-and-viewclasses-in-django-rest-framework-5dcd3a42617d


## Understand the deployment of this project
### Steps
1. Setup a proxy (reverse proxy)
2. Handle Static & media files through this proxy
3. Cofigure our app on the server.

### Components
1. WSGI service - WebserviceGatewayInterface that runs the python code that powers our Django application
2. Persistant Data - When we use containers like Docker etc.., these are stateless ie they shouldnt store any data related to the current state of the application. For example if a user uploads a file, it should be stored in a persistent volume that can be accessed by the containers that are running or other containers that you store in your service.
3. Reverse Proxy - So this is what's going to accept the requests into our application. So any request that comes from the Internet, it's not going to go directly to our Django service or WSGI service. It's going to go through a proxy. The reason we need a proxy is due to the following reason :
A WSGI server is great at executing python code but its not effecient at executing Javascript, static content like images etc... especially when the load is high. A webserver on the other hand is great at handling these types of requests. So we set up a reverse proxy using a web server application that allows us to serve files that the webserver serves effeciently and sent the rest to the WSGI server so that it can be handled by the python code.

### Applications
1. nginx - a webserver . its open source, fast and production grade. We use it to set up the reverse proxy
2. uWSGI - the wsgi server
3. Docker Compose - to pull all these services together and serve them on our server.

### Diagram of different services and volumes
![Alt text](images/DeploymentOverview.jpeg)
1. App service will be used to run our application using the uWSGI server. This will server our Django Application
2. We will be using a Postgres database to store the persistent data
3. The proxy or reverse prixy engine service which will handle the requests to our application.
4. We will have a static volume that will be used to store static files like CSS, Javascript , media files etc..
5. We will have another volume that will store the persistent data for the database.

So when a user makes a request
1. they're going to be making the request to the proxy or to the reverse proxy. That's the nginx server that's running.
2. Then, depending on the URL of that request, if it's for a static file, we're going to afford it straight to the volume. So Engine X is going to serve the file directly if they're trying to access a static file.So they're trying to access something like a JavaScript file, a PNG or some kind of image. Then this is going to be sent directly from the volume by our proxy and our Django app never needs to hear about these requests.
3. However, if the request is not for a static file, then it will get forwarded to the uWSGI server that's running our application. This way, our application can fulfill the request and return the response to the user.

### Handling Configuration
1. We cant store our configurations in git as its not secure.
2. We need a way to set proper credentials and things inside our server when we deploy our application.
3. We will be using environment variables.
4. We create a .env file on the server
5. We set the values inside Docker Compose. We can pass configuration values from the .env file to into the applications we are running in our services

### Proxy Folder
1. As I mentioned previously, we're going to be using an application called nginX, and in order to use nginX, we need to add some configuration files to our product that tell nginX how to run our application.
2. default.conf.tpl : template configuration file that's going to be used by our Docker file in order to apply the custom configuration values to the application. The reason why we call it .TPL is because we're not going to be using this file directly when we run our proxy. We're going to be passing it through something in order to set some values in the file that sets the real file on the server.
So the main block we have here starting on line one is the configuration block for the server.
Listen_port is the port that the server will be listening on. Its set using an environment variable thats passed to our application
location blocks are ways that you can map different URL mappings for that passed into the server requests and you can map them to different places on the system.
So any your row that starts with /static will go to an alias called Vol/Static which has a volume containing the static and media files for our application.
The next location block handles all the requests that aernt met by the above location block.
So nginx will first check if the request matches /static. If it does then it will pass it to alias and stop executing the request. if it doesnt match then  it will pass it to the second location block.
In the second config block, we are configuring the server by app host and app port. this will tell the nginx server what host and port on the uwsgi server to connect to.
Include helps us include the uwsgi parameters which are required for the http request to be processed in wsgi
Next, we have client max body size. This is the maximum body size of the request that will be passed. So it basically means here that the maximum image that can be uploaded will be ten megabytes.
3. Uwsgi_params - required for the http request to be processed in wsgi
4. Run.sh : Shell script that starts our proxy service


### Scripts Folder - run.sh


### Docker Compose Deploy
The docker-compose.yml is used for local development. The docker-compose-deploy.yml is used for deployment.




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
4. List some important configuratins of flake8 that can be used.


## Creating Unit tests
1. High level explanation of the various tests, helper methods needed, apiclients etc..

## OpenAPI Doc/Swagger
1. How to configure and manual config needed for non standard methods.

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


## Database Migrations
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


## Creating the User API
1. Delete some of the unncessary files like admin, model, migrations etc..
2. We first create a serialiser for creating our user object and serializing our user object.
3. Serializers are used to convert complex data types, such as Django model instances, into Python data types that can be easily rendered into JSON, XML, or other content types. Serializers also provide deserialization, allowing parsed data to be converted back into complex types after first validating the incoming data. Serializers in Django are a part of the Django REST framework, a powerful and flexible toolkit for building Web APIs.
4. We create a serializer and create a view that uses this serializer.
5. So when you make the http type request, it goes through to the URL and then it gets passed into this create user view clause, which will then call the sterilizer and create the object and then return the appropriate response.
6. URL -> View-> Serializer -> Model
7. We first create a serializer that uses our model. We then create a view that uses our serializer. We then create a url pattern which when accessed will use the View. So when a http call is made to the url pattern defined, it calls the view thats is defined which inturn calls the serialiser which in turn uses the model.

### Authentication
1. We are using Token Authentication.
2. Well, basically you start by creating a token.
3. So we need to provide an endpoint that accepts the user's username and password or the email address and password. And that is then going to create a new token in our database and return that token to the client.
4. So then the client can store that token somewhere So that could be in session stores.
5. If you're using a web browser, it could be in the local storage, it could be in a cookie or it could be on an actual database on the local client.
6. every request that the client makes to the APIs that have to be authenticated is simply includes this token in the http headers of the request, and this means that the request can be authenticated in our backend.
7.  pros of using token authentication are that it is supported out of the box by Django rest framework.
8. Cons of token auth is that the token needs to be stored on the client side so if someone gets hold of it, they can impersonate the user.
9. Logging out happens on the client side and it works by deleting the token.
10. Talk about how authentication works, see views file.

## APIView vs ViewSets
URL -> View-> Serializer -> Model
Router -> ViewSet-> Serializer ->Model

## Creating the DiagnosticTest API
1. Create an app
2. Delete some of the unncessary files like admin, model, migrations etc..
3. Create the model, enalble it in Django Admin, create the migrations
4. Create a serializer
5. Create a APIView or ViewSet
6. Create a urls.py to route the urls
7. Update the main app urls.py to access the urls you set up for the diagnostic api.


## Steps when creating a new Model
1. Add the model to the models.py
2. Enable this in the Django Admin.
3. Then we run the migrations will create the migrations script to run on the database.
4. Register the model in admin.py
5. Then add a serialiser, view or viewset and update urls.py
7. Nested Serializers.
