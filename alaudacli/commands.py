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
    print 'Successfully logged in as {}.'.format(username)


def logout():
    auth.delete_token()
    print 'Bye'


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
    print '[service_create]: OK'


def service_update(name, target_num_instances):
    service = Service.fetch(name)
    service.update(target_num_instances)
    print '[service_update]: OK'


def service_inspect(name):
    service = Service.fetch(name)
    result = service.inspect()
    print '[service_inspect]: ' + json.dumps(json.loads(result), indent=2)


def service_start(name):
    service = Service.fetch(name)
    service.start()
    print '[service_start]: OK'


def service_stop(name):
    service = Service.fetch(name)
    service.stop()
    print '[service_stop]: OK'


def service_rm(name):
    Service.remove(name)
    print '[service_rm]: OK'


def service_ps():
    service_list = Service.list()
    util.print_ps_output(service_list)
    print '[service_ps]: OK'


def compose_up(file):
    project = compose.load_project(file)
    project.up()
    print '[compose_up]: OK'


def compose_ps(file):
    project = compose.load_project(file)
    project.ps()
    print '[compose_ps]: OK'


def compose_start(file):
    project = compose.load_project(file)
    project.start()
    print '[compose_start]: OK'


def compose_stop(file):
    project = compose.load_project(file)
    project.stop()
    print '[compose_stop]: OK'


def compose_restart(file):
    project = compose.load_project(file)
    project.restart()
    print '[compose_restart]: OK'


def compose_rm(file):
    project = compose.load_project(file)
    project.rm()
    print '[compose_rm]: OK'


def compose_scale(descriptor, file):
    project = compose.load_project(file)
    scale_dict = util.parse_scale(descriptor)
    project.scale(scale_dict)
    print '[compose_scale]: OK'
