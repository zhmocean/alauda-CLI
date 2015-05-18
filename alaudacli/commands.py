import getpass
import json
import requests

import util
import auth
import compose
from service import Service


def login(username, password, cloud, endpoint):
    if not username:
        username = raw_input('Username: ')
    if not password:
        password = getpass.getpass()

    api_endpoint = endpoint
    if api_endpoint is None:
        api_endpoint = auth.get_api_endpoint(cloud)
    url = api_endpoint + 'generate-api-token/'
    payload = {'username': username, 'password': password}
    r = requests.post(url, payload)
    d = json.loads(r.text)
    token = d['token']
    auth.save_token(api_endpoint, token)
    print '[alauda] Successfully logged in as {}.'.format(username)


def logout():
    auth.delete_token()
    print '[alauda] Bye'


def service_create(image, name, start, target_num_instances, instance_size, run_command, env, ports, allocation_group, volumes, links):
    image_name, image_tag = util.parse_image_name_tag(image)
    instance_ports = util.parse_instance_ports(ports)
    instance_envvars = util.parse_envvars(env)
    links = util.parse_links(links)
    volumes = util.parse_volumes(volumes)
    service = Service(name=name,
                      image_name=image_name,
                      image_tag=image_tag,
                      target_num_instances=target_num_instances,
                      instance_size=instance_size,
                      run_command=run_command,
                      instance_ports=instance_ports,
                      instance_envvars=instance_envvars,
                      allocation_group=allocation_group,
                      volumes=volumes,
                      links=links)
    if start:
        service.run()
    else:
        service.create()


def service_update(name, target_num_instances):
    service = Service.fetch(name)
    service.update(target_num_instances)


def service_inspect(name):
    service = Service.fetch(name)
    result = service.inspect()
    print '[alauda] ' + json.dumps(json.loads(result), indent=2)


def service_start(name):
    service = Service.fetch(name)
    service.start()


def service_stop(name):
    service = Service.fetch(name)
    service.stop()


def service_rm(name):
    Service.remove(name)


def service_ps():
    service_list = Service.list()
    util.print_ps_output(service_list)


def compose_up(file):
    project = compose.load_project(file)
    project.up()


def compose_ps(file):
    project = compose.load_project(file)
    project.ps()


def compose_start(file):
    project = compose.load_project(file)
    project.start()


def compose_stop(file):
    project = compose.load_project(file)
    project.stop()


def compose_restart(file):
    project = compose.load_project(file)
    project.restart()


def compose_rm(file):
    project = compose.load_project(file)
    project.rm()


def compose_scale(descriptor, file):
    project = compose.load_project(file)
    scale_dict = util.parse_scale(descriptor)
    project.scale(scale_dict)
