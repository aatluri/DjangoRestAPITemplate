# This is the base image. Its an nginx image. The default image runs in the root mode ie the privilaged user. That is not secure.
# For security purposes, you want to make sure your application is running with the least privileges that it needs in order to perform its application duties.
# So we're using the engine x unprivileged docker image, which is a Docker image provided by the official engine x repo.
# And it basically gives you an unprivileged instance of engine x, so it's a more secure way to run your application.
FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="Adarsh Atluri"

# Copy the proxy config files and run.sh we created earlier to the image
COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

# Set the environment variable values.
ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000

# Swtich to the root user to set up the image.
USER root

# We create the necessary folders and set permissions accordingly.
# So now as the user, we're creating a new directory and forward slash involves a static which is going to be used to store the static files.
# And then we are setting the permissions on that to seven, five, five so that we can read the contents from the static file.
# We do touch because we need to be able to set permissions on this file so that the nginx user can modify it using the envsubst command.\
# touch creates an emptyfile at the location.
# Then we make nginx user the owner of this file.
# We then add the execution permission to the run.sh script.
RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

# Here we're setting up a volume for /static, so it's the default volume that's going to be created for this image.
# And later on we're going to be mapping this volume using our Docker compose configuration.
VOLUME /vol/static

# We then swtich from the Root user to the nginx user as we dont need to be a root user anymore.
USER nginx

# So this is the default script that's going to be run when you create instances from this image and we're
# simply calling our run.sh scripts that we copied to the image further above.
CMD ["/run.sh"]