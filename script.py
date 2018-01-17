#!/usr/bin/env python3
# coding: utf-8

import time
import argparse
from kubernetesClient.kubernetesClient import KubernetesClient

# Global vars
DOCKER_SERVER_URL = "unix://var/run/docker.sock"
DOCKER_REGISTRY = "./dockerRegistry/config/local.yml"
DEPLOYMENT_FILE = "./deployment.yml"


def main():

    parser = argparse.ArgumentParser(description='A script to run experiments.')
    parser.add_argument('peers_count', metavar='p', type=int, nargs=1, help='the number of peers to deploy')
    args = parser.parse_args()

    # registry = DockerRegistry(DOCKER_REGISTRY)
    # docker = DockerClient(DOCKER_SERVER_URL, registry)

    k8s = KubernetesClient()

    deployment = k8s.get_deployment_object()
    if not deployment:
        k8s.deploy_deployment(DEPLOYMENT_FILE)
    else:
        k8s.update_deployment_replicas(deployment, args.peers_count[0])


if __name__ == '__main__':
    main()
