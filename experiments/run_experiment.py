#!/usr/bin/env python3

import argparse
from experiment_parser import ExperimentParser
from kubernetesClient.kubernetesClient import KubernetesClient


def main():

    parser = argparse.ArgumentParser(description='A script to parse experiment configuration.')
    parser.add_argument('config', metavar='c', type=str, nargs=1, help='the path for the configuration file')
    args = parser.parse_args()

    parser = ExperimentParser(args.config[0])
    parser.parse()

    k8s = KubernetesClient()
    k8s.deploy_deployment(parser.deployment_experiment)


if __name__ == '__main__':
    main()