import getpass
import json
import requests

import util
import auth
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


def service_create(image, name, start, target_num_instances, instance_size, run_command, env, ports, allocation_group, volumes):
    image_name, image_tag = util.parse_image_name_tag(image)
    instance_ports = util.parse_instance_ports(ports)
    instance_envvars = util.parse_envvars(env)
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
                      volumes=volumes)
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
    result = Service.list()
    print '[service_ps]: ' + json.dumps(json.loads(result), indent=2)
