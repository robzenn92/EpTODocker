#!/usr/bin/env bash

##########################
# Setup
##########################

function setup {

    echo "Preparing the environment"
    # Install requirements
    pip install -r requirements.txt
    run_tests
}

##########################
# Test
##########################

function run_tests {

    echo "Running tests."
    source ./env/test.env && nose2
}

##########################
# Minikube
##########################

function minikube_status {

    echo "Checking Minikube Status"
    minikube status
}

function run_minikube {

    minikube start
}

function check_minikube {

    minikube_status > /dev/null
    if [ $? -eq 0 ]; then
        echo "Minikube is correctly running."
        return 0
    else
        read -p "Minikube is not running. Do you want to start it? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            run_minikube
        fi
    fi
}

##########################
# Docker
##########################

CYCLON_PATH=cyclon_project
EPTO_PATH=epto_project
KUBERNETES_CLIENT_PATH=kubernetesClient
VERSION=latest

function set_docker_context {

    read -p "Do you want to start working on Minikube context? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
#        minikube_status > /dev/null
#        if [ $? -eq 0 ]; then
#            echo "Minikube is not running. I will start it for you!"
#            run_minikube
#        fi
        eval $(minikube docker-env)
    fi
}

function delete {

    set_docker_context
    echo "Deleting $1"
    docker rmi -f $1
}

function build {

    if run_tests && check_minikube; then
        set_docker_context
        echo "Building $1"
        if [ "$1" = "all" ]; then
            echo "docker build -f ${CYCLON_PATH}/Dockerfile -t cyclon:${VERSION} ."
            docker build -f ${CYCLON_PATH}/Dockerfile -t cyclon:${VERSION} .
            echo "docker build -f ${EPTO_PATH}/Dockerfile -t epto:${VERSION} ."
            docker build -f ${EPTO_PATH}/Dockerfile -t epto:${VERSION} .
            tag_image cyclon
            tag_image epto
        elif [ "$1" = "cyclon" ]; then
            echo "docker build -f ${CYCLON_PATH}/Dockerfile -t $1:${VERSION} ."
            docker build -f ${CYCLON_PATH}/Dockerfile -t $1:${VERSION} .
            tag_image $1
        elif [ "$1" = "epto" ]; then
            echo "docker build -f ${EPTO_PATH}/Dockerfile -t $1:${VERSION} ."
            docker build -f ${EPTO_PATH}/Dockerfile -t $1:${VERSION} .
            tag_image $1
        elif [ "$1" = "kubeclient" ]; then
            echo "docker build -f ${KUBERNETES_CLIENT_PATH}/Dockerfile -f $1:${VERSION} ${KUBERNETES_CLIENT_PATH}"
            docker build -f ${KUBERNETES_CLIENT_PATH}/Dockerfile -t $1:${VERSION} ${KUBERNETES_CLIENT_PATH}
            tag_image $1
        else
            echo "Sorry I don't known any image named $1"
            echo "You can build [ cyclon, epto, kubeclient, all ]."
            exit 1
        fi
    fi
}

function tag_image {

    read -p "Do you want to tag $1? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        tag="884973541725.dkr.ecr.us-west-2.amazonaws.com/thesis:"
        read -p "Is this tag ok for you? [$tag$1] [Y/n] " -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            read -p "Please, enter the tag you want for $1: " -r
            echo
            tag=$REPLY
        else
            tag=$tag$1
        fi
        echo "docker tag $1:$VERSION $tag"
        docker tag $1:${VERSION} $tag
        upload_image $tag
    fi
}

function upload_image {

    echo "docker push $1"
    docker push $1
}

##########################
# Kubernetes
##########################

function deploy {

    echo "Deploying $1"
    kubectl create -f $1
    kubectl get pod -o wide
}

function deploy_grafana {
    kubectl create -f https://raw.githubusercontent.com/aws-samples/aws-workshop-for-kubernetes/master/cluster-monitoring/templates/heapster/heapster.yaml
    kubectl create -f https://raw.githubusercontent.com/aws-samples/aws-workshop-for-kubernetes/master/cluster-monitoring/templates/heapster/heapster-rbac.yaml
    kubectl create -f https://raw.githubusercontent.com/aws-samples/aws-workshop-for-kubernetes/master/cluster-monitoring/templates/heapster/influxdb.yaml
    kubectl create -f https://raw.githubusercontent.com/aws-samples/aws-workshop-for-kubernetes/master/cluster-monitoring/templates/heapster/grafana.yaml
}
##########################
# Kops
##########################

function print_kops_envs {

    echo "-- General ----------------------------------"
    echo " BUCKET_NAME: $BUCKET_NAME"
    echo " CLUSTER_NAME: $CLUSTER_NAME"
    echo " KOPS_STATE_STORE: $KOPS_STATE_STORE"
    echo "-- Node -------------------------------------"
    echo " NODE_COUNT: $KOPS_NODE_COUNT"
    echo " NODE_INSTANCE_TYPE: $KOPS_NODE_INSTANCE_TYPE"
    echo " ZONE: $KOPS_ZONE"
    echo "-- Master -----------------------------------"
    echo " MASTER_INSTANCE_TYPE: $KOPS_MASTER_INSTANCE_TYPE"
    echo "---------------------------------------------"
}

function kops_export_env {

    echo "Exporting environment variables for kops."
    source ./env/kops.env
    print_kops_envs
}

function s3api_check_bucket {

    kops_export_env
    buckets=$(aws s3api list-buckets --query "Buckets[].Name")
    for bucket in $buckets
    do
        if [[ "$bucket" == "\"$BUCKET_NAME\"" ]]; then
            echo "Bucket $BUCKET_NAME found."
            return 1 # Found!
        fi
    done
    echo "Bucket $BUCKET_NAME was not found."
    return 0 # Not found
}

function s3api_create_bucket {

    s3api_check_bucket
    if [ $? -eq 0 ]; then
        echo "k8s-epto-bucket not found, I am creating a new bucket"
        aws s3api create-bucket --bucket $BUCKET_NAME --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2
        echo "I am now enabling the versioning of the bucket"
        aws s3api put-bucket-versioning --bucket prefix-example-com-state-store  --versioning-configuration Status=Enabled
    fi
}

function kops_create {

    s3api_create_bucket

    kops create cluster ${CLUSTER_NAME} \
        --cloud aws \
        --node-count $KOPS_NODE_COUNT \
        --node-size $KOPS_NODE_INSTANCE_TYPE \
        --zones $KOPS_ZONE \
        --master-size $KOPS_MASTER_INSTANCE_TYPE
    kops update cluster ${CLUSTER_NAME} --yes
}

function kops_terminate {

    kops_export_env
    kops delete cluster --name ${CLUSTER_NAME}
    kops delete cluster --name ${CLUSTER_NAME} --yes
}

##########################
# ./shell funct_name args
##########################

# Check if the function exists (bash specific)
if declare -f "$1" > /dev/null; then
    "$@"   # call arguments verbatim
else
  echo "'$1' is not a function" >&2
  exit 1
fi