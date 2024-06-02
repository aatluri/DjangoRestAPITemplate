#!/bin/sh


set -e

# So what this does is replace all the environment variables in default.conf.tpl and outputs default.conf which is the actual configuration file that is used.
# Starts the nginx server with the configuration we have set above.
    # daemon off means that we want to run nginx in the foreground. It is the primary thing being run by that Docker container and
    # this way all of the logs and everything get output to the screen and the Docker container will continue to run while the engine x server is running.
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'