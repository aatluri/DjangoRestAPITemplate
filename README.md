# DiagnosticTestRecommender API

## Motivation behind this project
1. While working on real world projects or ideas, we spend a lot of time on tasks like project setup, cicd pipeline set up, deployment, documentation than on the actual implementation of our idea.
2. This project provides you a boiler plate project template with all the necessary things built in.
3. All you need to do is download this code base and follow a few simple steps to get it running on your machine or on AWS.
4. Then you can extend the logic inside this already deployed project to suit your needs.

## What does this project do
1. This is a ready to go Django REST API project template.
2. It has a complete CICD pipeline using GitHub Actions
3. The CICD Pipeline includes, linting, testing and deployment.
4. The project can be deployed locally as well as to the cloud like AWS or any other cloud servide.
6. It exposes REST endpoints that allow us to get/put/post/delete users who will be accessing this endpoint
7. It exposes REST endoints that allow us to get/put/post/delete an entity. In this case its a diagnostictest. What i mean here by a diagnostictest is tests like cbc, urine analysis etc...
9. It provides the capability to assign tags to the diagnostictests being exposed and also has a search capability that allows us to search for diagnostictests based on these tags.
10. It also has API documentation implemented.

## Real World Application of this project
I build this api to be able to filter diagnostic tests based on tags assigned to them. The tags would be patient symptoms and/or their family health history details. The purpose was to use this in hospitals or labs so that based on the patients health history & symptoms, we can return the respective diagnostictests that are recommended.  But you can update the diagnostictest entity to be whatever you need. For example it could be a recipe with tags. You can always duplicate the tags and also have ingredients. Then you would be able to filter a recipe based on tags and ingredients.

## Technologies used in this project
1. Python :  The programming language we will be using.
2. Django : We will be using Django on top of the Python framework. It's basically a Python framework for building websites.
3. Django Rest Framework : It adds features for building rest APIs. We will install this into Django.
4. PostGres : PostGres will be the database we will be using to store data. We will be defining the database configuration inside our actual project source code, which means it's reusable for other developers who might be working on the project. Or if we want to shift from one machine to another and it's also reusable for our deployment environment. So we have the database and application on the same docker image which we will install on a server.
5. Docker:  Docker is a software platform that allows you to build, test, and deploy applications quickly. Docker packages software into standardized units called containers that have everything the software needs to run including libraries, system tools, code, and runtime. We will be running a dockerized service of our API as well as a dockerized service of our database. This allows us to create a development environment that we can use to build our application. And also it allows us to easily deploy our application to a server.
6. Swagger UI : This will serve as documentation for our API and also give us a browser API that we can use to test
7. We will be using the Djanto Test Framework for the Unit Tests
8. We will be using Flake8 for Code Linting.
9. GitHub Actions : So GitHub actions is going to handle the CICD part. So it'll be used to run things like testing and linting every time we make changes to our code and push the code up to GitHub.


## Django Project Structure
1. app/ : This is the main Django app which is called app
2. app/core/ : This Django app contains code that is shared by multiple apps like the database definition using Django Models.
3. app/user/ : This Django app has everything that is needed for our User APIs. This will be called user and it will handle things such as the user registration and creating authentication tokens.
4. app/diagnostictest/ : This Django app will have everything to do with our diagnostictest api

## Contents of this code base
This code base as mentioned above is a Django REST API application.
It has the following folders at the root level :
1. .github/workflows -  This is a yaml configuration file is used by github actions for the cicd pipeline. We define what actions we want github to run when we push code to the master branch.
2. app folder - This contains all of the Django project files. It consists of the the multiple django apps we define for our application. It has the following contents:
    - manage.py : It is command-line utility for Django projects. It is generated automatically. It is placed in the root directory of the current project. It sets the DJANGO_SETTINGS_MODULE environment variable to point to the project’s settings.py file.
    - app : This is the main Django app folder that consists of the main Django files like settings.py, the urls that are exposed , the swagger documentation url etc..
        - __init__.py : the __init__.py file is used to mark a directory as a Python package. it comes by default when you create a Django project
        - asgi.py : As well as WSGI, Django also supports deploying on ASGI, the emerging Python standard for asynchronous web servers and applications. Django’s startproject management command sets up a default ASGI configuration for you, which you can tweak as needed for your project, and direct any ASGI-compliant application server to use.
        - settings.py : The settings.py file is the central one for configuring all Django projects. It is nothing else than a Python module with defined variables. All variables inside are constants, and according to PEP 0008 convention, they should be written with capital letters.
        - urls.py : This is the entry point for the project. Contains the root URL configuration of the entire project
        - wsgi.py : It is mostly used during deployment. It is used as an interface between application server to connect with django or any python framework which implements wsgi
    - core : We use this Django app to manage the admin functionalities of our project. It has the following contents:
        - management/commands/wait_for_db.py : In this project we have the database and application on the same docker image which we will install on a server. So we want the application to come up only after the database is available so that when we run the migrations, the db is available. So we created this wait for db command which we call before calling the main application. If we have a remote database, then we dont need to have this command.
        - migrations : The files in this folder are autogenerated. These are the database scripts which are generated based on the models we create in the models.py file
        - tests : This folder consists of the unit tests for this app.
        - admin.py : We customise the Django admin page in this file
        - models.py : This file consists of the database tables we need and their fields etc..
        - apps.py : This is generated by default by Django. It is used by Django when we run the application to create a class for each of the apps using this file if it exists. Otherwise it will use the base AppConfig.
    - user : We use this Django app to manage everything about the users who will access our APIs.
        - tests : This folder consists of the unit tests for this app.
        - apps.py : This is generated by default by Django. It is used by Django when we run the application to create a class for each of the apps using this file if it exists. Otherwise it will use the base AppConfig.
        - serializers.py : In this file we create the serializers for the User model.
        - urls.py : We create the url patterns we want for user. So once the user url is added to the urls.py in the app folder, all the url pattenrs of user will be accessible to a user.
        - views.py : We create the views for the user which are used in the serializer.
    - diagnostictest : We use this Django app to manage everthing about the diagnostictest entity and the tags entity which we use to filter diagnostictests by.
        - tests : This folder consists of the unit tests for this app.
        - apps.py : This is generated by default by Django. It is used by Django when we run the application to create a class for each of the apps using this file if it exists. Otherwise it will use the base AppConfig.
        - serializers.py : In this file we create the serializers for the diagnostictest and tags models.
        - urls.py : We create the url patterns we want for diagnostictests and tags. So once the diagnostictest and tags urls are added to the urls.py in the app folder, all the url pattenrs of diagnostictest and tags will be accessible to a user.
        - views.py : We create the views for the diagnostictest and tags which are used in the serializer.
    - images : We store any images we use in the readme file here.
    - proxy : This is mainly related to when we need to deploy the project to a cloud serivice. See the Cloud Deployment Process Summary Section .
    In order to use nginX, we need to add some configuration files to our product that tell nginX how to run our application. The contents of the proxy folder are:
        - default.conf.tpl : template configuration file that's going to be used by our Docker file in order to apply the custom configuration values to the application. The reason why we call it .TPL is because we're not going to be using this file directly when we run our proxy. We're going to be passing it through something in order to set some values in the file that sets the real file on the server.
        So the main block we have here starting on line one is the configuration block for the server.
        Listen_port is the port that the server will be listening on. Its set using an environment variable thats passed to our application
        location blocks are ways that you can map different URL mappings for that passed into the server requests and you can map them to different places on the system.
        So any your row that starts with /static will go to an alias called Vol/Static which has a volume containing the static and media files for our application.
        The next location block handles all the requests that aernt met by the above location block.
        So nginx will first check if the request matches /static. If it does then it will pass it to alias and stop executing the request. if it doesnt match then  it will pass it to the second location block.
        In the second config block, we are configuring the server by app host and app port. this will tell the nginx server what host and port on the uwsgi server to connect to.
        Include helps us include the uwsgi parameters which are required for the http request to be processed in wsgi
        Next, we have client max body size. This is the maximum body size of the request that will be passed. So it basically means here that the maximum image that can be uploaded will be ten megabytes.
        - Uwsgi_params - required for the http request to be processed in wsgi
        - Run.sh : Shell script that starts our proxy service
    - scripts : This consists of a run.sh file which is run once all of our application components i.e the webserver, wsgi server , database etc... are up
    - .dockerignore :  A .dockerignore is a configuration file that describes files and directories that you want to exclude when building a Docker image
    - .env.sample : It consists of the environment variables wihch are used in our docker-compose-deploy.yml. This file is renamed to .env when deploying.
    - .gitognore : Files that should be ignored by git.
    - .flake8 : We use flake8 for linting. This file tells flake8 which files to ignore.
    - docker-compose-deploy.yml : Dockercompose defines how Docker images should be used to run on our production server. This is the docker-compose file that is used for build and deployment in the cloud once its set up.
    - docker-compose.yml : Dockercompose defines how Docker images should be used to run on our development server. This is used for build and deployment on the local machine.
    - Dockerfile : The Docker File is just a list of steps that docker uses to build our image.
    - requirements.dev.txt : Mentions all the python dependencies in the dev environment
    - requirements.txt : Mentions all the python dependencies in the prod environment.



## Setup
This section will do the following:
1. Set up your system with the necessary software needed
2. Set up the project
3. Set up the CICD pipeline
Once the above is done, you will be able to build & deploy your project.

### System Setup
1. Install a code editor. I used VSCode
2. Install Docker Desktop for Windows or Mac
    - Once you are done installing, run the below commands to verify the install.
    - Run docker --version
    - Run docker-compose --version
3. Install Git
    - Most machines already come with git installed but since we are using Github actions for the CICD pipeline, you will need to ensure that git is installed.

### Project Setup
**Git**
1. Go to your github account and create a repository. Copy the https or ssh url for your project.
2. Then on your local machine, go to the location where you want to clone the repository
3. Run git clone "url for the project".

**GitHub & DockerHub**
1. Go to hub.docker.com and sign in to your account
2. Go to your profile/Account Settings/ Security
3. Create an Access Token. You can choose any name for your token but its good practice to use the name of your github repo.
4. Copy the access token. Once you close the access token, you wont be able to see it again but you can always delete and recerate it.
5. Go to Settings -> Secrets on your GitHub repository.
6. Create a new repository secret. Name should be DOCKERHUB_USER and in the value, put the name of your docker hub access token.
7. Create a new repository secret. Name should be DOCKERHUB_TOKEN and in the value, copy the value of dockerhub access token.

**Python Requirements**
1. All the python requirements are listed in the requirements.txt.
2. We also have a requirements.dev.txt in which we list the dependencies that are needed only during development.
3. Later you will see that in the Dockerfile, when we are running the project for the dev environment, we also install the dependencies mentioned in the requirements.dev.txt.
4. Since we already cloned the code base, we already have the requirements.txt and requirements.dev.txt file.
5. **_Depending on when you are using this, the versions for some of these dependencies might need to be updated to the latest versions._**

**Docker Configuration**
1. The Dockerfile needed for Docker configuration is already present in the code base.
2. The Docker File is just a list of steps that docker uses to build our image. The Docker File has all of the operating system level dependencies required for our project. We first choose the base image, install all the dependencies on that image and set up users.
3. The file has detailed comments, so you can go through it and understand what we are doing in the file.
4. Lets test that we can build our image successfully
5. Go to the Termimal and navigate to the diagnostictest folder which contains the Dockerfile and run the below command:
```
docker build .
```
6. If it ran successfully you should see that our image is created successfully.

**Docker Compose Configuration**
1. The docker-compose.yml file needed for Docker Compose configuration is already present in the code base.
2. Dockercompose defines how Docker images should be used to run on our development server.
3. The file has detailed comments, so you can go through it and understand what we are doing in the file.
4. Lets test that we can build our image successfully using docker-compose
5. Go to the Termimal and navigate to the diagnostictest folder which contains the Dockerfile and run the below command:
```
docker-compose build
```
6. This effectively does the same thing as docker build but it does it via the Dockerfile. It builds and tags the images appropriately for running the application.
7. If this command runs successfully you should see that our image is created successfully.
8. Then run the below command
```
docker-compose -f docker-compose-deploy.yml build
```
9. If this command runs successfully you should see that our image is created successfully.

**Linting & Tests**
1. As you might have seen , we use flake8 for linting and this has already been included in the requirements.dev.txt
2. For testing we use the Django test framework that comes with Django.

**GitHub Actions Configuration**
1. The .github/workflows/checks.yml contains the configuration for GitHub Actions.
2. But essentially we set set up a trigger and then steps for linting and testing.
3. We also set up DockerHub authentication using the secrets we created in the settings of our github repo earlier.
4. While its not necessary to set up DockerHub authentication, it gives us the advantage of getting around the rate limits set by docker to pull the base images each time we build our image.
2. The file has detailed comments for each step which you can go through tio get a better understanding of what happens in the file.

## docker-compose.yml vs docker-compose-deploy.yml
1. Both these files are docker compose configuration files. The key difference between them is that docker-compose.yml is set up for being run during development whereas docker-compose-deploy.yml is set up to be run during deployment.
2. The docker-compose.yml file has the ARGS DEV=TRUE. This overwrites the ARGS DEV=FALSE in the Dockerfile and tells docker that we are now building running in a development environment. So the Dockerfile also includes the dependencies from the requirements.dev.txt i.e flake8. So when we want runflake8 on our code or we want to execute the unit tests in our code, we will use docker-compose.yml
3. The docker-compose-deploy.yml does not set ARGS DEV=TRUE. So the ARGS DEV=FALSE in Dockerfile is not overwritten. So the dependencies from requirements.dev.txt are not installed. Also the docker-compose-deploy.yml sets up the proxy service as per our cloud deployment process summary . Please see the Cloud Deployment Process Summary section._When running the docker-compose-deploy.yml file, ensure that that you create a copy of the .env.sample file and name it .env as this is required._
4. **When running on the local machine, we can use either docker-compose.yml or docker-compose-deploy.xml. However using docker-compose-deploy.xml will be more useful as thats what we will run on the clour server as well and so if there are any issues we can catch them earlier.**
5. The ```-f docker-compose-deploy.yml``` tells docker-compose to use the docker-compose-deploy.yml. When not specified it uses the docker-compose.yml by default.
6. _All of the docker-compose commands will also work with docker-compose-deploy.xml except for the flake8 command. This is because flake8 is installed only when the project is built using docker-compose since the ARGS DEV is set to TRUE and the dependency mentioned in requirements.dev.txt i.e flake8 is also installed._



## Build & Run the project on your local machine
1. Open up terminal and navigate to the diagnostictest folder
2. To build the project, run the below command
```
docker-compose -f docker-compose-deploy.yml build
```
2. To run the project, run the below command
```
docker-compose -f docker-compose-deploy.yml up
```
3. You can hit Ctrl C to kill the run.

4. To cleanup the containers that might have been created , run the below command
```
docker-compose -f docker-compose-deploy.yml down
```
5. Its recommended to run the down command before we run the application so that any existing containers are cleaned up.

6. You can also do the same by using docker-compose.xml
```
docker compose build
docker-compose up
docker-compose down
```

## Django Admin
1. Once you run the project, you will need to create a superuser to login to the Django Admin Module.
2. Run ```docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py createsuperuser"``` to create a superuser.
3. Navigate to ```http://127.0.0.1:8000/admin/login/?next=/admin/``` to access the admin page.
4. Login with the superuser login and password.
5. The Django Admin Module will load. You will be able to manage users, authentication & the entities you created in the project i.e diagnostictests & tags in this case.

## Interacting with REST APIs
1. Navigate to ```http://127.0.0.1:80/api/docs``` and you will see the API documentation. The port will depend on which port you used in the docker-compose-deploy.xml.
2. Since we enabled authentication for all of our APIs, we will first need to create an authentication token using the superuser login credentials we created above.
3. Click on the POST /api/user/token & Click on Try it Out.
4. Enter the superuser email and password and click on Execute.
5. You will see a alphanumeric Token value.
6. Now click on Authorize at the top right. Scroll to tokenAuth and in the value enter ```Token value``` . Replace value with the token value you copied.
7. Click on Authorize.
8. Once you are authorized, you can now use any of the other apis.
9. When you try out these apis, you will also see the curl command to call these apis can be used in any other applications looking to call these APIs.

## Other Docker Commands
**Docker Compose Commands**
1. Run ```docker-compose run --rm app sh -c "python manage.py test"``` to run tests
2. Run ```docker-compose run --rm app sh -c "python manage.py wait_for_db"``` to run a command directly
3. Run ```docker-compose run --rm app sh -c "python manage.py makemigrations"``` to create the autogenerated migrations file
4. Run ```docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"``` to migrate the models to the database.
5. Run ```docker volume ls``` to list any volumes
6. Run ```docker volume rm "name of volume"``` to remove the volume
7. Run ```docker-compose run --rm app sh -c "flake8 --max-line-length 120"``` to run linting.
8. Run ```docker-compose run --rm app sh -c "python manage.py startapp user"``` to create a Django app within our project

**Docker Compose Deploy Commands**
1. Run ```docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py test"``` to run tests
2. Run ```docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py wait_for_db"``` to run a command directly
3. Run ```docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py makemigrations"``` to create the autogenerated migrations file
4. Run ```docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"``` to migrate the models to the database.
5. Run ```docker volume -f docker-compose-deploy.yml ls``` to list any volumes
6. Run ```docker volume -f docker-compose-deploy.yml rm "name of volume"``` to remove the volume
7. Run ```docker-compose run -f docker-compose-deploy.yml --rm app sh -c "python manage.py startapp user"``` to create a Django app within our project

**Explanation of a docker-compose command**
Consider ```docker-compose run --rm app sh -c "python manage.py test"``` as an example
1. docker-compose: runs a docker compose command
2. run : will start a specific container using the specified config
3. -rm : tells docker to remove the container once its finished running
4. app : the name of the app defined in the docker compose configuration
5. sh -c : Says we want to run a single shell command on our container
6. "python manage.py test" : Then finally you pass in the Django command you want to run in our container.
7. "docker-compose run --rm app" : This is the docker compose syntax. Everything after that is run on the container.



## Build & Deploy this project to the AWS Cloud
### Cloud Deployment Process Summary
You can think of this Django application having the following:
1. The Python code
2. The database
3. Static files like the CSS , HTML , images etc..

All our python code is executed by the uWSGI server.The database is the PostGres database. The static files like css, html, images etc.. are executed by a web server. We use nginx. We have a proxy service which is used to route user requests based on what the request needs. If its a request for a static file, then its routed to the ngix server. If its any other request then its routed to the uwsgi server.

1. Now if you look in the docker-compose-deploy.yml file, you will see three services.
2. The app service is used to run our application using the uwsgi server
3. The db service is for the database which in our case is the PostGres database.
4. The proxy service is to set up our web server which hosts the proxy as well as the nginx web server. All the configurations and other things needed to bring up the proxy is in the proxy folder.
5. So when we run the docker-compose-deploy up command to bring up our application, first the db , app and proxy services are brought up.
6. The order is enforced by the depends on command in the docker-compose-deploy file.
7. Then the /scripts/run.sh is executed which executes the commands to bring up our service.
8. In the run.sh file, we first ensure that the database is up and running, then we ensure all our static files are copied to a directory which is accessible to the nginx reverse proxy.
9. Then we run the migrations so that the database is upto date.
10. Then we start up the uwsgi server by ensuring that the nginx proxy serice can connet to it.
11. We also mention the number of uwsgi workers needed etc.. and then we also tell it to run the wsgi file in our app folder which ensures that all our Django python apps and their code will be running and reasy to be executed.

Now you are doing all of this on your machine. Which means when you run the docker-compose-deploy up on your machine, it spins up a docker image and then on that image it runs all the services you have defined and brings up your application and so when you access the localhost url you are able to access your application. But since you want your application to be used by users across the internet, instead of using your machine , you need a virtual server in the cloud where you can run the docker-compose-deploy command and all this setup is run there and you app can then be accessed by users across the internet. We use AWS EC2 for the virtual server.



### AWS Setup
1. Create an IAM user incase you do not already have one
2. Create the public private key pair in the /Users/adarshatluri/.ssh folder. Create the .ssh folder if it doesnt exist
3. Run the "ssh-keygen -t rsa -b 4096" to generate the private key public key pair.
4. Using the public key, import a key pair in AWS
5. Create an EC2 instance and include this keypair you imported.
6. Use the steps mentioned in the connect section of AWS in the EC2 instance tab to connect via ssh.
7. Run the below command from the folder containing the keys ssh -i "id_rsa" ec2-user@ec2-34-219-62-6.us-west-2.compute.amazonaws.com
8. Now we Set up Githib deploy key .
9. Run the  "ssh-keygen -t ed25519 -b 4096" in the terminal once you have ssh'd into the ec2 instance.
9. We then run "cat ~/.ssh/id_ed25519.pub" to display the public key.
10. Go to your github account -> the project repo -> settings -> Add deploy keys. And add the deploy key.

### EC2 Instance Setup
**Install and Configure Depdencies**
Use the below commands to configure the EC2 virtual machine running Amazon Linux 2.

**Install Git**
1. sudo yum install git -y

**Install Docker**
1. sudo yum install docker -y
2. make it auto start and give ec2-user permissions to use it
3. sudo systemctl enable docker.service
4. sudo systemctl start docker.service
5. sudo usermod -aG docker ec2-user

**_Note: After running the above, you need to logout by typing exit and re-connect to the server in order for the permissions to come into effect._**

**Install Docker Compose**
1. sudo curl -L "https://github.com/docker/compose/releases/download/v2.27.1}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
2. sudo chmod +x /usr/local/bin/docker-compose
3. Running Docker Service

**Cloning Code**
1. Use Git to clone your project: git clone <project ssh url>

**Running Service**

Ensure you create an .env file before starting the service.

To start the service, run:

```docker-compose -f docker-compose-deploy.yml up -d```

**Stopping Service**

To stop the service, run:

```docker-compose -f docker-compose-deploy.yml down```

To stop service and remove all data, run:

```docker-compose -f docker-compose-deploy.yml down --volumes```

**Viewing Logs**

To view container logs, run:

```docker-compose -f docker-compose-deploy.yml logs```

Add the -f to the end of the command to follow the log output as they come in.

**Updating App**

If you push new versions, pull new changes to the server by running the following command:

```git pull origin```

Then, re-build the app image so it includes the latest code by running:

```docker-compose -f docker-compose-deploy.yml build app```

To apply the update, run:

```docker-compose -f docker-compose-deploy.yml up --no-deps -d app```

The --no-deps -d ensures that the dependant services (such as proxy) do not restart.


**Accessing the API Post Deployment to AWS**
1. Go to AWS->EC2
2. Find the Public IPV4 DNS for your EC2 instance
3. Go to the Public IPV4 DNS\api\docs. For example:

 ```http://ec2-34-219-62-6.us-west-2.compute.amazonaws.com/api/docs```
4. You can also access the admin module at Public IPV4 DNS\admin.
5. You can follow the same steps ad on your local machine to create a superuser i.e by running the docker command.
6. But in this case, you will need to run this after you ssh into your EC2 instance.





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


## Creating a New API based on a new Model
1. Create a new Django App
2. Delete some of the unncessary files like admin, model, migrations etc..
3. Update the models.py in the core app to add the new Model.
4. We first create a serialiser for creating our object
5. Serializers are used to convert complex data types, such as Django model instances, into Python data types that can be easily rendered into JSON, XML, or other content types. Serializers also provide deserialization, allowing parsed data to be converted back into complex types after first validating the incoming data. Serializers in Django are a part of the Django REST framework, a powerful and flexible toolkit for building Web APIs.
6. We create a view that uses this serializer.
7. So when you make the http type request, it goes through to the URL and then it gets passed into this create oject view clause, which will then call the sterilizer and create the object and then return the appropriate response.
8. We then create a url pattern which when accessed will use the View
9. URL -> View-> Serializer -> Model
10. So when a http call is made to the url pattern defined, it calls the view thats is defined which inturn calls the serialiser which in turn uses the model.





