FROM python:2.7.14-alpine3.6

# Set correct timezone for logging
RUN apk add --update tzdata
ENV TZ=Europe/Rome

# Copy the application folders inside the container
ADD ./messages /usr/src/messages/
ADD ./partialView /usr/src/partialView/
ADD ./kubernetesClient /usr/src/kubernetesClient/
ADD ./cyclon /usr/src/cyclon/

ENV PATH=$PATH:/usr/src/
ENV PYTHONPATH /usr/src/

WORKDIR /usr/src/cyclon

# Install app dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD [ "python", "app.py" ]