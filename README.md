# Readme

A real distributed system managed by Kubernetes and composed of Docker containers which run EpTO developed in Python.

## Requirements

Please, make sure your system has the following installed.
- [Python](https://www.python.org) (2.7)
- [Docker](https://www.docker.com)
- [Kubernetes](https://kubernetes.io) (minikube)


Once you have done, you need to install all the packages listed in `requirements.txt`. To do so, you simply need to run the following commands.

```
$ git clone https://github.com/robzenn92/EpTODocker.git
$ cd EpTODocker
$ sh setup.sh
```

## Quick start with minikube

Please, be sure that docker is running. In order to start up a single-node cluster run:

```
$ minikube start
```

In case you set up a local [Docker Registry](https://docs.docker.com/registry/), you need to run the following.
```
$ minikube start --insecure-registry localhost:5000
```


The output should look like the following:
```
Starting local Kubernetes v1.7.5 cluster...
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
$ minikube ip
192.168.99.100
```

In order to stop minikube, just run:
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

## Test

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