import sys
import yaml

from project import Project


def load_project(filepath):
    compose_data = _load_yaml(filepath)
    services = load_services(compose_data)
    project = Project(services)
    return project


def load_services(compose_data):
    services = []
    return services


def _load_yaml(filepath):
    try:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    except:
        print 'Missing or invalid compose yaml file. (Do you have docker-compose.yml in the current directory?)'
        sys.exit(1)
