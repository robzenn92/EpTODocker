# Readme

A real distributed system managed by Kubernetes and composed of Docker containers which run EpTO developed in Python.

![EpTO Network](https://raw.githubusercontent.com/robzenn92/EpTODocker/master/resources/epto_pod_network/epto_pod_network.jpg)

## Requirements

Please, make sure your system has the following installed.
- [Python](https://www.python.org) (3.6)
- [Docker](https://www.docker.com)
- [Kubernetes](https://kubernetes.io) (for local setup download Minikube [v0.24.1](https://github.com/kubernetes/minikube/blob/v0.24.1/CHANGELOG.md))


## Setting up a Python development environment

One common problem with installing packages directly to your current site-packages area is that, if you have more than one project or use Python on your machine for things other than Django, you may run into dependency issues between your applications and the installed packages. For this reason, we'll be using virtualenv to manage our Django installation. This is common, and recommended, practice among Python and Django users. Please continue reading [here](https://jeffknupp.com/blog/2012/02/09/starting-a-django-project-the-right-way/).

Once you have created a new virtual environment, you need to activate it running something like:

```
source ~/.virtualenvs/myenv3/bin/activate
```

Once you have done, you need to install all the packages listed in `requirements.txt`. To do so, you simply need to run the following commands.

```
$ git clone https://github.com/robzenn92/EpTODocker.git
$ cd EpTODocker
$ sh setup.sh
```

## Quick start with minikube

[Minikube](https://github.com/kubernetes/minikube) is a tool that makes it easy to run Kubernetes locally. Minikube runs a single-node Kubernetes cluster inside a VM on your laptop for users looking to try out Kubernetes or develop with it day-to-day. The latest released version of minikube is [v0.23.0](https://github.com/kubernetes/minikube/blob/v0.23.0/CHANGELOG.md).

Please, be sure that docker is running. In order to start up a single-node cluster run:

```
$ minikube start
```

In case you want to have more memory.
```
$ minikube start --memory 4096
```

In case you set up a local [Docker Registry](https://docs.docker.com/registry/), you need to run the following.
```
$ minikube start --insecure-registry localhost:5000
```


The output should look like the following:
```
Starting local Kubernetes v1.8.0 cluster...
Starting VM...
Getting VM IP address...
Moving files into cluster...
Setting up certs...
Connecting to cluster...
Setting up kubeconfig...
Starting cluster components...
Kubectl is now configured to use the cluster.
```

To check whether there is a single-node cluster up and running, we expect the following:

```
$ minikube status
minikube: Running
cluster: Running
kubectl: Correctly Configured: pointing to minikube-vm at 192.168.99.100
```

Once the cluster is running you can interact with it using kubectl commands. In order to stop minikube, just run:
```
$ minikube stop
```

Minikube's configurations are stored in `~/.kube/config`. These will be used by the Kubernetes's client in order to deploy Docker containers and run the experiments.

The address and port of the Kubernetes master can be found as follows.

```
$ kubectl cluster-info | grep 'Kubernetes master'
```

However, if you want to access it via REST Api you can start a [proxy](https://kubernetes.io/docs/tasks/access-kubernetes-api/http-proxy-access-api/) to the Kubernetes API server as follows.

```
$ kubectl proxy --port=8080
Starting to serve on 127.0.0.1:8080
```

Then you can send requests to `http://localhost:8080/api/` as defined in the [API docs](https://kubernetes.io/docs/api-reference/v1.8/).

### Kubernetes Addons

Kubernetes comes with a variety of addons. One of them which is really useful in order to supervise the cluster is [Grafana](https://github.com/grafana/kubernetes-app). You can enable Grafana on your cluster following the steps defined here below or on the [Addons's page](https://github.com/kubernetes/minikube/blob/master/docs/addons.md).

```
$ minikube addons enable heapster
$ minikube addons open heapster
```

Other addons that will be used are [Elasticsearch](https://www.elastic.co), [Fluentd](https://www.fluentd.org) and [Kibana](https://www.elastic.co/products/kibana). These definition can be found [here (v1.8.0)](https://github.com/kubernetes/kubernetes/tree/v1.8.0/cluster/addons/fluentd-elasticsearch). Elasticsearch is a search engine that is responsible for storing our logs and allowing for them to be queried. Fluentd sends log messages from Kubernetes to Elasticsearch, whereas Kibana is a graphical interface for viewing and querying the logs stored in Elasticsearch. You can enable them by executing:

```
$ cd efk
$ sh deploy.sh
```


# Test

To execute tests no matter in which packages they are, please run the following.

```
$ sh run_tests.sh
```

# Build

The project EpTODocker is basically composed of two Docker containers (cyclon and epto). To build both of them is as simple as run the following script. 

```
$ sh build.sh
```

This will run the tests, and in case the tests pass will build the docker images and deploy them into the minikube single-node cluster using the definition stored in `deployment.yml`.

Sometimes you may find helpful to remove `<none>` images. You can do that with the following command.

```
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
```

# Deploy

To deploy EpTO into minikube, you just need to run a kubectl command specifying the deployment.yml file as follows.

```
$ kubectl create -f deployment.yml
```

In order to make the replica set accessible from the outside world, you need to create a service which exposes the NodePort of the pods as follows.

```
$ kubectl expose deployment epto-deployment --type=NodePort
```

Now you can reach a random peer's welcome page available on:

```
$ curl 192.168.99.100:<nodePort>/hello
```

The response should look like the following:

```json
{
    "success": {
        "message": "Hello, world! This is a peer."
    }
}
```