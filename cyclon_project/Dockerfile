FROM python:3.6.3-alpine3.6

# Set the defaul port to expose
ARG PORT=5000
ARG FOLDER='cyclon_project'
ARG DESTINATION_FOLDER='/usr/src'

# Set correct timezone for logging
RUN apk add --update tzdata
ENV TZ=Europe/Rome

# Copy the application folders inside the container
ADD $FOLDER/api $DESTINATION_FOLDER/$FOLDER/api
ADD $FOLDER/cyclon_project $DESTINATION_FOLDER/$FOLDER/cyclon_project
ADD $FOLDER/manage.py $DESTINATION_FOLDER/$FOLDER/manage.py
ADD $FOLDER/requirements.txt $DESTINATION_FOLDER/$FOLDER/requirements.txt
ADD $FOLDER/start_prod.sh $DESTINATION_FOLDER/$FOLDER/start_dev.sh

ADD message $DESTINATION_FOLDER/message
ADD partialView $DESTINATION_FOLDER/partialView
ADD kubernetesClient $DESTINATION_FOLDER/kubernetesClient

ENV PATH=$PATH:$DESTINATION_FOLDER/
ENV PYTHONPATH=$DESTINATION_FOLDER/
RUN ["chmod", "+x", "/usr/src/cyclon_project/start_dev.sh"]

WORKDIR $DESTINATION_FOLDER/$FOLDER

# Install app dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $PORT
CMD ["sh", "start_dev.sh"]