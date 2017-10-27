# !/usr/bin/env python3
# coding: utf-8

import os
import sys
import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException


class KubernetesClient(object):

    # -------------------

    def __init__(self):

        # Configs can be set in Configuration class directly or using helper
        # utility. If no argument provided, the config will be loaded from
        # default location.
        try:
            if os.path.exists(os.path.expanduser(config.kube_config.KUBE_CONFIG_DEFAULT_LOCATION)):
                config.load_kube_config()
            else:
                config.load_incluster_config()
        except Exception as e:
            sys.stderr.write("Exception when loading configuration: %s\n" % e)

        # Clients
        self.ClientV1 = client.CoreV1Api()
        self.ClientV1Beta1Api = client.ExtensionsV1beta1Api()

    # -------------------

    def list_pods(self):
        ret = self.ClientV1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

    def list_pods_by_field_selector(self, field_selector, label_selector='', namespace='default'):
        response = []
        try:
            pods = self.ClientV1.list_namespaced_pod(namespace=namespace, label_selector=label_selector, field_selector=field_selector)
            for pod in pods.items:
                if pod.metadata.deletion_timestamp is None:
                    response.append(pod)
            return response
        except ApiException as e:
            sys.stderr.write("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)

    def list_pods_ips_by_field_selector(self, field_selector, label_selector='', namespace='default'):
        response = []
        try:
            pods = self.ClientV1.list_namespaced_pod(namespace=namespace, label_selector=label_selector, field_selector=field_selector)
            for pod in pods.items:
                if pod.metadata.deletion_timestamp is None:
                    response.append(pod.status.pod_ip)
            return response
        except ApiException as e:
            sys.stderr.write("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)


    def list_pods_by_label_selector(self, label_selector, namespace='default'):
        response = []
        try:
            pods = self.ClientV1.list_namespaced_pod(namespace=namespace, label_selector=label_selector)
            for pod in pods.items:
                if pod.metadata.deletion_timestamp is None:
                    response.append(pod)
            return response
        except ApiException as e:
            sys.stderr.write("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)

    def list_pods_ips_by_label_selector(self, label_selector, namespace='default'):
        ips = []
        try:
            pods = self.ClientV1.list_namespaced_pod(namespace=namespace, label_selector=label_selector)
            for pod in pods.items:
                if pod.metadata.deletion_timestamp is None:
                    ips.append(pod.status.pod_ip)
            return ips
        except ApiException as e:
            sys.stderr.write("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)
            sys.stdout.write("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)

    def deploy_deployment(self, deployment_file, replicas):
        with open(deployment_file) as f:
            dep = yaml.load(f)
            dep['spec']['replicas'] = replicas
            resp = self.ClientV1Beta1Api.create_namespaced_deployment(body=dep, namespace="default")
            print("Deployment created. status='%s'" % str(resp.status))
