FROM python:3.6.3-alpine3.6

# Set the defaul port to expose
ARG PORT=5001
ARG FOLDER='epto_project'
ARG DESTINATION_FOLDER='/usr/src'

# Set correct timezone for logging
RUN apk add --update tzdata
ENV TZ=Europe/Rome

# Copy the application folders inside the container
ADD $FOLDER/api $DESTINATION_FOLDER/$FOLDER/api
ADD $FOLDER/epto_project $DESTINATION_FOLDER/$FOLDER/epto_project
ADD $FOLDER/manage.py $DESTINATION_FOLDER/$FOLDER/manage.py
ADD $FOLDER/requirements.txt $DESTINATION_FOLDER/$FOLDER/requirements.txt
ADD $FOLDER/start_prod.sh $DESTINATION_FOLDER/$FOLDER/start_prod.sh

ADD ball $DESTINATION_FOLDER/ball
ADD event $DESTINATION_FOLDER/event
ADD message $DESTINATION_FOLDER/message

ENV PATH=$PATH:$DESTINATION_FOLDER/
ENV PYTHONPATH=$DESTINATION_FOLDER/
RUN ["chmod", "+x", "/usr/src/epto_project/start_prod.sh"]

WORKDIR $DESTINATION_FOLDER/$FOLDER

# Install app dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $PORT
CMD ["sh", "start_prod.sh"]