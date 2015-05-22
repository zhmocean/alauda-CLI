import yaml
from copy import deepcopy
import util
from project import Project
from service import Service
from exceptions import AlaudaInputError
import os


def load_project(filepath):
    abspath = os.path.abspath(filepath)
    compose_data = _load_yaml(abspath)
    vertex_list = [abspath]
    edge_list = []
    load_extends_file(compose_data, abspath, vertex_list, edge_list)
    services = load_services(compose_data)
    project = Project(services)
    return project


def _get_linked_services(link_list):
    parsed_links = util.parse_links(link_list)
    return [x[0] for x in parsed_links]


def sort_services(compose_data):
    src_dict = compose_data.copy()
    src_keys = src_dict.keys()
    sorted_list = []
    while len(src_dict) > 0:
        for key, value in src_dict.items():
            links = _get_linked_services(value.get('links'))
            if links is None:
                sorted_list.append(key)
                del src_dict[key]
            elif not set(links).issubset(set(src_keys)):
                raise AlaudaInputError("{} has invalid link name".format(links))
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
    return services


def load_service(service_name, service_data):
    image_name, image_tag = util.parse_image_name_tag(service_data['image'])
    ports = load_ports(service_data)
    run_command = load_command(service_data)
    links = load_links(service_data)
    volumes = load_volumes(service_data)
    envvars = load_envvars(service_data)
    domain = load_domain(service_data)
    instance_num, instance_size = load_instance(service_data)
    scale_mode, auto_scale_cfg = load_scale(service_data)
    service = Service(name=service_name,
                      image_name=image_name,
                      image_tag=image_tag,
                      run_command=run_command,
                      instance_envvars=envvars,
                      instance_ports=ports,
                      volumes=volumes,
                      links=links,
                      target_num_instances=instance_num,
                      instance_size=instance_size,
                      scaling_mode=scale_mode,
                      autoscaling_config=auto_scale_cfg,
                      custom_domain_name=domain)
    return service


def load_domain(service_data):
    return service_data.get('domain', None)


def load_instance(service_data):
    size = service_data.get('size', 'XS')
    number = service_data.get('number', 1)
    return number, size


def load_scale(service_data):
    autoscaling_config = service_data.get('autoscaling_config', None)
    if autoscaling_config is None:
        return util.parse_autoscale_info(None)
    return util.parse_autoscale_info((True, autoscaling_config))


def load_links(service_data):
    return util.parse_links(service_data.get('links'))


def load_ports(service_data):
    return util.parse_instance_ports(service_data.get('ports'))


def load_command(service_data):
    return service_data.get('command', '')


def load_volumes(service_data):
    return util.parse_volumes(service_data.get('volumes'))


def load_envvars(service_data):
    return util.parse_envvars(service_data.get('environment'))


def load_extends_file(compose_data, file_name, vertex_list, edge_list):
    for local_service_name, local_origin_value in compose_data.items():
        if 'extends' in local_origin_value.keys():
            extends = local_origin_value['extends']
            extend_file_name = os.path.abspath(extends['file'])
            original_service_name = extends['service']
            vertex = extend_file_name
            if vertex not in vertex_list:
                vertex_list.append(vertex)
            edge = (file_name, vertex)
            if edge not in edge_list:
                edge_list.append(edge)
            vertex_tmp = deepcopy(vertex_list)
            edge_tmp = deepcopy(edge_list)
            result = util.topoSort(vertex_tmp, edge_tmp)
            if result is None:
                raise AlaudaInputError('There is a circle in extends. Please check!')
            original_compose_data = _load_yaml(extend_file_name)
            load_extends_file(original_compose_data, extend_file_name, vertex_list, edge_list)
            original_service_value = original_compose_data[original_service_name]
            for key, value in original_service_value.items():
                if key == 'links' or key == 'volumes_from':
                    continue
                elif key == 'ports':
                    merge_original_port(local_origin_value, value)
                elif key == 'expose':
                    merge_original_expose(local_origin_value, value)
                elif key == 'environment':
                    merge_original_environment(local_origin_value, value)
                elif key == 'volumes':
                    merge_original_volume(local_origin_value, value)
                elif key not in local_origin_value.keys():
                    local_origin_value[key] = value
                else:
                    continue


def merge_original_port(local_value, original_value):
    pass


def merge_original_expose(local_value, original_value):
    if local_value.get('expose', None) is None:
        local_value['expose'] = original_value
    else:
        for value in original_value:
            if value not in local_value['expose']:
                local_value['expose'].append(value)


def merge_original_environment(local_value, original_value):
    if local_value.get('environment', None) is None:
        local_value['environment'] = original_value
    else:
        local_envs = util.parse_envvars(local_value['environment'])
        for env in original_value:
            key, _ = util.parse_envvar(env)
            if key not in local_envs.keys():
                local_value['environment'].append(env)


def merge_original_volume(local_value, original_value):
    pass


def _load_yaml(filepath):
    try:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    except:
        raise AlaudaInputError('Missing or invalid compose yaml file at {}.'.format(filepath))
