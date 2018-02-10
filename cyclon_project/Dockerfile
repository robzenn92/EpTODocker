FROM python:3.6.4-alpine3.7

# Set the defaul port to expose
ARG PORT=5000

# Set the default folders
ARG FOLDER='cyclon_project'
ARG DEST_FOLDER='/usr/src'

# Set correct timezone for logging
RUN apk add --update tzdata
ENV TZ=Europe/Rome

ENV KUBECONFIG=$DEST_FOLDER/kubernetesClient/config

ENV PATH=$PATH:$DEST_FOLDER/
ENV PYTHONPATH=$DEST_FOLDER/

# Copy the application folders inside the container
ADD $FOLDER/api $DEST_FOLDER/$FOLDER/api
ADD $FOLDER/cyclon_project $DEST_FOLDER/$FOLDER/cyclon_project
ADD $FOLDER/manage.py $DEST_FOLDER/$FOLDER/manage.py
ADD $FOLDER/requirements.txt $DEST_FOLDER/$FOLDER/requirements.txt
ADD $FOLDER/start_prod.sh $DEST_FOLDER/$FOLDER/start.sh

ADD message $DEST_FOLDER/message
ADD partialView $DEST_FOLDER/partialView
ADD kubernetesClient $DEST_FOLDER/kubernetesClient

WORKDIR $DEST_FOLDER/$FOLDER

# Install app dependencies
RUN pip install -r requirements.txt

EXPOSE $PORT
CMD ["sh", "start.sh"]