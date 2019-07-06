FROM manifoldai/orbyter-ml-dev:1.7
ADD requirements_docker.txt /app/requirements_docker.txt
# set working directory to /app/
WORKDIR /app/
# set up pip and install python packages
RUN apt-get update &&\
pip3 install -r requirements_docker.txt
# create unprivileged user
RUN adduser --disabled-password --gecos ‘’ myuser
# make tweetvalidator available in Python path
ENV PYTHONPATH "${PYTHONPATH}:/app/src/"

# Uncomment below and add credentials to access Twitter API
# ENV TWITTER_CONSUMER_KEY "XXX"
# ENV TWITTER_CONSUMER_SECRET "XXX"
# ENV TWITTER_ACCESS_TOKEN "XXX"
# ENV TWITTER_ACCESS_SECRET "XXX"

# Run initial command
CMD bash
