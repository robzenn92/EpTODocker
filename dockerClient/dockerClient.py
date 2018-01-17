#!/usr/bin/env python3
# coding: utf-8

import yaml
import docker
import os


class DockerClient(object):

    def __init__(self, base_url, registry):
        self.client = docker.DockerClient(base_url=base_url)
        self.registry = registry

    def get_image_tag(self, image_path):

        # Checks if a configuration file exists within dockerfile_folder_path
        config_path = os.path.join(image_path, 'config/config.yml')
        config_exists = os.path.exists(config_path)

        # Load local configuration
        if config_exists:
            with open(config_path, 'r') as f:
                config = yaml.load(f)
                return self.registry.address + config['image']['name'] + ":" + config['image']['tag']
        return None

    def build(self, image_path):

        try:
            image = self.client.images.build(
                path=image_path,
                tag=self.get_image_tag(image_path)
            )
        except docker.errors.BuildError:
            print("A BuildError occurred")
        except docker.errors.APIError:
            print("An APIError occurred")

        return image

    def run_container(self, container):
        try:
            run = self.client.containers.run(container)
        except docker.errors.ContainerError:
            print("A ContainerError occurred")
        except docker.errors.ImageNotFound:
            print("The specified image does not exist.")
        except docker.errors.APIError:
            print("If the server returned an error.")
        return run

    def push(self, image_path):
        try:
            self.client.images.push(self.get_image_tag(image_path))
        except docker.errors.APIError as e:
            print ("An APIError occurred: ", e.message)
