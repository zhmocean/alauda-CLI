import sys
import yaml

import util
from project import Project
from service import Service


def load_project(filepath):
    compose_data = _load_yaml(filepath)
    services, services_sorted_name = load_services(compose_data)
    project = Project(services, services_sorted_name)
    return project


def _get_links(values):
    def _get_link(value):
        if isinstance(value, str):
            result = value.split(':')
            return result[0]
        elif isinstance(value, dict):
            if len(value) == 1:
                return value.keys()[0]
        return None
    if values is None:
        return values
    link_list = []
    for value in values:
        link = _get_link(value)
        if link is not None:
            link_list.append(link)
    return link_list


def sort_services(compose_data):
    src_dict = compose_data.copy()
    src_keys = src_dict.keys()
    sorted_list = []
    while len(src_dict) > 0:
        for key, value in src_dict.items():
            links = _get_links(value.get('links'))
            if links is None:
                sorted_list.append(key)
                del src_dict[key]
            elif not set(links).issubset(set(src_keys)):
                print "{} has invalid link name".format(links)
                sys.exit(1)
            elif set(links).issubset(set(sorted_list)):
                sorted_list.append(key)
                del src_dict[key]
            else:
                continue
    return sorted_list


def load_services(compose_data):
    services = []
    sorted_list = sort_services(compose_data)
    for service_name in sorted_list:
        service = load_service(service_name, compose_data[service_name])
        services.append(service)
    return services, sorted_list


def load_service(service_name, service_data):
    image_name, image_tag = util.parse_image_name_tag(service_data['image'])
    ports = load_ports(service_data)
    run_command = load_command(service_data)
    links = load_links(service_data)
    volumes = load_volumes(service_data)
    envvars = load_envvars(service_data)
    service = Service(name=service_name,
                      image_name=image_name,
                      image_tag=image_tag,
                      run_command=run_command,
                      instance_envvars=envvars,
                      instance_ports=ports,
                      volumes=volumes,
                      links=links)
    return service


def load_links(service_data):
    return util.parse_links(service_data.get('links'))


def load_ports(service_data):
    return util.parse_instance_ports(service_data.get('ports'))


def load_command(service_data):
    return service_data.get('command', '')


def load_volumes(service_data):
    return util.parse_volumes(service_data.get('volumes', None))


def load_envvars(service_data):
    return util.parse_envvars(service_data.get('environment', {}), ':')


def _load_yaml(filepath):
    try:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    except:
        print 'Missing or invalid compose yaml file. (Do you have docker-compose.yml in the current directory?)'
        sys.exit(1)
