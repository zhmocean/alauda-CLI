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


def services_sort(compose_data):
    src_dic = compose_data.copy()
    src_keys = src_dic.keys()
    sort_list = []
    while len(src_dic) > 0:
        for key, value in src_dic.items():
            link = value.get('links', None)
            if link is None:
                sort_list.append(key)
                del src_dic[key]
            elif not set(link).issubset(set(src_keys)):
                print "{} has invalid link name".format(link)
                sys.exit(1)
            elif set(link).issubset(set(sort_list)):
                sort_list.append(key)
                del src_dic[key]
            else:
                continue
    return sort_list


def load_services(compose_data):
    services = []
    sort_list = services_sort(compose_data)
    for service_name in sort_list:
        service = load_service(service_name, compose_data[service_name])
        services.append(service)
    return services


def load_service(service_name, service_data):
    image_name, image_tag = util.parse_image_name_tag(service_data['image'])
    ports = load_ports(service_data)
    run_command = load_command(service_data)
    links = load_links(service_data)
    service = Service(name=service_name,
                      image_name=image_name,
                      image_tag=image_tag,
                      run_command=run_command,
                      instance_ports=ports,
                      links=links)
    return service


def load_links(service_data):
    links = None
    if 'links' in service_data.keys():
        links = util.parse_links(service_data['links'])
    return links


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
