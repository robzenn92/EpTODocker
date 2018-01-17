#!/usr/bin/env python3

import os
import sys
import yaml
import shutil
import argparse

CURRENT_PATH = os.path.dirname(__file__)
DEPLOYMENT_FILE = os.path.join(CURRENT_PATH, "..", "deployment.yml")


class ExperimentParser(object):

    def __init__(self, config_path):
        self.output_folder = ""
        self.deployment_experiment = ""
        self.config_path = config_path

    def load_config(self):
        current_path = os.path.dirname(__file__)
        with open(os.path.join(current_path, "config/" + self.config_path)) as f:
            return yaml.load(f)

    def customize_container(self, container, customization):

        new_properties = []
        for custom_env in customization['env']:
            customized = False
            for env in container['env']:
                if custom_env['name'] == env['name']:
                    env['value'] = custom_env['value']
                    customized = True

            if not customized:
                new_properties.append(custom_env)

        for env in new_properties:
            container['env'].append(env)
        container['env'].sort()
        return container

    def prepare_output_folder(self, configuration):

        os.makedirs(self.output_folder)
        with open(DEPLOYMENT_FILE) as f:

            deployment = yaml.load(f)
            deployment['spec']['replicas'] = configuration['replicas']

            # I am customizing containers
            for container in deployment['spec']['template']['spec']['containers']:
                for customization in configuration['spec']['containers']:
                    if customization['name'] == container['name']:
                        container = self.customize_container(container, customization)

            self.deployment_experiment = self.output_folder + '/deployment.yml'

            with open(self.output_folder + '/deployment.yml', 'w') as outfile:
                yaml.dump(deployment, outfile, default_flow_style=False)

    def parse(self):

        configuration = self.load_config()['experiment']

        self.output_folder = configuration['name'].replace(" ", "_") if configuration['name'] else "experiment"
        self.output_folder = os.path.join(CURRENT_PATH, self.output_folder)

        if os.path.exists(self.output_folder):
            shutil.rmtree(self.output_folder)

        if not os.path.exists(self.output_folder):
            self.prepare_output_folder(configuration)

        else:
            sys.exit(
                self.output_folder + " already exists as output folder! " +
                "Please delete it or change the experiment's name in config.yml"
            )


def main():
    parser = argparse.ArgumentParser(description='A script to parse experiment configuration.')
    parser.add_argument('config', metavar='c', type=str, nargs=1, help='the path for the configuration file')
    args = parser.parse_args()
    ExperimentParser(args.config[0]).parse()


if __name__ == '__main__':
    main()
