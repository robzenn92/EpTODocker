FROM python:2.7.14-alpine3.6

# Define timezone
RUN apk add --update tzdata
ENV TZ=Europe/Rome

# To be able to install numpy
# RUN apk add --update make cmake gcc g++ gfortran

# Copy the application folders inside the container
ADD ./messages /usr/src/messages/
ADD ./partialView /usr/src/partialView/
ADD ./epto /usr/src/epto/

ENV PATH=$PATH:/usr/src/
ENV PYTHONPATH /usr/src/

WORKDIR /usr/src/epto

# Install app dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001
CMD [ "python", "app.py" ]