# !/usr/bin/env python3
# coding: utf-8

import os
import sys
import yaml
import structlog
import logging.config
from kubernetes import client, config
from kubernetes.client.rest import ApiException

# Getting environment variables from Deployment
APP = os.environ['APP']
DEPLOYMENT_NAME = os.environ['DEPLOYMENT_NAME']
DEFAULT_CONTEXT = 'minikube'

#: Default handler
LOGGING_DEFAULT_HANDLER = "console"
#: Default formatter
LOGGING_DEFAULT_FORMATTER = "STANDARD"


def get_logging_formatters():
    return {
        "MINIMAL": {
            "format": "%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "STANDARD": {
            "format": "[%(levelname)-7s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "VERBOSE": {
            "format": "%(asctime)s - %(name)s - %(levelname)-8s %(module)s [%(filename)s:%(lineno)s] %(process)d %(thread)d %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    }


def get_logging_handlers():
    handlers = {
        "console": {
            "level": os.environ['LOG_LEVEL'],
            "class": "logging.StreamHandler",
            "formatter": os.environ['LOG_FORMATTER'],
            "stream": sys.stdout
        },
    }
    return handlers


def get_loggers():
    handlers = [LOGGING_DEFAULT_HANDLER]
    return {
        "": {
            "handlers": handlers,
            "level": os.environ['LOG_LEVEL'],
            "propagate": True
        }
    }


def get_dict_config():
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "root": {
            "level": os.environ['LOG_LEVEL'],
            "handlers": [LOGGING_DEFAULT_HANDLER]
        },
        "formatters": get_logging_formatters(),
        "handlers": get_logging_handlers(),
        "loggers": get_loggers()
    }


logging.config.dictConfig(get_dict_config())
log = logging.getLogger()
logger = structlog.wrap_logger(log)


class KubernetesClient(object):

    # -------------------

    def __init__(self):

        logger.debug('Creating KubernetesClient')

        config_file = os.getenv('KUBECONFIG', None)
        context = os.getenv('KUBECONTEXT', DEFAULT_CONTEXT)

        logger.debug('Configuration file is: ' + os.getenv('KUBECONFIG', 'None'))
        logger.debug('Configuration context is: ' + context)

        list_kube_config_contexts = config.list_kube_config_contexts(config_file)
        print(list_kube_config_contexts)

        try:
            logger.debug('Trying to load config.load_incluster_config()')
            config.load_incluster_config()
        except Exception as e:
            s = str(e)
            logger.critical('Exception when config.load_incluster_config()', exception=s)
            try:
                logger.debug('Trying to load config.load_kube_config()')
                config.load_kube_config(config_file, context)
            except Exception as e:
                s = str(e)
                logger.critical('Exception when config.load_kube_config()', exception=s)

        # Clients
        self.ClientV1 = client.CoreV1Api()
        self.ExtensionsV1beta1Api = client.ExtensionsV1beta1Api()

    # -------------------

    def get_deployment_object(self):
        try:
            return self.ExtensionsV1beta1Api.read_namespaced_deployment(name=DEPLOYMENT_NAME, namespace='default')
        except ApiException:
            return None

    def update_deployment_replicas(self, deployment, replicas):
        # Update pod replicas
        deployment.spec.replicas = replicas
        # Update the deployment
        self.ExtensionsV1beta1Api.patch_namespaced_deployment(name=DEPLOYMENT_NAME, namespace="default", body=deployment)

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

    def deploy_deployment(self, deployment_file):

        try:

            with open(deployment_file) as f:
                dep = yaml.load(f)
                try:
                    self.ExtensionsV1beta1Api.create_namespaced_deployment(body=dep, namespace="default")
                except ApiException as e:
                    sys.stderr.write("Exception when calling ExtensionsV1beta1Api.create_namespaced_deployment: %s\n" % e)

        except Exception as error:
            sys.stderr.write("Exception when trying to open: " + deployment_file + ": " + str(error))


if __name__ == '__main__':

    k8s = KubernetesClient()
    ips = k8s.list_pods_ips_by_field_selector(label_selector="app="+APP, field_selector="status.phase=Running")
    print(ips)
