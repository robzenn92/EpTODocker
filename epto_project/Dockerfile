FROM python:3.6.4-alpine3.7

# Set the defaul port to expose
ARG PORT=5001

# Set the default folders
ARG FOLDER='epto_project'
ARG DEST_FOLDER='/usr/src'

# Set correct timezone for logging
RUN apk add --update tzdata
ENV TZ=Europe/Rome

ENV PATH=$PATH:$DEST_FOLDER/
ENV PYTHONPATH=$DEST_FOLDER/

# Copy the application folders inside the container
ADD $FOLDER/api $DEST_FOLDER/$FOLDER/api
ADD $FOLDER/epto_project $DEST_FOLDER/$FOLDER/epto_project
ADD $FOLDER/manage.py $DEST_FOLDER/$FOLDER/manage.py
ADD $FOLDER/requirements.txt $DEST_FOLDER/$FOLDER/requirements.txt
ADD $FOLDER/start_prod.sh $DEST_FOLDER/$FOLDER/start.sh

ADD ball $DEST_FOLDER/ball
ADD event $DEST_FOLDER/event
ADD message $DEST_FOLDER/message

WORKDIR $DEST_FOLDER/$FOLDER

# Install app dependencies
RUN pip install -r requirements.txt

EXPOSE $PORT
CMD ["sh", "start.sh"]