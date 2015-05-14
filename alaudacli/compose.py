import sys
import yaml

import util
from project import Project
from service import Service


def load_project(filepath):
    compose_data = _load_yaml(filepath)
    services = load_services(compose_data)
    project = Project(services)
    return project


def load_services(compose_data):
    services = []
    for service_name, service_data in compose_data.items():
        service = load_service(service_name, service_data)
        services.append(service)
    return services


def load_service(service_name, service_data):
    image_name, image_tag = util.parse_image_name_tag(service_data['image'])
    ports = load_ports(service_data)
    run_command = load_command(service_data)
    service = Service(name=service_name,
                      image_name=image_name,
                      image_tag=image_tag,
                      run_command=run_command,
                      instance_ports=ports)
    return service


def load_ports(service_data):
    ports = None
    if 'ports' in service_data.keys():
        ports = util.parse_instance_ports(service_data['ports'])
    return ports


def load_command(service_data):
    command = ''
    if 'command' in service_data.keys():
        command = service_data['command']
    return command


def _load_yaml(filepath):
    try:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    except:
        print 'Missing or invalid compose yaml file. (Do you have docker-compose.yml in the current directory?)'
        sys.exit(1)
