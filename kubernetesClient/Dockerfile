FROM python:3.6.3-alpine3.6

# Set correct timezone for logging
RUN apk add --update tzdata
ENV TZ=Europe/Rome

ENV PATH=$PATH:/usr/src/
ENV PYTHONPATH /usr/src/
ENV KUBECONFIG config

# Copy the application folders inside the container
ADD . /usr/src/kubernetesClient/
WORKDIR /usr/src/kubernetesClient

# Install app dependencies
RUN pip install -r requirements.txt

CMD [ "python", "kubernetesClient.py" ]