FROM manifoldai/orbyter-ml-dev:1.7
ADD requirements.txt /app/requirements.txt
# set working directory to /app/
WORKDIR /app/
# set up pip and install python packages
RUN apt-get update &&\
pip3 install -r requirements.txt
# create unprivileged user
RUN adduser --disabled-password --gecos ‘’ myuser
# Run initial command
CMD bash
